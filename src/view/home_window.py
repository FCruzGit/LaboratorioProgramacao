"""Módulo da tela inicial (login) do sistema."""

import os
import ctypes
import customtkinter as ctk
from PIL import Image
from view.register_popup import RegisterPopup
from view.forgot_password_popup import ForgotPasswordPopup
from view.dashboard_window import DashboardWindow
from view.utils import center_window, ICON_PATH, BG_COLOR, CARD_COLOR, BTN_PRIMARY, BTN_SECONDARY, TEXT_COLOR
from service.database_service import authenticate

# Faz o ícone aparecer na barra de tarefas do Windows
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("gestao_notas.app")


class HomeWindow(ctk.CTk):
    """Tela de login do sistema de gestão de notas."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Sistema de Gestão de Notas")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)

        ctk.set_appearance_mode("light")

        center_window(self, 900, 600)
        self._set_icon()
        self._build_ui()

    def _set_icon(self) -> None:
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

    def _build_ui(self) -> None:
        # Frame esquerdo (formulário de login)
        self.login_frame = ctk.CTkFrame(
            self, width=420, height=520, fg_color=CARD_COLOR, corner_radius=20
        )
        self.login_frame.place(x=30, y=40)
        self.login_frame.pack_propagate(False)

        # Título "Entrar"
        ctk.CTkLabel(
            self.login_frame,
            text="Entrar",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=TEXT_COLOR,
        ).pack(anchor="w", padx=40, pady=(40, 30))

        # Campo Usuário
        ctk.CTkLabel(
            self.login_frame,
            text="Usuário",
            font=ctk.CTkFont(size=14),
            text_color="#333333",
        ).pack(anchor="w", padx=40)

        self.entry_usuario = ctk.CTkEntry(
            self.login_frame,
            height=45,
            fg_color="#F0F0F0",
            border_width=0,
            corner_radius=4,
            font=ctk.CTkFont(size=14),
        )
        self.entry_usuario.pack(fill="x", padx=40, pady=(5, 20))

        # Campo Senha
        ctk.CTkLabel(
            self.login_frame,
            text="Senha",
            font=ctk.CTkFont(size=14),
            text_color="#333333",
        ).pack(anchor="w", padx=40)

        self.entry_senha = ctk.CTkEntry(
            self.login_frame,
            height=45,
            fg_color="#F0F0F0",
            border_width=0,
            corner_radius=4,
            font=ctk.CTkFont(size=14),
            show="*",
        )
        self.entry_senha.pack(fill="x", padx=40, pady=(5, 30))

        # Botão Entrar
        ctk.CTkButton(
            self.login_frame,
            text="Entrar",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=BTN_PRIMARY,
            hover_color="#0D47A1",
            height=45,
            corner_radius=6,
            command=self._on_login,
        ).pack(fill="x", padx=40, pady=(0, 10))

        # Botão Cadastrar-se
        ctk.CTkButton(
            self.login_frame,
            text="Cadastrar-se",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=BTN_SECONDARY,
            hover_color="#424242",
            height=45,
            corner_radius=6,
            command=self._on_cadastro,
        ).pack(fill="x", padx=40, pady=(0, 10))

        # Link "Esqueci minha senha"
        forgot_label = ctk.CTkLabel(
            self.login_frame,
            text="Esqueci minha senha",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_COLOR,
            cursor="hand2",
        )
        forgot_label.pack(pady=(5, 0))
        forgot_label.bind("<Button-1>", lambda e: self._on_forgot_password())

        # Imagem à direita
        img_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "assets", "sistema", "inicio.png"
        )
        if os.path.exists(img_path):
            img = Image.open(img_path)
            self.home_image = ctk.CTkImage(light_image=img, dark_image=img, size=(350, 350))
            img_label = ctk.CTkLabel(self, image=self.home_image, text="", fg_color=BG_COLOR)
            img_label.place(x=500, y=130)

    def _on_login(self) -> None:
        """Ação ao clicar em Entrar."""
        from tkinter import messagebox

        usuario = self.entry_usuario.get().strip().lower()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        user = authenticate(usuario, senha)
        if user:
            self.withdraw()
            DashboardWindow(self, user)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def _on_cadastro(self) -> None:
        """Abre popup de cadastro."""
        RegisterPopup(self)

    def _on_forgot_password(self) -> None:
        """Abre popup de recuperação de senha."""
        ForgotPasswordPopup(self)
