"""Painel de relatórios (professor/admin)."""

import customtkinter as ctk
from service.database_service import get_teacher_subjects, get_report_for_subject, get_admin_report


def render_report_panel(parent, user: dict) -> None:
    if user["tipo"] == "admin":
        _render_admin_report(parent)
    else:
        _render_teacher_report(parent, user)


def _render_admin_report(parent) -> None:
    ctk.CTkLabel(parent, text="Relatório Geral", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    report = get_admin_report()

    totals_frame = ctk.CTkFrame(parent, fg_color="transparent")
    totals_frame.pack(fill="x", padx=30, pady=(0, 15))

    for i, (label, value) in enumerate([("Total de Cursos", str(report["total_cursos"])), ("Total de Matérias", str(report["total_materias"]))]):
        card = ctk.CTkFrame(totals_frame, fg_color="#FFFFFF", corner_radius=10, width=200, height=70)
        card.grid(row=0, column=i, padx=8, sticky="nsew")
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12), text_color="#777777").pack(anchor="w", padx=15, pady=(10, 0))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=20, weight="bold"), text_color="#1565C0").pack(anchor="w", padx=15)

    totals_frame.grid_columnconfigure(0, weight=1)
    totals_frame.grid_columnconfigure(1, weight=1)

    if not report["materias_stats"]:
        ctk.CTkLabel(parent, text="Nenhum dado de aprovação/reprovação disponível.", font=ctk.CTkFont(size=14), text_color="#666666").pack(anchor="w", padx=30, pady=10)
        return

    ctk.CTkLabel(parent, text="Aprovados / Reprovados por Matéria", font=ctk.CTkFont(size=16, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(5, 8))

    container = ctk.CTkScrollableFrame(parent, fg_color="#FFFFFF", corner_radius=10, height=280)
    container.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    header = ctk.CTkFrame(container, fg_color="#F0F4F8", corner_radius=4)
    header.pack(fill="x", pady=(0, 5))
    ctk.CTkLabel(header, text="Curso", font=ctk.CTkFont(size=12, weight="bold"), text_color="#555", width=180).pack(side="left", padx=10)
    ctk.CTkLabel(header, text="Matéria", font=ctk.CTkFont(size=12, weight="bold"), text_color="#555", width=180).pack(side="left", padx=10)
    ctk.CTkLabel(header, text="Aprovados", font=ctk.CTkFont(size=12, weight="bold"), text_color="#2E7D32", width=80).pack(side="left", padx=10)
    ctk.CTkLabel(header, text="Reprovados", font=ctk.CTkFont(size=12, weight="bold"), text_color="#C62828", width=80).pack(side="left", padx=10)

    for stat in report["materias_stats"]:
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=stat["curso"], font=ctk.CTkFont(size=12), text_color="#333", width=180).pack(side="left", padx=10)
        ctk.CTkLabel(row, text=stat["materia"], font=ctk.CTkFont(size=12), text_color="#333", width=180).pack(side="left", padx=10)
        ctk.CTkLabel(row, text=str(stat["aprovados"]), font=ctk.CTkFont(size=12, weight="bold"), text_color="#2E7D32", width=80).pack(side="left", padx=10)
        ctk.CTkLabel(row, text=str(stat["reprovados"]), font=ctk.CTkFont(size=12, weight="bold"), text_color="#C62828", width=80).pack(side="left", padx=10)


def _render_teacher_report(parent, user: dict) -> None:
    ctk.CTkLabel(parent, text="Relatórios", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    vinculos = get_teacher_subjects(user["usuario"])

    if not vinculos:
        ctk.CTkLabel(parent, text="Nenhuma matéria vinculada ao seu perfil.", font=ctk.CTkFont(size=15), text_color="#666666").pack(anchor="w", padx=30, pady=10)
        return

    container = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    for v in vinculos:
        report = get_report_for_subject(v["materia"], v["turma"], v["periodo"], v["semestre"])

        card = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=12)
        card.pack(fill="x", pady=6, padx=5)

        ctk.CTkLabel(card, text=f"{v['materia']} — Turma {v['turma']} — {v['periodo']} — {v['semestre']}", font=ctk.CTkFont(size=15, weight="bold"), text_color="#1565C0").pack(anchor="w", padx=20, pady=(12, 5))

        stats_frame = ctk.CTkFrame(card, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=(0, 12))

        stats = [
            ("Alunos", str(report["total_alunos"])),
            ("Média Geral", f"{report['media']:.1f}"),
            ("Maior Nota", f"{report['maior']:.1f}"),
            ("Menor Nota", f"{report['menor']:.1f}"),
        ]

        for i, (label, value) in enumerate(stats):
            stat_box = ctk.CTkFrame(stats_frame, fg_color="#F0F4F8", corner_radius=8, width=130, height=60)
            stat_box.grid(row=0, column=i, padx=5, pady=3, sticky="nsew")
            stat_box.pack_propagate(False)
            ctk.CTkLabel(stat_box, text=label, font=ctk.CTkFont(size=11), text_color="#777777").pack(anchor="w", padx=10, pady=(8, 0))
            ctk.CTkLabel(stat_box, text=value, font=ctk.CTkFont(size=15, weight="bold"), text_color="#333333").pack(anchor="w", padx=10)

        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
        stats_frame.grid_columnconfigure(3, weight=1)
