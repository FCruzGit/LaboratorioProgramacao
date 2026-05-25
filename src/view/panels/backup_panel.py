"""Painel de backup (admin)."""

import customtkinter as ctk
from tkinter import messagebox
from service.backup_service import generate_backup


def render_backup_panel(parent) -> None:
    ctk.CTkLabel(parent, text="Gerar Backup", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    ctk.CTkLabel(
        parent, text="Clique no botão abaixo para gerar um backup do banco de dados.\nO arquivo será salvo na pasta database/.",
        font=ctk.CTkFont(size=14), text_color="#555555", justify="left",
    ).pack(anchor="w", padx=30, pady=(0, 20))

    status_label = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=13), text_color="#2E7D32")
    status_label.pack(anchor="w", padx=30, pady=(10, 0))

    def _gerar_backup():
        zip_name = generate_backup()
        if zip_name:
            status_label.configure(text=f"✓ Backup gerado: {zip_name}")
            messagebox.showinfo("Sucesso", f"Backup salvo em:\ndatabase/{zip_name}")
        else:
            messagebox.showerror("Erro", "Arquivo de dados não encontrado.")

    ctk.CTkButton(
        parent, text="Gerar Backup", font=ctk.CTkFont(size=15, weight="bold"),
        fg_color="#1565C0", hover_color="#0D47A1", height=45, corner_radius=6,
        command=_gerar_backup,
    ).pack(anchor="w", padx=30)
