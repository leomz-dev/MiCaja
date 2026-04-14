import customtkinter as ctk
from app.controllers.main_controller import MainController
from app.ui.main_window import MainWindow

def main():
    # Estética de la aplicación
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    controller = MainController()
    app = MainWindow(controller)
    app.mainloop()

if __name__ == "__main__":
    main()
