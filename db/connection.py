# db/banco.py
import mysql.connector
from db.config import * 

class Banco:
    def __init__(self):
        self.con = None
        try:
            # Conecta sem banco para criar o banco, se necessário
            con_temp = mysql.connector.connect(
                **DB_CONFIG_TEMP
            )

            if con_temp.is_connected():
                print("Conexão estabelecida com o servidor MySQL.")

            cursor = con_temp.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS `tarefa-db`")
            print("Banco de dados 'tarefa-db' criado (ou já existia).")
            cursor.close()
            con_temp.close()

            # Agora conecta diretamente no banco
            self.con = mysql.connector.connect(
                **DB_CONFIG
            )

            if self.con.is_connected():
                print("Conexão estabelecida com o banco de dados 'tarefa-db'.")
            cursor = self.con.cursor()


            comando_tabela0 = """

            CREATE TABLE IF NOT EXISTS `tarefa-db`.`tarefa` (
                `idTarefa` INT NOT NULL AUTO_INCREMENT,
                `nome` VARCHAR(100) NOT NULL,
                `descricao` VARCHAR(250) NOT NULL,
                `dataCriacao` INT NOT NULL,
                `dataTermino` INT NOT NULL,
                `status` TINYINT NULL DEFAULT 0,
                `dataDeTermino` VARCHAR(45) NULL,
                `idPessoa` INT NOT NULL,
                PRIMARY KEY (`idTarefa`),
                INDEX `fk_tarefa_Pessoa_idx` (`idPessoa` ASC) VISIBLE,
                CONSTRAINT `fk_tarefa_Pessoa`
                  FOREIGN KEY (`idPessoa`)
                  REFERENCES `tarefa-db`.`Pessoa` (`idPessoa`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION)
                ENGINE = InnoDB;

            
            """

            comando_tabela = """

            CREATE TABLE IF NOT EXISTS `tarefa-db`.`tarefa` (
                `idTarefa` INT NOT NULL AUTO_INCREMENT,
                `nome` VARCHAR(100) NOT NULL,
                `descricao` VARCHAR(250) NOT NULL,
                `dataCriacao` INT NOT NULL,
                `dataTermino` INT NOT NULL,
                `status` TINYINT NULL DEFAULT 0,
                `dataDeTermino` VARCHAR(45) NULL,
                `idPessoa` INT NOT NULL,
                PRIMARY KEY (`idTarefa`),
                INDEX `fk_tarefa_Pessoa_idx` (`idPessoa` ASC) VISIBLE,
                CONSTRAINT `fk_tarefa_Pessoa`
                  FOREIGN KEY (`idPessoa`)
                  REFERENCES `tarefa-db`.`Pessoa` (`idPessoa`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION)
                ENGINE = InnoDB;

            
            """
            cursor.execute(comando_tabela0)
            self.con.commit()
            cursor.execute(comando_tabela)
            self.con.commit()

            cursor.close()

        except mysql.connector.Error as err:
            print("erro foi aqui")
            print("Erro:", err)

    def get_conexao(self):
        return self.con
