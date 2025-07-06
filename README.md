## API CherryPy

### Descrição do Projeto
Implementação de uma API REST em CherryPy para gerenciamento de tarefas associadas a usuários. O serviço inclui operações de **CRUD** (criação, leitura, atualização e deleção) tanto para **pessoas** quanto para **tarefas**, com validações de entrada e respostas em JSON.

### Banco de Dados
- **SGBD:** MySQL  
- Tabelas:
  - `Pessoa`  
  - `Tarefa` (com chave estrangeira `idPessoa` → `Pessoa.idPessoa`)  
- A classe de conexão (`Banco`) cria automaticamente o banco e as tabelas, se necessários.

### Padrão de Projeto
- **DAO (Data Access Object):**  
  - `PessoaDAO` e `TarefaDAO` encapsulam toda a lógica de acesso ao MySQL.  
  - Métodos: `inserir()`, `buscar()`, `atualizar()`, `deletar()`.  
- **Entities:**  
  - `Pessoa` e `Tarefa` modelam as colunas do banco como atributos de classe.  
- **Server:**  
  - Configura o dispatcher de rotas do CherryPy e orquestra chamadas aos DAOs usando uma conexão única compartilhada.

### Endpoints Disponíveis

| Método   | Rota                        | Ação                                       | Códigos de Resposta           |
|:--------:|:----------------------------|:-------------------------------------------|:------------------------------|
| **POST** | `/tarefa`                   | Cria nova tarefa                           | 200, 404, 422                 |
| **GET**  | `/tarefa/:id`               | Retorna tarefa por ID                      | 200, 400, 404                 |
| **GET**  | `/pessoa/:id/tarefas`       | Lista tarefas de uma pessoa                | 200, 500                      |
| **PATCH**| `/tarefa`                   | Atualiza campos de uma tarefa              | 200, 400, 404                 |
| **DELETE**| `/tarefa/:id`              | Exclui tarefa por ID                       | 200, 400, 404                 |
| **POST** | `/pessoa`                   | Cria nova pessoa (`userName` único)        | 201, 409, 422, 500            |
| **GET**  | `/pessoa/:userName`         | Busca pessoa por `userName`                | 200, 400, 404                 |
| **PATCH**| `/pessoa`                   | Atualiza dados de uma pessoa               | 200, 400, 404                 |
| **DELETE**| `/pessoa/:id`              | Exclui pessoa por ID                       | 200, 400, 404                 |

---
