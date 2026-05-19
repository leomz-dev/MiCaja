import customtkinter as ctk
from app.ui.theme import COLORS, SPACING, FONTS


class KpiCard(ctk.CTkFrame):
    def __init__(
        self, master, title, value="", subtitle="", icon="",
        value_color=None, accent_icon_bg=None, **kwargs,
    ):
        super().__init__(
            master,
            fg_color=COLORS["bg_card"],
            corner_radius=SPACING["card_radius"],
            **kwargs,
        )
        self.grid_columnconfigure(0, weight=1)
        value_color = value_color or COLORS["text_primary"]
        accent_icon_bg = accent_icon_bg or COLORS["bg_card_alt"]

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 0))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text=title.upper(), anchor="w",
            font=ctk.CTkFont(family=FONTS["kpi_label"][0], size=11, weight="bold"),
            text_color=COLORS["text_secondary"],
        ).grid(row=0, column=0, sticky="w")

        if icon:
            icon_box = ctk.CTkFrame(
                header, width=36, height=36, corner_radius=8,
                fg_color=accent_icon_bg,
            )
            icon_box.grid(row=0, column=1)
            icon_box.pack_propagate(False)
            ctk.CTkLabel(
                icon_box, text=icon, font=ctk.CTkFont(size=16),
                text_color=value_color,
            ).place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_value = ctk.CTkLabel(
            self, text=value, anchor="w",
            font=ctk.CTkFont(family=FONTS["kpi_value"][0], size=26, weight="bold"),
            text_color=value_color,
        )
        self.lbl_value.grid(row=1, column=0, sticky="w", padx=20, pady=(8, 0))

        self.lbl_subtitle = ctk.CTkLabel(
            self, text=subtitle, anchor="w",
            font=ctk.CTkFont(size=12), text_color=COLORS["text_secondary"],
        )
        self.lbl_subtitle.grid(row=2, column=0, sticky="w", padx=20, pady=(4, 18))

    def update(self, value, subtitle=None, value_color=None):
        self.lbl_value.configure(text=value)
        if subtitle is not None:
            self.lbl_subtitle.configure(text=subtitle)
        if value_color:
            self.lbl_value.configure(text_color=value_color)
