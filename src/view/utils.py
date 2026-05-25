"""Utilitários e constantes compartilhadas das views."""

import os

ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sistema", "icon.ico")

BG_COLOR = "#DCE8F0"
CARD_COLOR = "#FFFFFF"
BTN_PRIMARY = "#1565C0"
BTN_SECONDARY = "#616161"
TEXT_COLOR = "#1565C0"


def center_window(window, width: int, height: int) -> None:
    """Centraliza uma janela na tela."""
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
