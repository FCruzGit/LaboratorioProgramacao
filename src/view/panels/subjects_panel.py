"""Painel de gerenciamento de matérias (admin)."""

import customtkinter as ctk
from tkinter import messagebox
from service.database_service import get_courses, add_subject, rename_subject, remove_subject


def render_subjects_panel(parent) -> None:
    """Renderiza o painel de gerenciamento de matérias."""
    ctk.CTkLabel(
        parent, text="Gerenciar Matérias",
        font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333",
    ).pack(anchor="w", padx=30, pady=(20, 15))

    # Selecionar curso
    top_frame = ctk.CTkFrame(parent, fg_color="transparent")
    top_frame.pack(fill="x", padx=30, pady=(0, 5))

    ctk.CTkLabel(top_frame, text="Curso", font=ctk.CTkFont(size=13), text_color="#333333").pack(anchor="w")
    courses = get_courses()
    course_names = [c["nome"] for c in courses]
    course_var = ctk.StringVar(value=course_names[0] if course_names else "")

    # Criar matéria
    create_frame = ctk.CTkFrame(parent, fg_color="transparent")
    create_frame.pack(fill="x", padx=30, pady=(0, 10))

    ctk.CTkLabel(create_frame, text="Nova Matéria", font=ctk.CTkFont(size=13), text_color="#333333").pack(anchor="w")
    new_entry = ctk.CTkEntry(
        create_frame, height=35, fg_color="#F0F0F0", border_width=0,
        corner_radius=4, font=ctk.CTkFont(size=13), placeholder_text="Nome da matéria",
    )
    new_entry.pack(side="left", fill="x", expand=True, pady=(3, 0), padx=(0, 10))

    # Lista de matérias
    list_frame = ctk.CTkScrollableFrame(parent, fg_color="#FFFFFF", corner_radius=10, height=250)
    list_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

    def _refresh_list():
        for w in list_frame.winfo_children():
            w.destroy()

        curso_sel = course_var.get()
        courses_data = get_courses()
        subjects = []
        for c in courses_data:
            if c["nome"] == curso_sel:
                subjects = c["subjects"]
                break

        if not subjects:
            ctk.CTkLabel(
                list_frame, text="Nenhuma matéria cadastrada.",
                font=ctk.CTkFont(size=13), text_color="#999999",
            ).pack(anchor="w", padx=10, pady=5)
            return

        for subj in subjects:
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=3)

            entry = ctk.CTkEntry(
                row, height=32, fg_color="#F0F4F8", border_width=0,
                corner_radius=4, font=ctk.CTkFont(size=13),
            )
            entry.insert(0, subj)
            entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

            def _rename(e=entry, old=subj):
                novo = e.get().strip()
                if novo and novo != old:
                    if rename_subject(course_var.get(), old, novo):
                        messagebox.showinfo("Sucesso", f"Matéria renomeada para '{novo}'!")
                        _refresh_list()
                    else:
                        messagebox.showerror("Erro", "Falha ao renomear.")

            ctk.CTkButton(
                row, text="Salvar", width=60, height=30,
                font=ctk.CTkFont(size=11), fg_color="#1565C0", hover_color="#0D47A1",
                corner_radius=4, command=_rename,
            ).pack(side="left", padx=(0, 5))

            def _remove(nome=subj):
                if remove_subject(course_var.get(), nome):
                    _refresh_list()

            ctk.CTkButton(
                row, text="✕", width=30, height=30,
                font=ctk.CTkFont(size=12), fg_color="#C62828", hover_color="#B71C1C",
                corner_radius=4, command=_remove,
            ).pack(side="left")

    def _criar():
        nome = new_entry.get().strip()
        curso = course_var.get()
        if not nome:
            messagebox.showwarning("Atenção", "Informe o nome da matéria.")
            return
        if not curso:
            messagebox.showwarning("Atenção", "Selecione um curso.")
            return
        if add_subject(curso, nome):
            messagebox.showinfo("Sucesso", f"Matéria '{nome}' adicionada!")
            new_entry.delete(0, "end")
            _refresh_list()
        else:
            messagebox.showerror("Erro", "Matéria já existe neste curso.")

    ctk.CTkButton(
        create_frame, text="Criar", width=80, height=35,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color="#1565C0", hover_color="#0D47A1", corner_radius=6,
        command=_criar,
    ).pack(side="left", pady=(3, 0))

    ctk.CTkOptionMenu(
        top_frame, values=course_names if course_names else ["Nenhum curso"],
        variable=course_var, width=300, height=35,
        fg_color="#F0F0F0", button_color="#D0D0D0", text_color="#333333",
        corner_radius=4, font=ctk.CTkFont(size=13),
        command=lambda _: _refresh_list(),
    ).pack(anchor="w", pady=(3, 0))

    _refresh_list()
