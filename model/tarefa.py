


class Tarefa: 
    def __init__(self,
                 idTarefa = None, 
                 nome = "", 
                 descricao = "", 
                 dataCriacao = None,
                 dataTermino = None, 
                 status = None,
                 dataDeTermino = None, 
                 idPessoa = None
                 ):

        # Inicializa os atributos com valores padrão
        self.idTarefa = idTarefa
        self.nome = nome
        self.descricao = descricao
        self.dataTermino = dataTermino
        self.dataDeTermino = dataDeTermino
        self.status = status
        self.dataCriacao = dataCriacao
        self.idPessoa = idPessoa


        

    def iniciar_tarefa(self, mensagem):

        campos = mensagem.split('#')

        

        for campo in campos:
            campo = campo.split(':')
            chave = campo[0]
            valor = campo[1]

            if hasattr(self, chave):
                if chave in self.camposInt:
                    try:
                        valor = int(valor)
                    except:
                        pass
                    
                setattr(self, chave, valor)
    def __str__(self):
        return (
            f"Tarefa:\n"
            f"  idTarefa: {self.idTarefa}\n"
            f"  Nome: {self.nome}\n"
            f"  Descrição: {self.descricao}\n"
            f"  Data Término: {self.dataTermino}\n"
            f"  Data de Término: {self.dataDeTermino}\n"
            f"  Status: {self.status}\n"
            f"  Data de Criação: {self.dataCriacao}"
        )

    def to_dict(self):
        return {
        'idTarefa': self.idTarefa,
        'nome': self.nome,
        'descricao': self.descricao,
        'dataCriacao': self.dataCriacao,
        'dataTermino': self.dataTermino,
        'status': self.status,
        'dataDeTermino': self.dataDeTermino
    }

def converterParaDicionario(objeto: Tarefa):

    return {
        '__class__': 'tarefa.Tarefa',
        'idTarefa': objeto.idTarefa,
        'nome': objeto.nome,
        'descricao': objeto.descricao,
        'dataCriacao': objeto.dataCriacao,
        'dataTermino': objeto.dataTermino,
        'status': objeto.status,
        'dataDeTermino': objeto.dataDeTermino
        
    }

def converterParaObjeto(classname, dicionario: dict):

    tarefa = Tarefa(dicionario['idTarefa'], dicionario['nome'], dicionario['descricao'], dicionario['dataCriacao'], dicionario['dataTermino'], dicionario['status'], dicionario['dataDeTermino'])

    return tarefa