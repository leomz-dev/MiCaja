import customtkinter as ctk
from app.ui.theme import COLORS


class TypeBadge(ctk.CTkFrame):
    def __init__(self, master, tipo, **kwargs):
        is_ingreso = tipo == "Ingreso"
        fg = COLORS["primary_light"] if is_ingreso else COLORS["danger_light"]
        tc = COLORS["primary"] if is_ingreso else COLORS["danger"]
        label = "Ingreso" if is_ingreso else "Gasto"
        super().__init__(master, fg_color=fg, corner_radius=12, **kwargs)
        ctk.CTkLabel(
            self, text=label, font=ctk.CTkFont(size=11, weight="bold"),
            text_color=tc, padx=10, pady=2,
        ).pack()
