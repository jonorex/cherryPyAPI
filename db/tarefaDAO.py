from db.connection import Banco
import datetime


from model.tarefa import Tarefa


class TarefaDAO:
    def __init__(self, conexao):
        
        self.tarefa = Tarefa()
        

        self.con = conexao
    
        

  


    def salvar(self, tarefa: Tarefa):
        self.tarefa = tarefa
        sql = """
            INSERT INTO TAREFA (NOME, DESCRICAO, DATACRIACAO, DATATERMINO, IDPESSOA) VALUE (%s, %s, %s, %s, %s)
        """

        cursor  = self.con.cursor()
        self.tarefa.dataCriacao = int(datetime.datetime.now().timestamp())
        self.tarefa.dataTermino = int(self.tarefa.dataTermino)
        cursor.execute(sql, (
            self.tarefa.nome, 
            self.tarefa.descricao, 
            self.tarefa.dataCriacao,
            self.tarefa.dataTermino,
            self.tarefa.idPessoa))
        
        self.con.commit()
        self.tarefa.idTarefa = cursor.lastrowid
        cursor.close()

        if (self.tarefa.idTarefa == None): self.tarefa.idTarefa = 0

        return self.tarefa.idTarefa

    def buscar(self, id: int):
        cursor = self.con.cursor()

        cursor.execute("SELECT * FROM tarefa WHERE idTarefa = %s ", (id,))

        
        result = cursor.fetchone()
        cursor.close()

        if (result is None):
            return None

        tarefa =  Tarefa(*result)
        print(f"linha 91 {result}")
        return tarefa


    def atualizar(self, tarefa: Tarefa):
        self.tarefa = tarefa

        sql = "update tarefa set "
        fields = []  # Use uma lista em vez de tuple para poder adicionar elementos
        if self.tarefa.nome:
            sql += "nome = %s, "
            fields.append(self.tarefa.nome)
        if self.tarefa.descricao:
            sql += "descricao = %s, "
            fields.append(self.tarefa.descricao)
        if self.tarefa.dataCriacao:
            sql += "dataCriacao = %s, "
            fields.append(self.tarefa.dataCriacao)  # Esta linha estava faltando o append
        if self.tarefa.dataTermino:
            sql += "dataTermino = %s, "
            fields.append(self.tarefa.dataTermino)
        if self.tarefa.status:
            sql += "status = %s, "
            fields.append(self.tarefa.status)
        if self.tarefa.dataDeTermino:
            sql += "dataDeTermino = %s, "  
            fields.append(self.tarefa.dataDeTermino)
        # Remova a vírgula final se existir
        if sql.endswith(", "):
            sql = sql[:-2]
        sql += " where idTarefa = %s"
        fields.append(self.tarefa.idTarefa)
        
        cursor = self.con.cursor()
        cursor.execute(sql, tuple(fields))  # Converta a lista para tupla
        self.con.commit()
        retorno = ''
        # um registro foi alterado
        if cursor.rowcount > 0:
            retorno = True
        # nenhum registro foi alterado, atualização falhou
        else:
            retorno = False
        cursor.close()
        return retorno

    def deletar(self, id: int):
        cursor = self.con.cursor()

        cursor.execute("DELETE FROM tarefa WHERE idTarefa = %s ", (id,))

        self.con.commit()
        r = ''
        if (cursor.rowcount > 0):
            r = True
        else:
            r = False
        cursor.close()
        return r
    
    def listarTarefas(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM tarefa")

        # Consome o resultado primeiro
        result = cursor.fetchall()

        objetos = [Tarefa(*tarefa) for tarefa in result]


        for tarefa in objetos: 
            print(tarefa)

        cursor.close()

        return objetos