import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import DateEntry
import time
from model.tarefa import Tarefa
from model.pessoa import Pessoa
import clienteCherrypy


class TaskListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tarefas")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        self.tasks = []
        self.next_id = 1
        self.idUser = None
        self.user = None
        self.load_tasks()
        
        self.setup_main_screen()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        
    
    def user_button_on_click(self):
        # primeiro, limpe/exiba as tarefas antigas
        self.tasks = []
        self.display_tasks()

        user_name = self.user_entry.get()
        user = clienteCherrypy.get_person(user_name)

        # Se houver texto exibido antes, esconda temporariamente
        self.no_tasks_label.pack_forget()

        # Se não veio usuário (problema de conexão)
        if not user:
            self.no_tasks_label.config(text="falha de conexão")
            self.no_tasks_label.pack(fill=tk.X, pady=10)
            return

        # Se a resposta trouxe erro
        if user.get("erro"):
            self.no_tasks_label.config(text=user.get("erro"))
            self.no_tasks_label.pack(fill=tk.X, pady=10)
            return

        # Se chegou até aqui, usuário existe—esconda o label de erro (caso estivesse visível)
        self.no_tasks_label.pack_forget()

        # Agora carrega tarefas normalmente
        self.idUser = user["pessoa"]["idPessoa"]
        self.user = Pessoa(user["pessoa"]["idPessoa"], user["pessoa"]["userName"], user["pessoa"]["nome"])
        
        self.load_tasks()
        self.display_tasks()


    def delete_user(self):
        confirm = messagebox.askyesno("Confirmar", "Deseja excluir?")
        
        if confirm:
            r = clienteCherrypy.delete_pessoa(self.idUser)
            if r:
                print("excluido com sucesso")
            elif r.get("erro"):
                messagebox.showerror("Erro", f"{r.get("erro")}")
            self.load_tasks()
            self.display_tasks()
        

    def setup_main_screen(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        user_label = tk.Label(self.root, text="Nome:")
        user_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.user_entry = tk.Entry(self.root)
        self.user_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.user_button = tk.Button(self.root, text="Buscar", command=self.user_button_on_click)
        self.user_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_user_button = tk.Button(self.root, text="Add User", command=self.open_insert_user)
        self.add_user_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_user_button = tk.Button(self.root, text="Edit User", command=lambda t=True: self.open_edit_user_screen(t))
        self.edit_user_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.del_user_button = tk.Button(self.root, text="Del User", command=self.delete_user)
        self.del_user_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Título
        title_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="Lista de Tarefas", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT)
        
        # Container para lista de tarefas com scroll
        self.tasks_container = tk.Frame(self.main_frame, bg="#ffffff")
        self.tasks_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas com scrollbar
        self.canvas = tk.Canvas(self.tasks_container, bg="#ffffff")
        self.scrollbar = ttk.Scrollbar(self.tasks_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ffffff")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Botão flutuante para adicionar tarefa
        self.add_button = tk.Button(
            self.root, 
            text="+", 
            font=("Helvetica", 16, "bold"),
            bg="#4CAF50", 
            fg="white", 
            relief=tk.RAISED,
            command=self.open_add_task_screen
        )
        self.add_button.place(relx=0.9, rely=0.9, width=50, height=50)
        
        self.display_tasks()
    
    def on_canvas_resize(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def on_close(self):

        self.root.destroy()

    
    
    def truncate_text(self, text, max_length=40):
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text
    
    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            day, month, year = map(int, date_str.split('/'))
            return datetime.date(year, month, day)
        except:
            return None
    
    def display_tasks(self):
        # Limpar as tarefas atuais
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Pegar todas as tarefas
        all_tasks = self.tasks

        if not all_tasks:
            self.no_tasks_label = tk.Label(self.scrollable_frame, text="Nenhuma tarefa cadastrada", 
                                     font=("Helvetica", 12), bg="#ffffff", pady=20)
            self.no_tasks_label.pack(fill=tk.X)
            return

        # Separar tarefas em concluídas e não concluídas
        completed_tasks = []
        incomplete_tasks = []

        for task in all_tasks:
            if int(task.status):  # Se status = 1 (concluída)
                completed_tasks.append(task)
            else:
                incomplete_tasks.append(task)

        # Para tarefas não concluídas, separar com e sem data
        incomplete_with_date = []
        incomplete_without_date = []

        for task in incomplete_tasks:
            try:
                if task.dataTermino and not isinstance(task.dataTermino, str):
                    parsed_date = datetime.datetime.fromtimestamp(int(task.dataTermino))
                    incomplete_with_date.append((task, parsed_date))
                else:
                    incomplete_without_date.append(task)
            except:
                incomplete_without_date.append(task)

        # Ordenar tarefas não concluídas com data por data limite (mais próximas primeiro)
        incomplete_with_date.sort(key=lambda x: x[1])

        # Montar a lista final: 
        # 1. Não concluídas com data (ordenadas por proximidade) 
        # 2. Não concluídas sem data
        # 3. Concluídas (no final)
        sorted_tasks = ([task for task, _ in incomplete_with_date] + 
                        incomplete_without_date + 
                        completed_tasks)

        # Exibir as tarefas ordenadas
        for task in sorted_tasks:
            self.create_task_card(task)
    
    def create_task_card(self, task):
        # Card da tarefa
        card_frame = tk.Frame(self.scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
        card_frame.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
        
        # Frame para título e descrição
        info_frame = tk.Frame(card_frame, bg="white")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Título
        title_label = tk.Label(info_frame, text=task.nome, font=("Helvetica", 12, "bold"), 
                              anchor="w", bg="white")
        title_label.pack(fill=tk.X)
        
        # Descrição truncada
        desc_text = self.truncate_text(task.descricao)
        desc_label = tk.Label(info_frame, text=desc_text, font=("Helvetica", 10), 
                             fg="gray", anchor="w", bg="white")
        desc_label.pack(fill=tk.X)
        
        # Data para finalizar (adicionado no card)
        if task.dataTermino:

            if not isinstance(task.dataTermino,str):
                # Converter o timestamp para um objeto datetime
                data = datetime.datetime.fromtimestamp(task.dataTermino)

                # Formatar a data no formato dia/mês/ano
                data_formatada = data.strftime("%d/%m/%Y")
            else: data_formatada = task.dataTermino

            date_label = tk.Label(info_frame, text=f"Prazo: {data_formatada}", font=("Helvetica", 9), 
                                fg="#666666", anchor="w", bg="white")
            date_label.pack(fill=tk.X, pady=(3, 0))

            if task.dataDeTermino:
                
                # Converter o timestamp para um objeto datetime
                data = datetime.datetime.fromtimestamp(int(task.dataDeTermino))

                # Formatar a data no formato dia/mês/ano
                data_formatada = data.strftime("%d/%m/%Y")

                date_label = tk.Label(info_frame, text=f"Finalizado em: {data_formatada}", font=("Helvetica", 9), 
                                    fg="#666666", anchor="w", bg="white")
                date_label.pack(fill=tk.X, pady=(3, 0))

            
            
        
        # Frame para botões
        buttons_frame = tk.Frame(card_frame, bg="white")
        buttons_frame.pack(side=tk.RIGHT, padx=5)
        
        # Botão de editar
        edit_button = tk.Button(buttons_frame, text="✏️", font=("Helvetica", 10), bg="white", bd=1,
                              command=lambda t=task: self.open_edit_task_screen(t))
        edit_button.pack(side=tk.LEFT, padx=2)
        
        # Botão de excluir
        delete_button = tk.Button(buttons_frame, text="🗑️", font=("Helvetica", 10), bg="white", bd=1,
                                command=lambda t=task: self.delete_task(t))
        delete_button.pack(side=tk.LEFT, padx=2)
        
        # Botão para marcar como concluída
        check_button = tk.Button(buttons_frame, text="✓", font=("Helvetica", 10), bg="white", bd=1,
                               command=lambda t=task: self.complete_task(t))
        check_button.pack(side=tk.LEFT, padx=2)
        
        # Associar clique no card para abrir detalhes
        card_frame.bind("<Button-1>", lambda e, t=task: self.open_task_details(t))
        title_label.bind("<Button-1>", lambda e, t=task: self.open_task_details(t))
        desc_label.bind("<Button-1>", lambda e, t=task: self.open_task_details(t))
        info_frame.bind("<Button-1>", lambda e, t=task: self.open_task_details(t))
        if task.dataTermino:
            date_label.bind("<Button-1>", lambda e, t=task: self.open_task_details(t))
    
    def open_task_details(self, task):
        print(task.idTarefa)
    
       
        details_window = tk.Toplevel(self.root)
        details_window.title("Detalhes da Tarefa")
        details_window.geometry("400x400")  # Aumentei mais a altura para garantir que tudo seja visível
        details_window.configure(bg="#f0f0f0")
        
        # Frame para detalhes
        details_frame = tk.Frame(details_window, bg="#f0f0f0", padx=20, pady=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(details_frame, text="Título:", font=("Helvetica", 10, "bold"), 
                              anchor="w", bg="#f0f0f0")
        title_label.pack(fill=tk.X, pady=(0, 5))
        
        title_value = tk.Label(details_frame, text=task.nome, font=("Helvetica", 12), 
                              anchor="w", bg="white", relief=tk.GROOVE, padx=10, pady=5)
        title_value.pack(fill=tk.X, pady=(0, 10))
        
        # Descrição
        desc_label = tk.Label(details_frame, text="Descrição:", font=("Helvetica", 10, "bold"), 
                             anchor="w", bg="#f0f0f0")
        desc_label.pack(fill=tk.X, pady=(0, 5))
        
        desc_frame = tk.Frame(details_frame, bg="white", relief=tk.GROOVE, padx=10, pady=5)
        desc_frame.pack(fill=tk.X, pady=(0, 10), ipady=5)  # Mudei para tk.X e adicionei ipady
        
        desc_value = tk.Text(desc_frame, font=("Helvetica", 11), wrap=tk.WORD, 
                            borderwidth=0, highlightthickness=0, height=8)  # Defini altura fixa
        desc_value.insert("1.0", task.descricao)
        desc_value.config(state=tk.DISABLED)
        desc_value.pack(fill=tk.X)
        
        # Data - Garantir que essa seção apareça após a descrição
        date_frame = tk.Frame(details_frame, bg="#f0f0f0")
        date_frame.pack(fill=tk.X, pady=(10, 5))
        
        date_label = tk.Label(date_frame, text="Data para finalizar:", font=("Helvetica", 10, "bold"), 
                             anchor="w", bg="#f0f0f0")
        date_label.pack(fill=tk.X)
        
        # Verifica se há uma data e exibe ou exibe "Não definida"

        # Converter o timestamp para um objeto datetime
        data = datetime.datetime.fromtimestamp(task.dataTermino)

        # Formatar a data no formato dia/mês/ano
        data_formatada = data.strftime("%d/%m/%Y")
        
        date_text = data_formatada
        date_value = tk.Label(details_frame, text=date_text, font=("Helvetica", 12), 
                             anchor="w", bg="white", relief=tk.GROOVE, padx=10, pady=5)
        date_value.pack(fill=tk.X, pady=(0, 10))
        
        # Botão para marcar como concluída
        complete_button = tk.Button(details_frame, text="Marcar como Concluída", font=("Helvetica", 12),
                                  bg="#4CAF50", fg="white", pady=5,
                                  command=lambda: [self.complete_task(task), details_window.destroy()])
        complete_button.pack(fill=tk.X, pady=10)

    def open_add_task_screen(self):
        self.open_task_form()
    
    def open_edit_task_screen(self, task):
        self.open_task_form(task)

    def open_edit_user_screen(self, user):
        self.open_insert_user(user)
    

    def open_insert_user(self, user=None):

       
        form_window = tk.Toplevel(self.root)
        title =  "Editar Usuário" if user else "Inserir usuário"
        form_window.title(title)
        form_window.geometry("400x350")
        form_window.configure(bg="#f0f0f0")
        
        # Frame para formulário
        form_frame = tk.Frame(form_window, bg="#f0f0f0", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # username
        title_label = tk.Label(form_frame, text="username:", font=("Helvetica", 10, "bold"), 
                              anchor="w", bg="#f0f0f0")
        title_label.pack(fill=tk.X, pady=(0, 5))
        
        username_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # nome
        name_label = tk.Label(form_frame, text="nome:", font=("Helvetica", 10, "bold"), 
                             anchor="w", bg="#f0f0f0")
        name_label.pack(fill=tk.X, pady=(0, 5))
        
        name_entry = tk.Entry(form_frame, font=("Helvetica", 11))
        name_entry.pack(fill=tk.X, pady=(0, 10))
        
        if user:
            username_entry.insert(0, self.user.userName)
            name_entry.insert(0, self.user.nome)
        

        # Botão de salvar
        save_button = tk.Button(form_frame, text="Salvar", font=("Helvetica", 12),
                              bg="#4CAF50", fg="white", pady=5,
                              command=lambda: self.save_user(
                                  username_entry.get(),
                                  name_entry.get(),
                                  form_window,
                                  self.idUser if user else None
                              ))
        save_button.pack(fill=tk.X, pady=10)

    def open_task_form(self, task=None):
        is_edit = task is not None
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Editar Tarefa" if is_edit else "Nova Tarefa")
        form_window.geometry("400x350")
        form_window.configure(bg="#f0f0f0")
        
        # Frame para formulário
        form_frame = tk.Frame(form_window, bg="#f0f0f0", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(form_frame, text="Título:", font=("Helvetica", 10, "bold"), 
                              anchor="w", bg="#f0f0f0")
        title_label.pack(fill=tk.X, pady=(0, 5))
        
        title_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Descrição
        desc_label = tk.Label(form_frame, text="Descrição:", font=("Helvetica", 10, "bold"), 
                             anchor="w", bg="#f0f0f0")
        desc_label.pack(fill=tk.X, pady=(0, 5))
        
        desc_text = tk.Text(form_frame, font=("Helvetica", 11), height=6)
        desc_text.pack(fill=tk.X, pady=(0, 10))
        
        # Data
        date_label = tk.Label(form_frame, text="Data para finalizar:", font=("Helvetica", 10, "bold"), 
                             anchor="w", bg="#f0f0f0")
        date_label.pack(fill=tk.X, pady=(0, 5))
        
        date_entry = DateEntry(form_frame, font=("Helvetica", 12), date_pattern="dd/mm/yyyy")
        date_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Preencher campos se for edição
        if is_edit:
            title_entry.insert(0, task.nome)
            desc_text.insert("1.0", task.descricao)
            if task.dataTermino:
                # Converter o timestamp para um objeto datetime
                data = datetime.datetime.fromtimestamp(task.dataTermino)

                # Formatar a data no formato dia/mês/ano
                data_formatada = data.strftime("%d/%m/%Y")
                try:
                    day, month, year = map(int, data_formatada.split('/'))
                    date_entry.set_date(datetime.date(year, month, day))
                except:
                    pass
            
        # Botão de salvar
        save_button = tk.Button(form_frame, text="Salvar", font=("Helvetica", 12),
                              bg="#4CAF50", fg="white", pady=5,
                              command=lambda: self.save_task(
                                  title_entry.get(),
                                  desc_text.get("1.0", tk.END).strip(),
                                  date_entry.get_date().strftime("%d/%m/%Y"),
                                  task.idTarefa if is_edit else None,
                                  form_window
                              ))
        save_button.pack(fill=tk.X, pady=10)

    def save_user(self, username, name, window=None, idUser = None):
        result = None
        if idUser:
            result = clienteCherrypy.update_pessoa(Pessoa(idUser, username, name))
        else:
            result = clienteCherrypy.add_person(username, name)
        if not result:
            messagebox.showerror("Erro", "Falha de conexão")
        elif result.get("erro"):
            messagebox.showerror("Erro", result.get("erro"))
        else:
            self.idUser = result.get("id")
            if (window):
                window.destroy()
    
    def save_task(self, nome, descricao, dataTermino, idTarefa=None, window=None):
        if not nome:
            messagebox.showwarning("Atenção", "O título da tarefa é obrigatório!")
            return
        
        # Converter a string para um objeto datetime
        data_obj = datetime.datetime.strptime(dataTermino, "%d/%m/%Y")
    
        # Obter o timestamp em segundos (resultado em float)
        timestamp_sec = data_obj.timestamp()
    
        # Se preferir o timestamp como inteiro:
        timestamp_sec_int = int(timestamp_sec)

        if idTarefa:  # Edição

            clienteCherrypy.update_task(Tarefa(idTarefa, nome, descricao, None, timestamp_sec_int))

            for tarefa in self.tasks:
                if tarefa.idTarefa == idTarefa:

                    

                    tarefa.nome = nome
                    tarefa.descricao = descricao
                    tarefa.dataTermino = dataTermino
            
                
        else:  # Nova tarefa
            
        
            r = clienteCherrypy.add_task(Tarefa(nome= nome, descricao = descricao, dataTermino =  timestamp_sec_int, idPessoa=self.idUser ))
            
          
              
            if not r:
                messagebox.showerror("Erro", "Falha de conexão") 
            elif r.get("erro"): 
                messagebox.showerror("Erro", r.get("erro")) 
            else:
                print("adicionado com sucesso")
        
        self.load_tasks()
        self.display_tasks()
        
        if window:
            window.destroy()
    
    def delete_task(self, task):
        confirm = messagebox.askyesno("Confirmar", "Deseja excluir esta tarefa?")
        
        if confirm:
            clienteCherrypy.delete_task(task.idTarefa)
            self.load_tasks()
            self.display_tasks()
    
    def complete_task(self, task):
        if (task.status): return
        task.status = 1
        task.dataDeTermino =  int(time.time())


        result = clienteCherrypy.update_task(task)
        if(result.get("sucesso")):
            messagebox.showinfo("Sucesso", "Tarefa marcada como concluída!")
        elif (result.get("erro")):
            messagebox.showerror("Erro", f"{result.get("erro")}")
        else:
            messagebox.showerror("Erro", "Falha de conexão")

        self.load_tasks()
        
        self.display_tasks()
        
    

    
    def load_tasks(self):
        if self.idUser:
            self.tasks = clienteCherrypy.list_person_tasks(self.idUser)
        

if __name__ == "__main__":
    root = tk.Tk()
    
    app = TaskListApp(root)
    root.mainloop()