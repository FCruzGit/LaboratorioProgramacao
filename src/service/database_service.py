"""Serviço de gerenciamento do banco de dados JSON."""

import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "database", "data.json")

TURMAS = ["A", "B", "C"]
PERIODOS = ["Manhã", "Noturno"]


def _default_data() -> dict:
    semesters = []
    for year in range(2015, 2036):
        semesters.append(f"{year}.1")
        semesters.append(f"{year}.2")

    courses = [
        {"nome": "Psicologia", "subjects": ["Psicologia Geral", "Neurociência", "Psicologia do Desenvolvimento", "Psicopatologia", "Psicologia Social", "Teorias da Personalidade", "Avaliação Psicológica", "Psicologia Clínica", "Psicologia Organizacional", "Ética Profissional"]},
        {"nome": "Medicina", "subjects": ["Anatomia Humana", "Fisiologia", "Bioquímica", "Farmacologia", "Patologia", "Semiologia Médica", "Clínica Médica", "Cirurgia Geral", "Saúde Pública", "Ética Médica"]},
        {"nome": "Filosofia", "subjects": ["Introdução à Filosofia", "Lógica", "Ética", "Filosofia Política", "Metafísica", "Epistemologia", "Estética", "Filosofia da Linguagem", "História da Filosofia Antiga", "História da Filosofia Moderna"]},
        {"nome": "Análise e Desenvolvimento de Sistemas", "subjects": ["Lógica de Programação", "Estrutura de Dados", "Banco de Dados", "Engenharia de Software", "Programação Orientada a Objetos", "Desenvolvimento Web", "Redes de Computadores", "Sistemas Operacionais", "Segurança da Informação", "Projeto Integrador"]},
    ]

    return {
        "users": [{"usuario": "admin", "nome_completo": "Administrador", "email": "admin@sistema.com", "senha": "admin", "nome_mae": "admin", "tipo": "admin"}],
        "system": {"semesters": semesters, "courses": courses},
    }


def init_db() -> None:
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        _save(_default_data())


def _load() -> dict:
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# === Usuários ===

def user_exists(usuario: str) -> bool:
    data = _load()
    return any(u["usuario"] == usuario for u in data["users"])


def register_user(usuario: str, nome_completo: str, email: str, senha: str, nome_mae: str, tipo: str = "user") -> bool:
    if user_exists(usuario):
        return False
    data = _load()
    data["users"].append({"usuario": usuario, "nome_completo": nome_completo, "email": email, "senha": senha, "nome_mae": nome_mae, "tipo": tipo})
    _save(data)
    return True


def recover_password(usuario: str, nome_mae: str, nova_senha: str) -> bool:
    data = _load()
    for user in data["users"]:
        if user["usuario"] == usuario and user["nome_mae"] == nome_mae:
            user["senha"] = nova_senha
            _save(data)
            return True
    return False


def authenticate(usuario: str, senha: str) -> dict | None:
    data = _load()
    for user in data["users"]:
        if user["usuario"] == usuario and user["senha"] == senha:
            return user
    return None


def get_users_by_type(tipo: str) -> list:
    data = _load()
    return [u for u in data["users"] if u["tipo"] == tipo]


def get_all_students() -> list:
    return get_users_by_type("user")


def get_all_teachers() -> list:
    return get_users_by_type("teacher")


# === Sistema ===

def get_courses() -> list:
    return _load()["system"]["courses"]


def get_semesters() -> list:
    return _load()["system"]["semesters"]


def add_course(nome: str) -> bool:
    data = _load()
    if any(c["nome"].lower() == nome.lower() for c in data["system"]["courses"]):
        return False
    data["system"]["courses"].append({"nome": nome, "subjects": []})
    _save(data)
    return True


def rename_course(nome_antigo: str, nome_novo: str) -> bool:
    data = _load()
    for c in data["system"]["courses"]:
        if c["nome"] == nome_antigo:
            c["nome"] = nome_novo
            _save(data)
            return True
    return False


def remove_course(nome: str) -> bool:
    data = _load()
    courses = data["system"]["courses"]
    for i, c in enumerate(courses):
        if c["nome"] == nome:
            courses.pop(i)
            _save(data)
            return True
    return False


def add_subject(curso: str, materia: str) -> bool:
    data = _load()
    for c in data["system"]["courses"]:
        if c["nome"] == curso:
            if materia.lower() in [s.lower() for s in c["subjects"]]:
                return False
            c["subjects"].append(materia)
            _save(data)
            return True
    return False


def rename_subject(curso: str, nome_antigo: str, nome_novo: str) -> bool:
    data = _load()
    for c in data["system"]["courses"]:
        if c["nome"] == curso:
            for i, s in enumerate(c["subjects"]):
                if s == nome_antigo:
                    c["subjects"][i] = nome_novo
                    _save(data)
                    return True
    return False


def remove_subject(curso: str, materia: str) -> bool:
    data = _load()
    for c in data["system"]["courses"]:
        if c["nome"] == curso:
            if materia in c["subjects"]:
                c["subjects"].remove(materia)
                _save(data)
                return True
    return False


# === Matrícula (aluno) ===

