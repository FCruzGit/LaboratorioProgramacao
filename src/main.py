# src/main.py

from service.database_service import init_db
from view.home_window import HomeWindow


def main() -> None:
    """Ponto de entrada da aplicação."""
    init_db()
    app = HomeWindow()
    app.mainloop()

if __name__ == "__main__":
    main()