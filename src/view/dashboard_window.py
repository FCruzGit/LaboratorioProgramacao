"""Módulo da tela principal do sistema."""

import os
import ctypes
import customtkinter as ctk
from view.utils import center_window

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("gestao_notas.app")

ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sistema", "icon.ico")

MENU_OPTIONS = {
    "user": ["Consultar"],
    "teacher": ["Lançar Notas", "Editar Notas", "Relatórios"],
    "admin": ["Matricular", "Vincular Professor", "Cursos", "Matérias", "Relatórios", "Backup"],
}


class DashboardWindow(ctk.CTkToplevel):
    """Tela principal com sidebar e painel de conteúdo."""

    SIDEBAR_COLOR = "#1565C0"
    SIDEBAR_HOVER = "#0D47A1"
    BG_COLOR = "#F0F4F8"
    TEXT_COLOR = "#FFFFFF"

    def __init__(self, master, user: dict) -> None:
        super().__init__(master)

        self.user = user
        self.master_window = master

        self.title("Sistema de Gestão de Notas")
        self.resizable(False, False)
        self.configure(fg_color=self.BG_COLOR)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        center_window(self, 1000, 600)
        self.after(200, self._set_icon)
        self._build_sidebar()
        self._build_content()

    def _set_icon(self) -> None:
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

    def _build_sidebar(self) -> None:
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=15, fg_color=self.SIDEBAR_COLOR)
        self.sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)
        self.sidebar.pack_propagate(False)

        # Título UNISA
        ctk.CTkLabel(
            self.sidebar,
            text="UNISA",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.TEXT_COLOR,
        ).pack(pady=(25, 5))

        # Saudação
        ctk.CTkLabel(
            self.sidebar,
            text=f"Olá, {self.user['nome_completo']}",
            font=ctk.CTkFont(size=13),
            text_color=self.TEXT_COLOR,
        ).pack(pady=(5, 20))

        # Opções do menu baseadas no tipo
        options = MENU_OPTIONS.get(self.user["tipo"], [])
        for option in options:
            btn = ctk.CTkButton(
                self.sidebar,
                text=option,
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                text_color=self.TEXT_COLOR,
                hover_color=self.SIDEBAR_HOVER,
                anchor="w",
                height=40,
                corner_radius=8,
                command=lambda opt=option: self._on_menu_click(opt),
            )
            btn.pack(fill="x", padx=10, pady=3)

        # Botão sair
        ctk.CTkButton(
            self.sidebar,
            text="Sair",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=self.TEXT_COLOR,
            hover_color="#B22222",
            anchor="w",
            height=40,
            corner_radius=8,
            command=self._on_close,
        ).pack(side="bottom", fill="x", padx=10, pady=20)

    def _build_content(self) -> None:
        self.content_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR, corner_radius=0)
        self.content_frame.pack(side="left", expand=True, fill="both")

        self._show_default_content()

    def _show_default_content(self) -> None:
        self._clear_content()
        ctk.CTkLabel(
            self.content_frame,
            text="Selecione uma opção para seguir",
            font=ctk.CTkFont(size=20),
            text_color="#666666",
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _clear_content(self) -> None:
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _on_menu_click(self, option: str) -> None:
        self._clear_content()
        if option == "Matricular":
            from view.panels.enroll_panel import render_enroll_panel
            render_enroll_panel(self.content_frame)
        elif option == "Lançar Notas":
            from view.panels.grades_panel import render_grades_panel
            render_grades_panel(self.content_frame)
        elif option == "Editar Notas":
            from view.panels.edit_grades_panel import render_edit_grades_panel
            render_edit_grades_panel(self.content_frame)
        elif option == "Consultar":
            from view.panels.consult_panel import render_consult_panel
            render_consult_panel(self.content_frame, self.user)
        elif option == "Cursos":
            from view.panels.courses_panel import render_courses_panel
            render_courses_panel(self.content_frame)
        elif option == "Matérias":
            from view.panels.subjects_panel import render_subjects_panel
            render_subjects_panel(self.content_frame)
        elif option == "Vincular Professor":
            from view.panels.assign_teacher_panel import render_assign_teacher_panel
            render_assign_teacher_panel(self.content_frame)
        elif option == "Relatórios":
            from view.panels.report_panel import render_report_panel
            render_report_panel(self.content_frame, self.user)
        elif option == "Backup":
            from view.panels.backup_panel import render_backup_panel
            render_backup_panel(self.content_frame)
        else:
            ctk.CTkLabel(
                self.content_frame,
                text=f"{option}",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color="#333333",
            ).place(relx=0.5, rely=0.5, anchor="center")

    def _on_close(self) -> None:
        self.destroy()
        self.master_window.deiconify()
