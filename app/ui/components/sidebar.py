import customtkinter as ctk
from app.ui.theme import COLORS, SPACING, FONTS, NAV_ITEMS


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, app_name, on_navigate, on_new_operation, **kwargs):
        super().__init__(
            master,
            width=SPACING["sidebar_width"],
            fg_color=COLORS["bg_sidebar"],
            corner_radius=0,
            **kwargs,
        )
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.on_new_operation = on_new_operation
        self._nav_buttons = {}
        self._active_key = "dashboard"

        self._build_brand(app_name)
        self._build_nav()
        self._build_footer()

    def _build_brand(self, app_name):
        brand = ctk.CTkFrame(self, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(28, 24))

        icon = ctk.CTkLabel(
            brand, text="$", font=ctk.CTkFont(size=28),
            text_color=COLORS["primary"], width=36,
        )
        icon.pack(side="left")

        texts = ctk.CTkFrame(brand, fg_color="transparent")
        texts.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(
            texts, text=app_name, anchor="w",
            font=ctk.CTkFont(family=FONTS["title"][0], size=18, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            texts, text="Gestión Financiera", anchor="w",
            font=ctk.CTkFont(size=12), text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

    def _build_nav(self):
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="x", padx=12, pady=(0, 8))

        for key, icon, label in NAV_ITEMS:
            btn = ctk.CTkButton(
                nav,
                text=f"  {icon}   {label}",
                anchor="w",
                height=44,
                corner_radius=8,
                fg_color="transparent",
                hover_color=COLORS["bg_card"],
                text_color=COLORS["text_secondary"],
                font=ctk.CTkFont(size=14),
                command=lambda k=key: self.set_active(k, navigate=True),
            )
            btn.pack(fill="x", pady=2)
            self._nav_buttons[key] = btn

        self._highlight("dashboard")

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=16, pady=24)

        ctk.CTkButton(
            footer,
            text="+  Nueva Operación",
            height=48,
            corner_radius=SPACING["btn_radius"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["primary_light"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_new_operation,
        ).pack(fill="x", pady=(0, 16))

        ctk.CTkButton(
            footer,
            text="  ⎋  Cerrar Sesión",
            height=36,
            corner_radius=8,
            fg_color="transparent",
            hover_color=COLORS["bg_card"],
            text_color=COLORS["text_muted"],
            font=ctk.CTkFont(size=13),
            anchor="w",
            command=lambda: self.winfo_toplevel().destroy(),
        ).pack(fill="x")

    def _highlight(self, key):
        self._active_key = key
        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=COLORS["sidebar_active_bg"],
                    text_color=COLORS["primary"],
                    border_width=0,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                )

    def set_active(self, key, navigate=True):
        self._highlight(key)
        if navigate:
            self.on_navigate(key)
