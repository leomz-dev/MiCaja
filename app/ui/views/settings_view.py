import customtkinter as ctk
from app.ui.theme import COLORS, SPACING


class SettingsView(ctk.CTkScrollableFrame):
    def __init__(self, master, controller, **_kwargs):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self, text="Ajustes", anchor="w",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 20))

        card = ctk.CTkFrame(
            self, fg_color=COLORS["bg_card"], corner_radius=SPACING["card_radius"],
        )
        card.pack(fill="x", pady=8)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=24, pady=24)

        config = self.controller.get_config()
        rows = [
            ("Nombre del negocio", config.get("NombreNegocio", "Mi Caja")),
            ("Moneda", config.get("Moneda", "$")),
            ("Versión", "2.0 — Rediseño UI"),
            ("Almacenamiento", "data/micaja_data.xlsx"),
        ]
        for label, value in rows:
            row = ctk.CTkFrame(inner, fg_color="transparent")
            row.pack(fill="x", pady=10)
            ctk.CTkLabel(
                row, text=label, width=180, anchor="w",
                font=ctk.CTkFont(size=13), text_color=COLORS["text_secondary"],
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=str(value), anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=COLORS["text_primary"],
            ).pack(side="left", padx=12)

        ctk.CTkLabel(
            inner,
            text="La edición de configuración avanzada estará disponible en una próxima fase.",
            font=ctk.CTkFont(size=12), text_color=COLORS["text_muted"],
            wraplength=500, justify="left",
        ).pack(anchor="w", pady=(16, 0))

    def refresh(self, **_kwargs):
        pass
