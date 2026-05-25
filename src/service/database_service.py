"""Serviço de gerenciamento do banco de dados JSON."""

import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "database", "data.json")


def _default_data() -> dict:
    """Retorna a estrutura padrão do banco de dados."""
    semesters = []
    for year in range(2015, 2036):
        semesters.append(f"{year}.1")
        semesters.append(f"{year}.2")

    courses = [
        {
            "nome": "Psicologia",
            "subjects": [
                "Psicologia Geral",
                "Neurociência",
                "Psicologia do Desenvolvimento",
                "Psicopatologia",
                "Psicologia Social",
                "Teorias da Personalidade",
                "Avaliação Psicológica",
                "Psicologia Clínica",
                "Psicologia Organizacional",
                "Ética Profissional",
            ],
        },
        {
            "nome": "Medicina",
            "subjects": [
                "Anatomia Humana",
                "Fisiologia",
                "Bioquímica",
                "Farmacologia",
                "Patologia",
                "Semiologia Médica",
                "Clínica Médica",
                "Cirurgia Geral",
                "Saúde Pública",
                "Ética Médica",
            ],
        },
        {
            "nome": "Filosofia",
            "subjects": [
                "Introdução à Filosofia",
                "Lógica",
                "Ética",
                "Filosofia Política",
                "Metafísica",
                "Epistemologia",
                "Estética",
                "Filosofia da Linguagem",
                "História da Filosofia Antiga",
                "História da Filosofia Moderna",
            ],
        },
        {
            "nome": "Análise e Desenvolvimento de Sistemas",
            "subjects": [
                "Lógica de Programação",
                "Estrutura de Dados",
                "Banco de Dados",
                "Engenharia de Software",
                "Programação Orientada a Objetos",
                "Desenvolvimento Web",
                "Redes de Computadores",
                "Sistemas Operacionais",
                "Segurança da Informação",
                "Projeto Integrador",
            ],
        },
    ]

    return {
        "users": [
            {
                "usuario": "admin",
                "nome_completo": "Administrador",
                "email": "admin@sistema.com",
                "senha": "admin",
                "nome_mae": "admin",
                "tipo": "admin",
            }
        ],
        "system": {
            "semesters": semesters,
            "courses": courses,
        },
    }


def init_db() -> None:
    """Inicializa o arquivo JSON caso não exista."""
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        _save(_default_data())


def _load() -> dict:
    """Carrega os dados do JSON."""
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    """Salva os dados no JSON."""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def user_exists(usuario: str) -> bool:
    """Verifica se um usuário já existe."""
    data = _load()
    return any(u["usuario"] == usuario for u in data["users"])


def register_user(usuario: str, nome_completo: str, email: str, senha: str, nome_mae: str, tipo: str = "user") -> bool:
    """Cadastra um novo usuário. Retorna False se já existir."""
    if user_exists(usuario):
        return False
    data = _load()
    data["users"].append({
        "usuario": usuario,
        "nome_completo": nome_completo,
        "email": email,
        "senha": senha,
        "nome_mae": nome_mae,
        "tipo": tipo,
    })
    _save(data)
    return True


def recover_password(usuario: str, nome_mae: str, nova_senha: str) -> bool:
    """Recupera a senha validando o nome da mãe. Retorna False se inválido."""
    data = _load()
    for user in data["users"]:
        if user["usuario"] == usuario and user["nome_mae"] == nome_mae:
            user["senha"] = nova_senha
            _save(data)
            return True
    return False


def authenticate(usuario: str, senha: str) -> dict | None:
    """Autentica o usuário. Retorna os dados do usuário ou None."""
    data = _load()
    for user in data["users"]:
        if user["usuario"] == usuario and user["senha"] == senha:
            return user
    return None
