from db.tarefaDAO import TarefaDAO
import model.tarefa as tarefa
import cherrypy
import time
from model.pessoa import Pessoa
from db.pessoaDAO import PessoaDAO
from db.connection import Banco

DAY_DIF = 3600*23+59*60+59

class Server:
    def __init__(self):
        banco = Banco()
        conexao = banco.get_conexao()
        self.tarefaDAO = TarefaDAO(conexao)
        self.pessoaDAO = PessoaDAO(conexao)

    @cherrypy.expose
    @cherrypy.tools.json_in()   # lê JSON do corpo da requisição
    @cherrypy.tools.json_out()  # converte o retorno Python -> JSON
    def adicionarTarefa(self): #retorna o id inserido

        dados = cherrypy.request.json

        novaTarefa = tarefa.Tarefa(
            nome = dados.get("nome"),
            descricao = dados.get("descricao"),
            dataTermino = dados.get("dataTermino"),
            idPessoa= dados.get("idPessoa")
        )

        dif =  novaTarefa.dataTermino-time.time() + DAY_DIF
        
        if (len(novaTarefa.nome) > 0 and len(novaTarefa.descricao) and dif > 0 and novaTarefa.idPessoa):
            if (self.pessoaDAO.buscarPessoaId(novaTarefa.idPessoa)):

                novo_id = self.tarefaDAO.salvar(novaTarefa)
            else: 
                cherrypy.response.status = 404
                return {"sucesso": False, "erro": "Pessoa não encontrada"}

            return {"id": novo_id}
        else:
            cherrypy.response.status = 422
            return {"sucesso": False, "erro": "Você errou o valor de algum campo"}


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def buscarTarefa(self, id: int):

        try:
            tarefa_obj = self.tarefaDAO.buscar(int(id))
            if tarefa_obj is None:
                cherrypy.response.status = 404
                return {"erro": "Tarefa não encontrado"}
            return {"tarefa": tarefa_obj.__dict__}
        except ValueError:
            cherrypy.response.status = 400
            return {"erro": "ID inválido"}
    


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def listarTarefas(self):
        
        lista = self.tarefaDAO.listarTarefas()  # espera-se lista de objetos Tarefa
        # Converte cada objeto Tarefa num dicionário
        resultado = [t.__dict__ for t in lista]
        return {"tarefas": resultado}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def listarTarefasPessoa(self, id):
        
        lista = self.pessoaDAO.buscarTarefas(id)  # espera-se lista de objetos Tarefa
        # Converte cada objeto Tarefa num dicionário
        resultado = [t.__dict__ for t in lista]
        return {"tarefas": resultado}


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def atualizarTarefa(self):
    
        dados = cherrypy.request.json
        # Validação mínima de presença de ID
        if "idTarefa" not in dados:
            cherrypy.response.status = 400
            return {"sucesso": False, "erro": "Campo 'id' obrigatório"}

        try:
            tid = int(dados["idTarefa"])
        except ValueError:
            cherrypy.response.status = 400
            return {"sucesso": False, "erro": "ID inválido"}

        # Busca a tarefa existente (para manter outros campos que não foram enviados)
        existente = self.tarefaDAO.buscar(tid)
        if existente is None:
            cherrypy.response.status = 404
            return {"sucesso": False, "erro": "Tarefa não encontrada"}

        # Atualiza somente os campos presentes em dados (exceto id)
        # Ajuste conforme os atributos reais da sua classe Tarefa
        if "descricao" in dados:
            existente.descricao = dados["descricao"]
        if "concluida" in dados:
            existente.concluida = dados["concluida"]
        if "nome" in dados:
            existente.nome = dados["nome"]
        if "dataTermino" in dados:
            existente.dataTermino = dados["dataTermino"]
        if "dataDeTermino" in dados:
            existente.dataDeTermino = dados["dataDeTermino"]
        if "status" in dados:
            existente.status = dados["status"]
        # adicione outros campos aqui, se necessário

        

        ok = self.tarefaDAO.atualizar(existente)
        return {"sucesso": bool(ok)}
    

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def atualizarPessoa(self):
    
        dados = cherrypy.request.json
        # Validação mínima de presença de ID
        if "idPessoa" not in dados:
            cherrypy.response.status = 400
            return {"sucesso": False, "erro": "Campo 'id' obrigatório"}

        try:
            tid = int(dados["idPessoa"])
        except ValueError:
            cherrypy.response.status = 400
            return {"sucesso": False, "erro": "ID inválido"}

        # Busca a tarefa existente (para manter outros campos que não foram enviados)
        existente = self.pessoaDAO.buscarPessoaId(tid)
        if existente is None:
            cherrypy.response.status = 404
            return {"sucesso": False, "erro": "Usuário não encontrado"}

        # Atualiza somente os campos presentes em dados (exceto id)
        # Ajuste conforme os atributos reais da sua classe Tarefa
        if "nome" in dados:
            existente.nome = dados["nome"]
        if "userName" in dados:
            existente.userName = dados["userName"]
        # adicione outros campos aqui, se necessário
        ok = self.pessoaDAO.atualizar(existente)
        return {"sucesso": bool(ok)}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deletarTarefa(self, id: int):
    
        try:
            tid = int(id)
        except (ValueError, TypeError):
            cherrypy.response.status = 400
            return {"sucesso": False, "erro": "ID inválido"}

        ok = self.tarefaDAO.deletar(tid)
        if not ok:
            cherrypy.response.status = 404
            return {"sucesso": False, "erro": "Tarefa não encontrada ou não pôde ser excluída"}

        return {"sucesso": True}
    

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deletarPessoa(self, id: int):
    
        try:
            tid = int(id)
        except (ValueError, TypeError):
            cherrypy.response.status = 400
            return {"sucesso": False, "erro": "ID inválido"}

        ok = self.pessoaDAO.deletarPessoa(tid)
        if not ok:
            cherrypy.response.status = 404
            return {"sucesso": False, "erro": "Usuário não encontrado ou não pôde ser excluída"}

        return {"sucesso": True}


    

    @cherrypy.expose
    @cherrypy.tools.json_in()   # lê JSON do corpo da requisição
    @cherrypy.tools.json_out()  # converte o retorno Python -> JSON
    def adicionarPessoa(self): #retorna o id inserido

        dados = cherrypy.request.json

        novaPessoa = Pessoa(
            userName = dados.get("userName"),
            nome = dados.get("nome")
        )

    
        
        if (len(novaPessoa.nome) > 0 and len(novaPessoa.userName)):
            
            novo_id = self.pessoaDAO.adicionarPessoa(novaPessoa)

            if (novo_id == "usuário existente"):
                cherrypy.response.status = 409
                return {"sucesso": False, "erro": "Usuário existente"}
            elif (novo_id):
                cherrypy.response.status = 201
                return {"id": novo_id}
            else:
                cherrypy.response.status = 500
                return {"sucesso": False, "erro": "Erro ao inserir"}
        else:
            cherrypy.response.status = 422
            return {"sucesso": False, "erro": "Você errou o valor de algum campo"}
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def buscarPessoa(self, userName: str):
        """
        Chamada GET: /buscarTarefa?userName=123
        Retorna JSON com os dados da tarefa ou um erro.
        """
        # O CherryPy recebe parâmetros de query string como strings, então convertendo
        try:
            pessoa_obj = self.pessoaDAO.buscarPessoa(userName)
            if pessoa_obj is None:
                cherrypy.response.status = 404
                return {"erro": "Usuário não encontrado"}
            # Supondo que pessoa_obj.__dict__ seja serializável diretamente
            return {"pessoa": pessoa_obj.__dict__}
        except ValueError:
            cherrypy.response.status = 400
            return {"erro": "Username inválido"}

