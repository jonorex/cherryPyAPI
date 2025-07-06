


class Pessoa:
    
    def __init__(self, 
                  idPessoa = None,
                   userName = "", 
                   nome=""):
        
        self.idPessoa = idPessoa
        self.userName = userName
        self.nome = nome
    
    
    def __str__(self):
        return (
            f"Tarefa:\n"
            f"  idPessoa: {self.idPessoa}\n"
            f"  userName: {self.userName}\n"
            f"  nome: {self.nome}\n"
        )