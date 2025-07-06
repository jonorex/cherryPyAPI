from model.pessoa import Pessoa
from db.connection import Banco
from model.tarefa import Tarefa


class PessoaDAO:
    def __init__(self, conexao):
        
        self.pessoa = Pessoa()

        

        

        self.con = conexao

    
    def adicionarPessoa(self, pessoa):
        
        if (self.buscarPessoa(pessoa.userName)):
            return "usuário existente"
        
        sql = """
            INSERT INTO PESSOA (USERNAME, NOME) VALUES (%s, %s)
        """
        

        cursor = self.con.cursor()

        cursor.execute(sql, (
            pessoa.userName, 
            pessoa.nome))
        
        self.con.commit()
        pessoa.idPessoa = cursor.lastrowid
        cursor.close()

        if (pessoa.idPessoa == None): pessoa.idPessoa = 0

        return pessoa.idPessoa 

    def buscarPessoa(self, userName):
        cursor = self.con.cursor()

        cursor.execute("SELECT * FROM pessoa WHERE userName = %s ", (userName,))

        result = cursor.fetchone()
        pessoa = None
        if result:
            pessoa =  Pessoa(*result)
        cursor.close()

        print(f"linha 91 {result}")
        return pessoa
    

    def buscarPessoaId(self, id):
        cursor = self.con.cursor()

        cursor.execute("SELECT * FROM pessoa WHERE idPessoa = %s ", (id,))

        result = cursor.fetchone()
        pessoa = None
        if result:
            pessoa =  Pessoa(*result)
        cursor.close()

        print(f"linha 91 {result}")
        return pessoa

    def buscarTarefas(self, idPessoa):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM tarefa WHERE idPessoa = %s", (idPessoa,))

        # Consome o resultado primeiro
        result = cursor.fetchall()

        print(result)

        objetos = [Tarefa(*tarefa) for tarefa in result]

        cursor.close()

        return objetos

    def deletarPessoa(self, id):
        cursor =  self.con.cursor()
        cursor.execute("DELETE FROM pessoa WHERE idPessoa = %s", (id,))
        
        self.con.commit()
        if (cursor.rowcount > 0):
            return True
        return False
    

    def atualizar(self, pessoa: Pessoa):
    
        sql = "update pessoa set "
        fields = []  

        if pessoa.userName:
            sql += "userName = %s, "
            fields.append(pessoa.userName)
        if pessoa.nome:
            sql += "nome = %s, "
            fields.append(pessoa.nome)
        
        # Remova a vírgula final se existir
        if sql.endswith(", "):
            sql = sql[:-2]
        sql += " where idPessoa = %s"
        fields.append(pessoa.idPessoa)
        
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