def main():
    server = Server()

    despachante = cherrypy.dispatch.RoutesDispatcher()

    despachante.connect(name='adicionarTarefa', route='/tarefa', controller=server, 
                        action='adicionarTarefa', conditions=dict(method=['POST']))
    
    despachante.connect(name='buscartarefa', route='/tarefa/:id', controller=server, 
                        action='buscarTarefa', conditions=dict(method=['GET']))
    
    despachante.connect(name="buscarTarefas", route='/pessoa/:id/tarefas', controller=server,
                        action='listarTarefasPessoa', conditions=dict(method=['GET']))
    
    despachante.connect(name='buscarPessoa', route='/pessoa/:userName', controller=server, 
                        action='buscarPessoa', conditions=dict(method=['GET']))
    
    despachante.connect(name='adicionarPessoa', route='/pessoa', controller=server, 
                        action='adicionarPessoa', conditions=dict(method=['POST']))
    
    despachante.connect(name='atualizarTarefa', route='/tarefa', controller=server, 
                        action='atualizarTarefa', conditions=dict(method=['PATCH']))
    
    despachante.connect(name='deletarTarefa', route='/tarefa/:id', controller=server, 
                        action='deletarTarefa', conditions=dict(method=['DELETE']))
    
    despachante.connect(name='deletarPessoa', route='/pessoa/:id', controller=server, 
                        action='deletarPessoa', conditions=dict(method=['DELETE']))
    
    despachante.connect(name='atualizarPessoa', route='/pessoa', controller=server, 
                        action='atualizarPessoa', conditions=dict(method=['PATCH']))

    
    
    

    conf = {'/':{'request.dispatch':despachante}}
    cherrypy.tree.mount(root=None, config=conf)
    cherrypy.config.update({'server.socket_port':8083})
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    main()
