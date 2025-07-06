import requests
from model.tarefa import Tarefa
import json
import time
from model.pessoa import Pessoa
# Base URL of the CherryPy server
BASE_URL = "http://127.0.0.1:8083"

# -------------------------
# Pessoa (Person) Endpoints
# -------------------------

def add_person(user_name: str, nome: str) -> dict:
    """
    Adiciona uma nova pessoa no sistema.

    Args:
        user_name (str): Nome de usuário único.
        nome (str): Nome completo da pessoa.

    Returns:
        dict: JSON contendo o ID da pessoa criada ou mensagem de erro.
    """
    url = f"{BASE_URL}/pessoa"
    payload = {"userName": user_name, "nome": nome}
    response = requests.post(url, json=payload)
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}

    
    return data
    

def get_person(user_name: str) -> dict:
    """
    Busca os dados de uma pessoa pelo userName.

    Args:
        user_name (str): Nome de usuário da pessoa.

    Returns:
        dict: JSON com os dados da pessoa ou mensagem de erro.
    """
    url = f"{BASE_URL}/pessoa/{user_name}"
    response = requests.get(url)
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}
    print(f"person {data}")
    
    return data


# -------------------------
# Tarefa (Task) Endpoints
# -------------------------

def add_task(tarefa) -> dict:
    """
    Adiciona uma nova tarefa no sistema.

    Args:
        nome (str): Nome da tarefa.
        descricao (str): Descrição da tarefa.
        data_termino (float): Timestamp (em segundos) da data de término.
        id_pessoa (int): ID da pessoa responsável pela tarefa.

    Returns:
        dict: JSON contendo o ID da tarefa criada ou mensagem de erro.
    """
    url = f"{BASE_URL}/tarefa"
    payload = {
        "nome": tarefa.nome,
        "descricao": tarefa.descricao,
        "dataTermino": tarefa.dataTermino,
        "idPessoa": tarefa.idPessoa,
    }
    print(f"payload 82 {payload}")
    response = requests.post(url, json=payload)
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}

    
    return data


def get_task(task_id: int) -> dict:
    """
    Busca uma tarefa pelo seu ID.

    Args:
        task_id (int): ID da tarefa.

    Returns:
        dict: JSON com os dados da tarefa ou mensagem de erro.
    """
    url = f"{BASE_URL}/tarefa/{task_id}"
    response = requests.get(url)
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}

    if response.status_code == 200:
        return data
    else:
        raise requests.HTTPError(f"Erro ao buscar tarefa: {data.get('erro', response.text)}")


def list_person_tasks(person_id: int) -> dict:
    """
    Lista todas as tarefas associadas a uma pessoa.

    Args:
        person_id (int): ID da pessoa.

    Returns:
        dict: JSON com a lista de tarefas ou mensagem de erro.
    """

    url = f"{BASE_URL}/pessoa/{person_id}/tarefas"
    response = requests.get(url)
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}
    if response.status_code == 200:
        tarefas_list = data.get("tarefas", [])
        task_list = [Tarefa(**tarefa_dict) for tarefa_dict in tarefas_list]
        return task_list
    else:
        return []


def update_task(tarefa):
    url = f"{BASE_URL}/tarefa"
    response = requests.patch(url, json=tarefa.__dict__)  
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}

    
    return data


def delete_task(id):
    url = f"{BASE_URL}/tarefa/{id}"
    response = requests.patch(url)

    response = requests.delete(url)
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}

    return data.get("sucesso")


def update_pessoa(pessoa):
    url = f"{BASE_URL}/pessoa"
    response = requests.patch(url, json=pessoa.__dict__)  
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}

    
    return data

def delete_pessoa(id):
    url = f"{BASE_URL}/pessoa/{id}"
    response = requests.patch(url)

    response = requests.delete(url)
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        return {}

    return data.get("sucesso")
