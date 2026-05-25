"""Módulo do popup de recuperação de senha."""

import os
import customtkinter as ctk
from tkinter import messagebox
from service.database_service import recover_password
from view.utils import center_window


ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sistema", "icon.ico")

BG_COLOR = "#DCE8F0"
CARD_COLOR = "#FFFFFF"
BTN_PRIMARY = "#1565C0"
TEXT_COLOR = "#1565C0"


class ForgotPasswordPopup(ctk.CTkToplevel):
    """Popup de recuperação de senha."""

    def __init__(self, master) -> None:
        super().__init__(master)

        self.title("Esqueci minha senha")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)
        self.grab_set()

        center_window(self, 520, 360)
        self.after(200, self._set_icon)
        self._build_ui()

    def _set_icon(self) -> None:
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

    def _build_ui(self) -> None:
        frame = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=20)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(
            frame, text="Recuperar Senha",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT_COLOR,
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(25, 15))

        campos = [
            ("Usuário", False),
            ("Nome da Mãe", True),
            ("Nova Senha", True),
            ("Confirmar Senha", True),
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

        # Botão recuperar
        btn_frame = ctk.CTkFrame(frame, fg_color=CARD_COLOR)
        btn_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=30, pady=(15, 20))

        ctk.CTkButton(
            btn_frame, text="Alterar Senha",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=BTN_PRIMARY, hover_color="#0D47A1",
            height=38, corner_radius=6, command=self._recuperar,
        ).pack(fill="x")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def _recuperar(self) -> None:
        usuario = self.entries["Usuário"].get().strip().lower()
        nome_mae = self.entries["Nome da Mãe"].get().strip().lower()
        nova_senha = self.entries["Nova Senha"].get().strip()
        confirmar = self.entries["Confirmar Senha"].get().strip()

        if not all([usuario, nome_mae, nova_senha, confirmar]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=self)
            return

        if nova_senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=self)
            return

        if recover_password(usuario, nome_mae, nova_senha):
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou nome da mãe incorretos.", parent=self)
