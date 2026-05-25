"""Painel de consulta de notas (aluno)."""

import customtkinter as ctk
from service.database_service import get_user_subjects, get_teacher_for_subject


def _calc_media(notas: list) -> float:
    if not notas:
        return 0.0
    return sum(notas) / len(notas)


def render_consult_panel(parent, user: dict) -> None:
    ctk.CTkLabel(parent, text="Minhas Matérias", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    materias = get_user_subjects(user["usuario"])

    if not materias:
        ctk.CTkLabel(parent, text="Nenhuma matéria cadastrada.", font=ctk.CTkFont(size=15), text_color="#666666").pack(anchor="w", padx=30, pady=10)
        return

    container = ctk.CTkScrollableFrame(parent, fg_color="transparent", height=150)
    container.pack(fill="x", padx=20, pady=(0, 5))

    detail_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=12)
    detail_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    def _show_detail(materia):
        for w in detail_frame.winfo_children():
            w.destroy()

        professor = get_teacher_for_subject(materia["nome"], materia["turma"], materia["periodo"], materia["semestre"])

        # Info header
        info_frame = ctk.CTkFrame(detail_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(info_frame, text=f"{materia['nome']} — {materia['semestre']}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#333333").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Professor: {professor}  |  Turma: {materia['turma']}  |  Período: {materia['periodo']}", font=ctk.CTkFont(size=12), text_color="#666666").pack(anchor="w", pady=(2, 0))

        # Cards de notas
        cards_frame = ctk.CTkFrame(detail_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=(10, 5))

        notas = materia["notas"]
        tipos = [("AVI", "avi"), ("AVC", "avc"), ("AVG", "avg")]

        for i, (label, key) in enumerate(tipos):
            card = ctk.CTkFrame(cards_frame, fg_color="#F0F4F8", corner_radius=8, width=180, height=80)
            card.grid(row=0, column=i, padx=8, pady=5, sticky="nsew")
            card.pack_propagate(False)

            valores = notas.get(key, [])
            media = _calc_media(valores)

            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12, weight="bold"), text_color="#555555").pack(anchor="w", padx=10, pady=(8, 0))
            if valores:
                ctk.CTkLabel(card, text=", ".join(f"{v:.1f}" for v in valores), font=ctk.CTkFont(size=11), text_color="#777777").pack(anchor="w", padx=10)
                ctk.CTkLabel(card, text=f"Média: {media:.1f}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#333333").pack(anchor="w", padx=10)
            else:
                ctk.CTkLabel(card, text="Sem notas", font=ctk.CTkFont(size=12), text_color="#999999").pack(anchor="w", padx=10, pady=5)

        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)

        # Nota final (sempre /3)
        media_avi = _calc_media(notas.get("avi", []))
        media_avc = _calc_media(notas.get("avc", []))
        media_avg = _calc_media(notas.get("avg", []))
        nota_final = (media_avi + media_avc + media_avg) / 3

        aprovado = nota_final >= 7.0
        status_text = "APROVADO" if aprovado else "REPROVADO"
        status_color = "#2E7D32" if aprovado else "#C62828"

        result_frame = ctk.CTkFrame(detail_frame, fg_color="transparent")
        result_frame.pack(fill="x", padx=20, pady=(10, 15))
        ctk.CTkLabel(result_frame, text=f"Nota Final: {nota_final:.1f}", font=ctk.CTkFont(size=15, weight="bold"), text_color="#333333").pack(side="left")
        ctk.CTkLabel(result_frame, text=f"  —  {status_text}", font=ctk.CTkFont(size=15, weight="bold"), text_color=status_color).pack(side="left")

    for materia in materias:
        btn = ctk.CTkButton(
            container,
            text=f"{materia['nome']}  •  Turma {materia['turma']}  •  {materia['periodo']}  •  {materia['semestre']}",
            font=ctk.CTkFont(size=13), fg_color="#FFFFFF", text_color="#333333",
            hover_color="#E3F2FD", height=36, corner_radius=8, anchor="w",
            command=lambda m=materia: _show_detail(m),
        )
        btn.pack(fill="x", pady=2)

    _show_detail(materias[0])
