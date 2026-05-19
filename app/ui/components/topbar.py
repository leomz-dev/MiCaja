import customtkinter as ctk
from datetime import datetime
from app.ui.theme import COLORS, FONTS, PERIOD_OPTIONS


class TopBar(ctk.CTkFrame):
    def __init__(self, master, user_name, on_search, on_period_change, **kwargs):
        super().__init__(master, fg_color="transparent", height=72, **kwargs)
        self.pack_propagate(False)
        self.on_search = on_search
        self.on_period_change = on_period_change
        self._search_after_id = None

        self.grid_columnconfigure(1, weight=1)
        self._build_greeting(user_name)
        self._build_search()
        self._build_actions()

    def _greeting_text(self, name):
        hour = datetime.now().hour
        if hour < 12:
            saludo = "Buenos días"
        elif hour < 19:
            saludo = "Buenas tardes"
        else:
            saludo = "Buenas noches"
        return f"{saludo}, {name}"

    def _build_greeting(self, user_name):
        ctk.CTkLabel(
            self,
            text=self._greeting_text(user_name),
            font=ctk.CTkFont(family=FONTS["display_md"][0], size=22, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=(0, 24))

    def _build_search(self):
        search_wrap = ctk.CTkFrame(self, fg_color=COLORS["bg_input"], corner_radius=24, height=44)
        search_wrap.grid(row=0, column=1, sticky="ew", padx=8)
        search_wrap.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            search_wrap, text="⌕", width=36,
            font=ctk.CTkFont(size=16), text_color=COLORS["text_muted"],
        ).grid(row=0, column=0, padx=(12, 0))

        self.search_entry = ctk.CTkEntry(
            search_wrap,
            placeholder_text="Buscar transacciones, productos...",
            height=40,
            border_width=0,
            fg_color="transparent",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_primary"],
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 12))
        self.search_entry.bind("<KeyRelease>", self._on_search_key)

    def _build_actions(self):
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=0, column=2, sticky="e", padx=(16, 0))

        self.period_var = ctk.StringVar(value=PERIOD_OPTIONS[0])
        self.period_menu = ctk.CTkOptionMenu(
            actions,
            values=PERIOD_OPTIONS,
            variable=self.period_var,
            width=130,
            height=36,
            corner_radius=8,
            fg_color=COLORS["bg_card"],
            button_color=COLORS["bg_card_alt"],
            button_hover_color=COLORS["border"],
            dropdown_fg_color=COLORS["bg_card"],
            font=ctk.CTkFont(size=13),
            command=self._on_period,
        )
        self.period_menu.pack(side="left", padx=(0, 12))


    def _on_search_key(self, _event=None):
        if self._search_after_id:
            self.after_cancel(self._search_after_id)
        self._search_after_id = self.after(300, self._emit_search)

    def _emit_search(self):
        self.on_search(self.search_entry.get().strip())

    def _on_period(self, choice):
        self.on_period_change(choice)

    def get_period(self):
        return self.period_var.get()

    def clear_search(self):
        self.search_entry.delete(0, "end")
