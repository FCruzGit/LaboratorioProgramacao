"""Painel de backup (admin)."""

import os
import zipfile
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "data.json")
BACKUP_DIR = os.path.dirname(DB_PATH)


def render_backup_panel(parent) -> None:
    ctk.CTkLabel(parent, text="Gerar Backup", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333333").pack(anchor="w", padx=30, pady=(20, 15))

    ctk.CTkLabel(
        parent, text="Clique no botão abaixo para gerar um backup do banco de dados.\nO arquivo será salvo na pasta database/.",
        font=ctk.CTkFont(size=14), text_color="#555555", justify="left",
    ).pack(anchor="w", padx=30, pady=(0, 20))

    status_label = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=13), text_color="#2E7D32")
    status_label.pack(anchor="w", padx=30, pady=(10, 0))

    def _gerar_backup():
        if not os.path.exists(DB_PATH):
            messagebox.showerror("Erro", "Arquivo de dados não encontrado.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"backup_{timestamp}.zip"
        zip_path = os.path.join(BACKUP_DIR, zip_name)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(DB_PATH, "data.json")

        status_label.configure(text=f"✓ Backup gerado: {zip_name}")
        messagebox.showinfo("Sucesso", f"Backup salvo em:\ndatabase/{zip_name}")

    ctk.CTkButton(
        parent, text="Gerar Backup", font=ctk.CTkFont(size=15, weight="bold"),
        fg_color="#1565C0", hover_color="#0D47A1", height=45, corner_radius=6,
        command=_gerar_backup,
    ).pack(anchor="w", padx=30)
