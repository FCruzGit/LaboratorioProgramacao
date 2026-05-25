"""Painel de vínculo professor-matéria (admin)."""

import customtkinter as ctk
from tkinter import messagebox
from service.database_service import (
    get_all_teachers, get_courses, get_teacher_subjects,
    assign_teacher_subject, remove_teacher_subject, TURMAS, PERIODOS
)


def render_assign_teacher_panel(parent) -> None:
    ctk.CTkLabel(parent, text="Vincular Professor", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    form = ctk.CTkFrame(parent, fg_color="transparent")
    form.pack(fill="x", padx=30)

    teachers = get_all_teachers()
    teacher_names = [t["nome_completo"] for t in teachers]
    courses = get_courses()
    course_names = [c["nome"] for c in courses]

    # Professor | Curso
    ctk.CTkLabel(form, text="Professor", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=0, column=0, sticky="w")
    teacher_var = ctk.StringVar(value=teacher_names[0] if teacher_names else "")
    ctk.CTkOptionMenu(form, values=teacher_names or ["Nenhum"], variable=teacher_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13), command=lambda _: _refresh_list()).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

    ctk.CTkLabel(form, text="Curso", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=0, column=1, sticky="w")
    course_var = ctk.StringVar(value=course_names[0] if course_names else "")

    # Matéria | Turma
    ctk.CTkLabel(form, text="Matéria", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=2, column=0, sticky="w")
    subject_var = ctk.StringVar(value="")
    subject_menu = ctk.CTkOptionMenu(form, values=[""], variable=subject_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13))
    subject_menu.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

    def _update_subjects(choice):
        for c in courses:
            if c["nome"] == choice:
                subs = c["subjects"]
                subject_menu.configure(values=subs or ["Nenhuma"])
                subject_var.set(subs[0] if subs else "")
                break

    ctk.CTkOptionMenu(form, values=course_names or ["Nenhum"], variable=course_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13), command=_update_subjects).grid(row=1, column=1, sticky="ew", pady=(0, 8))
    if courses:
        _update_subjects(course_names[0])

    ctk.CTkLabel(form, text="Turma", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=2, column=1, sticky="w")
    turma_var = ctk.StringVar(value=TURMAS[0])
    ctk.CTkOptionMenu(form, values=TURMAS, variable=turma_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13)).grid(row=3, column=1, sticky="ew", pady=(0, 8))

    # Período | Semestre
    ctk.CTkLabel(form, text="Período", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=4, column=0, sticky="w")
    periodo_var = ctk.StringVar(value=PERIODOS[0])
    ctk.CTkOptionMenu(form, values=PERIODOS, variable=periodo_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13)).grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

    from service.database_service import get_semesters
    semesters = get_semesters()
    ctk.CTkLabel(form, text="Semestre", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=4, column=1, sticky="w")
    semestre_var = ctk.StringVar(value=semesters[0] if semesters else "")
    ctk.CTkOptionMenu(form, values=semesters or [""], variable=semestre_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13)).grid(row=5, column=1, sticky="ew", pady=(0, 8))

    def _get_teacher_usuario():
        for t in teachers:
            if t["nome_completo"] == teacher_var.get():
                return t["usuario"]
        return None

    def _vincular():
        usuario = _get_teacher_usuario()
        if not usuario:
            messagebox.showwarning("Atenção", "Selecione um professor.")
            return
        if assign_teacher_subject(usuario, subject_var.get(), turma_var.get(), periodo_var.get(), semestre_var.get()):
            messagebox.showinfo("Sucesso", "Vínculo realizado!")
            _refresh_list()
        else:
            messagebox.showerror("Erro", "Vínculo já existe.")

    ctk.CTkButton(form, text="Vincular", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#1565C0", hover_color="#0D47A1", height=40, corner_radius=6, command=_vincular).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(8, 0))

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)

    # Lista de vínculos
    list_frame = ctk.CTkScrollableFrame(parent, fg_color="#FFFFFF", corner_radius=10, height=160)
    list_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

    def _refresh_list():
        for w in list_frame.winfo_children():
            w.destroy()
        usuario = _get_teacher_usuario()
        if not usuario:
            return
        vinculadas = get_teacher_subjects(usuario)
        if not vinculadas:
            ctk.CTkLabel(list_frame, text="Nenhum vínculo.", font=ctk.CTkFont(size=13), text_color="#999").pack(anchor="w", padx=10, pady=5)
            return
        for v in vinculadas:
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{v['materia']} — Turma {v['turma']} — {v['periodo']} — {v['semestre']}", font=ctk.CTkFont(size=13), text_color="#333").pack(side="left")

            def _rem(mat=v["materia"], t=v["turma"], p=v["periodo"], s=v["semestre"]):
                remove_teacher_subject(_get_teacher_usuario(), mat, t, p, s)
                _refresh_list()

            ctk.CTkButton(row, text="✕", width=30, height=28, fg_color="#C62828", hover_color="#B71C1C", corner_radius=4, font=ctk.CTkFont(size=12), command=_rem).pack(side="right")

    _refresh_list()
