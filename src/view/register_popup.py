"""Módulo do popup de cadastro."""

import os
import customtkinter as ctk
from tkinter import messagebox
from service.database_service import register_user, user_exists
from view.utils import center_window


ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sistema", "icon.ico")

BG_COLOR = "#DCE8F0"
CARD_COLOR = "#FFFFFF"
BTN_PRIMARY = "#1565C0"
TEXT_COLOR = "#1565C0"


class RegisterPopup(ctk.CTkToplevel):
    """Popup de cadastro de usuário."""

    def __init__(self, master) -> None:
        super().__init__(master)

        self.title("Cadastrar-se")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)
        self.grab_set()

        center_window(self, 520, 450)
        self.after(200, self._set_icon)
        self._build_ui()

    def _set_icon(self) -> None:
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

    def _build_ui(self) -> None:
        frame = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=20)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(
            frame, text="Cadastrar-se",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT_COLOR,
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(25, 15))

        # Campos em grid 2 colunas
        campos = [
            ("Usuário", False),
            ("Nome Completo", False),
            ("Email", False),
            ("Senha", True),
            ("Nome da Mãe", True),
        ]

        self.entries = {}
        row = 1
        col = 0
        for campo, oculto in campos:
            container = ctk.CTkFrame(frame, fg_color=CARD_COLOR)
            container.grid(row=row, column=col, sticky="ew", padx=(30 if col == 0 else 10, 10 if col == 0 else 30), pady=6)

            ctk.CTkLabel(
                container, text=campo, font=ctk.CTkFont(size=12), text_color="#333333"
            ).pack(anchor="w")

            entry = ctk.CTkEntry(
                container, height=38, fg_color="#F0F0F0", border_width=0,
                corner_radius=4, font=ctk.CTkFont(size=13),
                show="*" if oculto else "",
            )
            entry.pack(fill="x", pady=(3, 0))
            self.entries[campo] = entry

            col += 1
            if col > 1:
                col = 0
                row += 1

        # Campo Tipo (dropdown) — ao lado de Nome da Mãe
        tipo_container = ctk.CTkFrame(frame, fg_color=CARD_COLOR)
        tipo_container.grid(row=row, column=col, sticky="ew", padx=(10, 30), pady=6)

        ctk.CTkLabel(
            tipo_container, text="Tipo", font=ctk.CTkFont(size=12), text_color="#333333"
        ).pack(anchor="w")

        self.tipo_var = ctk.StringVar(value="Usuário")
        self.tipo_menu = ctk.CTkOptionMenu(
            tipo_container,
            values=["Usuário", "Professor"],
            variable=self.tipo_var,
            height=38,
            fg_color="#F0F0F0",
            button_color="#D0D0D0",
            button_hover_color="#B0B0B0",
            text_color="#333333",
            corner_radius=4,
            font=ctk.CTkFont(size=13),
        )
        self.tipo_menu.pack(fill="x", pady=(3, 0))

        row += 1

        # Botão cadastrar abaixo
        ctk.CTkButton(
            frame, text="Cadastrar",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=BTN_PRIMARY, hover_color="#0D47A1",
            height=42, corner_radius=6, command=self._cadastrar,
        ).grid(row=row, column=0, columnspan=2, sticky="ew", padx=30, pady=(15, 20))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def _cadastrar(self) -> None:
        usuario = self.entries["Usuário"].get().strip().lower()
        nome = self.entries["Nome Completo"].get().strip()
        email = self.entries["Email"].get().strip().lower()
        senha = self.entries["Senha"].get().strip()
        nome_mae = self.entries["Nome da Mãe"].get().strip().lower()
        tipo = "user" if self.tipo_var.get() == "Usuário" else "teacher"

        if not all([usuario, nome, email, senha, nome_mae]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=self)
            return

        if user_exists(usuario):
            messagebox.showerror("Erro", "Usuário já existe.", parent=self)
            return

        register_user(usuario, nome, email, senha, nome_mae, tipo)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!", parent=self)
        self.destroy()