def enroll_subject(usuario: str, materia: str, semestre: str, turma: str, periodo: str) -> bool:
    data = _load()
    for user in data["users"]:
        if user["usuario"] == usuario:
            if "materias" not in user:
                user["materias"] = []
            for m in user["materias"]:
                if m["nome"] == materia and m["semestre"] == semestre and m["turma"] == turma and m["periodo"] == periodo:
                    return False
            user["materias"].append({
                "nome": materia, "semestre": semestre, "turma": turma, "periodo": periodo,
                "notas": {"avi": [], "avc": [], "avg": []},
            })
            _save(data)
            return True
    return False


def get_user_subjects(usuario: str) -> list:
    data = _load()
    for user in data["users"]:
        if user["usuario"] == usuario:
            return user.get("materias", [])
    return []


def update_grade(usuario: str, materia: str, semestre: str, turma: str, periodo: str, tipo_nota: str, notas: list) -> bool:
    data = _load()
    for user in data["users"]:
        if user["usuario"] == usuario:
            for m in user.get("materias", []):
                if m["nome"] == materia and m["semestre"] == semestre and m["turma"] == turma and m["periodo"] == periodo:
                    m["notas"][tipo_nota] = notas
                    _save(data)
                    return True
    return False


# === Vínculo professor ===

def assign_teacher_subject(professor_usuario: str, materia: str, turma: str, periodo: str, semestre: str) -> bool:
    data = _load()
    for user in data["users"]:
        if user["usuario"] == professor_usuario and user["tipo"] == "teacher":
            if "materias_vinculadas" not in user:
                user["materias_vinculadas"] = []
            for v in user["materias_vinculadas"]:
                if v["materia"] == materia and v["turma"] == turma and v["periodo"] == periodo and v["semestre"] == semestre:
                    return False
            user["materias_vinculadas"].append({"materia": materia, "turma": turma, "periodo": periodo, "semestre": semestre})
            _save(data)
            return True
    return False


def remove_teacher_subject(professor_usuario: str, materia: str, turma: str, periodo: str, semestre: str) -> bool:
    data = _load()
    for user in data["users"]:
        if user["usuario"] == professor_usuario and user["tipo"] == "teacher":
            vinculadas = user.get("materias_vinculadas", [])
            for i, v in enumerate(vinculadas):
                if v["materia"] == materia and v["turma"] == turma and v["periodo"] == periodo and v["semestre"] == semestre:
                    vinculadas.pop(i)
                    _save(data)
                    return True
    return False


def get_teacher_subjects(professor_usuario: str) -> list:
    """Retorna lista de dicts: [{'materia', 'turma', 'periodo', 'semestre'}]"""
    data = _load()
    for user in data["users"]:
        if user["usuario"] == professor_usuario:
            return user.get("materias_vinculadas", [])
    return []


def get_teacher_for_subject(materia: str, turma: str, periodo: str, semestre: str) -> str:
    """Retorna o nome do professor vinculado a uma matéria/turma/período/semestre."""
    data = _load()
    for user in data["users"]:
        if user["tipo"] == "teacher":
            for v in user.get("materias_vinculadas", []):
                if v["materia"] == materia and v["turma"] == turma and v["periodo"] == periodo and v["semestre"] == semestre:
                    return user["nome_completo"]
    return "Não definido"


# === Relatórios ===

def get_report_for_subject(materia: str, turma: str, periodo: str, semestre: str) -> dict:
    data = _load()
    todas_notas = []
    alunos = 0

    for user in data["users"]:
        if user["tipo"] != "user":
            continue
        for m in user.get("materias", []):
            if m["nome"] == materia and m["turma"] == turma and m["periodo"] == periodo and m["semestre"] == semestre:
                alunos += 1
                for tipo in ["avi", "avc", "avg"]:
                    todas_notas.extend(m["notas"].get(tipo, []))

    if not todas_notas:
        return {"media": 0.0, "maior": 0.0, "menor": 0.0, "total_alunos": alunos}

    return {
        "media": sum(todas_notas) / len(todas_notas),
        "maior": max(todas_notas),
        "menor": min(todas_notas),
        "total_alunos": alunos,
    }


def get_admin_report() -> dict:
    data = _load()
    courses = data["system"]["courses"]
    total_cursos = len(courses)
    total_materias = sum(len(c["subjects"]) for c in courses)

    materias_stats = []
    for course in courses:
        for subject in course["subjects"]:
            aprovados = 0
            reprovados = 0
            for user in data["users"]:
                if user["tipo"] != "user":
                    continue
                for m in user.get("materias", []):
                    if m["nome"] == subject:
                        notas = m["notas"]
                        media_avi = sum(notas.get("avi", [])) / len(notas["avi"]) if notas.get("avi") else 0.0
                        media_avc = sum(notas.get("avc", [])) / len(notas["avc"]) if notas.get("avc") else 0.0
                        media_avg = sum(notas.get("avg", [])) / len(notas["avg"]) if notas.get("avg") else 0.0
                        final = (media_avi + media_avc + media_avg) / 3
                        if final >= 6.0:
                            aprovados += 1
                        else:
                            reprovados += 1
            if aprovados > 0 or reprovados > 0:
                materias_stats.append({"curso": course["nome"], "materia": subject, "aprovados": aprovados, "reprovados": reprovados})

    return {"total_cursos": total_cursos, "total_materias": total_materias, "materias_stats": materias_stats}
