"""Painel de gerenciamento de cursos (admin)."""

import customtkinter as ctk
from tkinter import messagebox
from service.database_service import get_courses, add_course, rename_course, remove_course


def render_courses_panel(parent) -> None:
    """Renderiza o painel de gerenciamento de cursos."""
    ctk.CTkLabel(
        parent, text="Gerenciar Cursos",
        font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333",
    ).pack(anchor="w", padx=30, pady=(20, 15))

    # Criar curso
    create_frame = ctk.CTkFrame(parent, fg_color="transparent")
    create_frame.pack(fill="x", padx=30, pady=(0, 10))

    ctk.CTkLabel(create_frame, text="Novo Curso", font=ctk.CTkFont(size=13), text_color="#333333").pack(anchor="w")
    new_entry = ctk.CTkEntry(
        create_frame, height=35, fg_color="#F0F0F0", border_width=0,
        corner_radius=4, font=ctk.CTkFont(size=13), placeholder_text="Nome do curso",
    )
    new_entry.pack(side="left", fill="x", expand=True, pady=(3, 0), padx=(0, 10))

    def _criar():
        nome = new_entry.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Informe o nome do curso.")
            return
        if add_course(nome):
            messagebox.showinfo("Sucesso", f"Curso '{nome}' criado!")
            new_entry.delete(0, "end")
            _refresh_list()
        else:
            messagebox.showerror("Erro", "Curso já existe.")

    ctk.CTkButton(
        create_frame, text="Criar", width=80, height=35,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color="#1565C0", hover_color="#0D47A1", corner_radius=6,
        command=_criar,
    ).pack(side="left", pady=(3, 0))

    # Lista de cursos
    list_frame = ctk.CTkScrollableFrame(parent, fg_color="#FFFFFF", corner_radius=10, height=300)
    list_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

    def _refresh_list():
        for w in list_frame.winfo_children():
            w.destroy()

        courses = get_courses()
        for course in courses:
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=3)

            entry = ctk.CTkEntry(
                row, height=32, fg_color="#F0F4F8", border_width=0,
                corner_radius=4, font=ctk.CTkFont(size=13),
            )
            entry.insert(0, course["nome"])
            entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

            def _rename(e=entry, old=course["nome"]):
                novo = e.get().strip()
                if novo and novo != old:
                    if rename_course(old, novo):
                        messagebox.showinfo("Sucesso", f"Curso renomeado para '{novo}'!")
                        _refresh_list()
                    else:
                        messagebox.showerror("Erro", "Falha ao renomear.")

            ctk.CTkButton(
                row, text="Salvar", width=60, height=30,
                font=ctk.CTkFont(size=11), fg_color="#1565C0", hover_color="#0D47A1",
                corner_radius=4, command=_rename,
            ).pack(side="left", padx=(0, 5))

            def _remove(nome=course["nome"]):
                if remove_course(nome):
                    _refresh_list()

            ctk.CTkButton(
                row, text="✕", width=30, height=30,
                font=ctk.CTkFont(size=12), fg_color="#C62828", hover_color="#B71C1C",
                corner_radius=4, command=_remove,
            ).pack(side="left")

    _refresh_list()
