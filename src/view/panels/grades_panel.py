"""Painel de lançamento de notas (professor)."""

import customtkinter as ctk
from tkinter import messagebox
from service.database_service import get_all_students, get_user_subjects, update_grade


def render_grades_panel(parent) -> None:
    ctk.CTkLabel(parent, text="Lançar Notas", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    form = ctk.CTkFrame(parent, fg_color="transparent")
    form.pack(fill="x", padx=30)

    students = get_all_students()
    student_names = [s['nome_completo'] for s in students]
    student_var = ctk.StringVar(value=student_names[0] if student_names else "")

    ctk.CTkLabel(form, text="Aluno", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(form, text="Matéria", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=0, column=1, sticky="w")

    subject_var = ctk.StringVar(value="")
    subject_menu = ctk.CTkOptionMenu(form, values=["Selecione um aluno"], variable=subject_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13))
    subject_menu.grid(row=1, column=1, sticky="ew", pady=(0, 8))

    materias_aluno = []

    def _update_materias(choice):
        materias_aluno.clear()
        for s in students:
            if s['nome_completo'] == choice:
                materias_aluno.extend(get_user_subjects(s['usuario']))
                break
        if materias_aluno:
            nomes = [f"{m['nome']} | {m['turma']} | {m['periodo']} | {m['semestre']}" for m in materias_aluno]
            subject_menu.configure(values=nomes)
            subject_var.set(nomes[0])
            _update_notas_display()
        else:
            subject_menu.configure(values=["Sem matérias"])
            subject_var.set("Sem matérias")

    ctk.CTkOptionMenu(form, values=student_names or ["Nenhum"], variable=student_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13), command=_update_materias).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

    ctk.CTkLabel(form, text="Tipo de Nota", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=2, column=0, sticky="w")
    tipo_nota_var = ctk.StringVar(value="avi")
    ctk.CTkOptionMenu(form, values=["avi", "avc", "avg"], variable=tipo_nota_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13), command=lambda _: _update_notas_display()).grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

    ctk.CTkLabel(form, text="Nota", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=2, column=1, sticky="w")
    nota_entry = ctk.CTkEntry(form, height=35, fg_color="#F0F0F0", border_width=0, corner_radius=4, font=ctk.CTkFont(size=13), placeholder_text="Ex: 7.5")
    nota_entry.grid(row=3, column=1, sticky="ew", pady=(0, 8))

    def _get_selected_materia():
        sel = subject_var.get()
        for m in materias_aluno:
            label = f"{m['nome']} | {m['turma']} | {m['periodo']} | {m['semestre']}"
            if label == sel:
                return m
        return None

    def _lancar():
        sel_student = student_var.get()
        if not sel_student or sel_student == "Nenhum":
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        m = _get_selected_materia()
        if not m:
            messagebox.showwarning("Atenção", "Selecione uma matéria.")
            return
        nota_text = nota_entry.get().strip()
        if not nota_text:
            messagebox.showwarning("Atenção", "Informe a nota.")
            return
        try:
            nova_nota = float(nota_text)
        except ValueError:
            messagebox.showerror("Erro", "A nota deve ser um valor numérico.")
            return
        if nova_nota < 0 or nova_nota > 10:
            messagebox.showerror("Erro", "A nota deve ser entre 0 e 10.")
            return

        tipo = tipo_nota_var.get()
        notas_atuais = m["notas"].get(tipo, [])
        notas_atuais.append(nova_nota)
        usuario = None
        for s in students:
            if s['nome_completo'] == sel_student:
                usuario = s['usuario']
                break
        if usuario and update_grade(usuario, m["nome"], m["semestre"], m["turma"], m["periodo"], tipo, notas_atuais):
            m["notas"][tipo] = notas_atuais
            nota_entry.delete(0, "end")
            messagebox.showinfo("Sucesso", f"Nota {nova_nota} lançada!")
            _update_notas_display()
        else:
            messagebox.showerror("Erro", "Falha ao lançar nota.")

    ctk.CTkButton(form, text="Lançar Nota", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#1565C0", hover_color="#0D47A1", height=40, corner_radius=6, command=_lancar).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))
    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)

    notas_display_label = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=13), text_color="#555555")
    notas_display_label.pack(anchor="w", padx=30, pady=(15, 0))

    def _update_notas_display():
        m = _get_selected_materia()
        tipo = tipo_nota_var.get()
        if m:
            valores = m["notas"].get(tipo, [])
            txt = f"Notas lançadas ({tipo.upper()}): " + (" | ".join(f"{v:.1f}" for v in valores) if valores else "Nenhuma")
            notas_display_label.configure(text=txt)
        else:
            notas_display_label.configure(text="")

    subject_menu.configure(command=lambda _: _update_notas_display())
    if student_names:
        _update_materias(student_names[0])
