"""Painel de matrícula (admin)."""

import customtkinter as ctk
from tkinter import messagebox
from service.database_service import (
    get_all_students, get_courses, get_semesters, enroll_subject, TURMAS, PERIODOS
)


def render_enroll_panel(parent) -> None:
    ctk.CTkLabel(parent, text="Matricular Aluno", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    form = ctk.CTkFrame(parent, fg_color="transparent")
    form.pack(fill="x", padx=30)

    students = get_all_students()
    student_names = [s['nome_completo'] for s in students]
    courses = get_courses()
    course_names = [c["nome"] for c in courses]
    semesters = get_semesters()

    # Row 0: Aluno | Curso
    ctk.CTkLabel(form, text="Aluno", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=0, column=0, sticky="w")
    student_var = ctk.StringVar(value=student_names[0] if student_names else "")
    ctk.CTkOptionMenu(form, values=student_names or ["Nenhum"], variable=student_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13)).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

    ctk.CTkLabel(form, text="Curso", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=0, column=1, sticky="w")
    course_var = ctk.StringVar(value=course_names[0] if course_names else "")

    # Row 2: Matéria | Semestre
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

    ctk.CTkLabel(form, text="Semestre", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=2, column=1, sticky="w")
    semester_var = ctk.StringVar(value=semesters[0] if semesters else "")
    ctk.CTkOptionMenu(form, values=semesters or [""], variable=semester_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13)).grid(row=3, column=1, sticky="ew", pady=(0, 8))

    # Row 4: Turma | Período
    ctk.CTkLabel(form, text="Turma", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=4, column=0, sticky="w")
    turma_var = ctk.StringVar(value=TURMAS[0])
    ctk.CTkOptionMenu(form, values=TURMAS, variable=turma_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13)).grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

    ctk.CTkLabel(form, text="Período", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=4, column=1, sticky="w")
    periodo_var = ctk.StringVar(value=PERIODOS[0])
    ctk.CTkOptionMenu(form, values=PERIODOS, variable=periodo_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13)).grid(row=5, column=1, sticky="ew", pady=(0, 8))

    def _matricular():
        sel = student_var.get()
        if not sel or sel == "Nenhum":
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        usuario = None
        for s in students:
            if s['nome_completo'] == sel:
                usuario = s['usuario']
                break
        if not usuario:
            return
        if enroll_subject(usuario, subject_var.get(), semester_var.get(), turma_var.get(), periodo_var.get()):
            messagebox.showinfo("Sucesso", "Matrícula realizada!")
        else:
            messagebox.showerror("Erro", "Aluno já matriculado nesta combinação.")

    ctk.CTkButton(form, text="Matricular", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#1565C0", hover_color="#0D47A1", height=40, corner_radius=6, command=_matricular).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 0))

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)
