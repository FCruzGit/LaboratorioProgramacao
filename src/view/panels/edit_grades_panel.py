"""Painel de edição de notas (professor)."""

import customtkinter as ctk
from tkinter import messagebox
from service.database_service import get_all_students, get_user_subjects, update_grade


def render_edit_grades_panel(parent) -> None:
    ctk.CTkLabel(parent, text="Editar Notas", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    form = ctk.CTkFrame(parent, fg_color="transparent")
    form.pack(fill="x", padx=30)

    students = get_all_students()
    student_names = [s['nome_completo'] for s in students]
    student_var = ctk.StringVar(value=student_names[0] if student_names else "")

    ctk.CTkLabel(form, text="Aluno", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(form, text="Matéria", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=0, column=1, sticky="w")

    subject_var = ctk.StringVar(value="")
    subject_menu = ctk.CTkOptionMenu(form, values=["Selecione"], variable=subject_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13))
    subject_menu.grid(row=1, column=1, sticky="ew", pady=(0, 8))

    ctk.CTkLabel(form, text="Tipo de Nota", font=ctk.CTkFont(size=13), text_color="#333333").grid(row=2, column=0, sticky="w", columnspan=2)
    tipo_nota_var = ctk.StringVar(value="avi")
    ctk.CTkOptionMenu(form, values=["avi", "avc", "avg"], variable=tipo_nota_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13), command=lambda _: _load_notas()).grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)

    materias_aluno = []

    notas_frame = ctk.CTkScrollableFrame(parent, fg_color="#FFFFFF", corner_radius=10, height=180)
    notas_frame.pack(fill="x", padx=30, pady=(10, 10))

    entries_list = []

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
            _load_notas()
        else:
            subject_menu.configure(values=["Sem matérias"])
            subject_var.set("Sem matérias")
            for w in notas_frame.winfo_children():
                w.destroy()

    ctk.CTkOptionMenu(form, values=student_names or ["Nenhum"], variable=student_var, height=35, fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333", corner_radius=4, font=ctk.CTkFont(size=13), command=_update_materias).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
    subject_menu.configure(command=lambda _: _load_notas())

    def _get_selected_materia():
        sel = subject_var.get()
        for m in materias_aluno:
            if f"{m['nome']} | {m['turma']} | {m['periodo']} | {m['semestre']}" == sel:
                return m
        return None

    def _load_notas():
        nonlocal entries_list
        for w in notas_frame.winfo_children():
            w.destroy()
        entries_list.clear()
        m = _get_selected_materia()
        if not m:
            return
        valores = m["notas"].get(tipo_nota_var.get(), [])
        if not valores:
            ctk.CTkLabel(notas_frame, text="Nenhuma nota.", font=ctk.CTkFont(size=13), text_color="#999").pack(anchor="w", padx=10, pady=5)
            return
        for i, valor in enumerate(valores):
            row = ctk.CTkFrame(notas_frame, fg_color="transparent")
            row.pack(fill="x", pady=3, padx=5)
            ctk.CTkLabel(row, text=f"Nota {i+1}:", font=ctk.CTkFont(size=13), text_color="#333", width=60).pack(side="left", padx=(0, 5))
            entry = ctk.CTkEntry(row, height=32, width=100, fg_color="#F0F0F0", border_width=0, corner_radius=4, font=ctk.CTkFont(size=13))
            entry.insert(0, str(valor))
            entry.pack(side="left", padx=(0, 10))
            entries_list.append(entry)

            def _remove(idx=i):
                m2 = _get_selected_materia()
                if m2:
                    notas = m2["notas"].get(tipo_nota_var.get(), [])
                    if 0 <= idx < len(notas):
                        notas.pop(idx)
                        usuario = None
                        for s in students:
                            if s['nome_completo'] == student_var.get():
                                usuario = s['usuario']
                                break
                        if usuario:
                            update_grade(usuario, m2["nome"], m2["semestre"], m2["turma"], m2["periodo"], tipo_nota_var.get(), notas)
                            m2["notas"][tipo_nota_var.get()] = notas
                            _load_notas()

            ctk.CTkButton(row, text="✕", width=30, height=30, fg_color="#C62828", hover_color="#B71C1C", font=ctk.CTkFont(size=12), corner_radius=4, command=_remove).pack(side="left")

    def _salvar():
        m = _get_selected_materia()
        if not m:
            return
        novas = []
        for entry in entries_list:
            try:
                nota = float(entry.get().strip())
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos.")
                return
            if nota < 0 or nota > 10:
                messagebox.showerror("Erro", f"Nota {nota} inválida (0-10).")
                return
            novas.append(nota)
        usuario = None
        for s in students:
            if s['nome_completo'] == student_var.get():
                usuario = s['usuario']
                break
        if usuario and update_grade(usuario, m["nome"], m["semestre"], m["turma"], m["periodo"], tipo_nota_var.get(), novas):
            m["notas"][tipo_nota_var.get()] = novas
            messagebox.showinfo("Sucesso", "Notas atualizadas!")
            _load_notas()

    ctk.CTkButton(parent, text="Salvar Alterações", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#1565C0", hover_color="#0D47A1", height=40, corner_radius=6, command=_salvar).pack(fill="x", padx=30, pady=(5, 15))

    if student_names:
        _update_materias(student_names[0])
