from tkinter import ttk
from app.ui.theme import COLORS


def configure_treeview(style_name="MiCaja.Treeview"):
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        style_name,
        background=COLORS["tree_bg"],
        foreground=COLORS["text_primary"],
        fieldbackground=COLORS["tree_bg"],
        borderwidth=0,
        rowheight=36,
        font=("Inter", 11),
    )
    style.map(style_name, background=[("selected", COLORS["tree_selected"])])
    style.configure(
        f"{style_name}.Heading",
        background=COLORS["tree_heading"],
        foreground=COLORS["text_secondary"],
        relief="flat",
        font=("Inter", 10, "bold"),
    )
    return style_name
