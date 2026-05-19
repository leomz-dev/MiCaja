import customtkinter as ctk
from tkinter import ttk, messagebox
from app.ui.theme import COLORS, SPACING
from app.ui.tree_style import configure_treeview


class TransactionsView(ctk.CTkFrame):
    def __init__(self, master, controller, callbacks, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self.callbacks = callbacks
        self._period = "Todo el tiempo"
        self._search = ""
        self._tipo = "Todos"
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hdr, text="Historial de Transacciones", anchor="w",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_primary"],
        ).grid(row=0, column=0, sticky="w")

        filters = ctk.CTkFrame(hdr, fg_color="transparent")
        filters.grid(row=0, column=1, sticky="e")

        self.tipo_var = ctk.StringVar(value="Todos")
        ctk.CTkOptionMenu(
            filters, values=["Todos", "Ingreso", "Egreso"],
            variable=self.tipo_var, width=120, height=36,
            fg_color=COLORS["bg_card"], command=self._on_tipo_filter,
        ).pack(side="left", padx=4)

        card = ctk.CTkFrame(
            self, fg_color=COLORS["bg_card"], corner_radius=SPACING["card_radius"],
        )
        card.grid(row=1, column=0, sticky="nsew")
        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(0, weight=1)

        style_name = configure_treeview("Tx.Treeview")
        self.tree = ttk.Treeview(
            card,
            columns=("Fecha", "Tipo", "Concepto", "Cant", "Unitario", "Total", "Desc"),
            show="headings",
            style=style_name,
        )
        for col, text, w, anchor in [
            ("Fecha", "FECHA", 100, "center"),
            ("Tipo", "TIPO", 90, "center"),
            ("Concepto", "CONCEPTO", 200, "w"),
            ("Cant", "CANT.", 60, "center"),
            ("Unitario", "UNITARIO", 110, "e"),
            ("Total", "TOTAL", 120, "e"),
            ("Desc", "NOTAS", 160, "w"),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor=anchor)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Delete>", self._on_delete)

        hint = ctk.CTkLabel(
            self, text="Doble clic para editar · Supr para eliminar",
            font=ctk.CTkFont(size=11), text_color=COLORS["text_muted"],
        )
        hint.grid(row=2, column=0, sticky="w", pady=(8, 0))

    def _on_tipo_filter(self, _=None):
        self._tipo = self.tipo_var.get()
        self.refresh(self._period, self._search)

    def _on_double_click(self, _event):
        sel = self.tree.selection()
        if sel:
            self.callbacks["edit_transaction"](int(sel[0]))

    def _on_delete(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        if messagebox.askyesno("Eliminar", "¿Eliminar esta transacción permanentemente?"):
            self.controller.delete_transaction(int(sel[0]))
            self.callbacks["refresh_all"]()

    def refresh(self, period="Todo el tiempo", search=""):
        self._period = period
        self._search = search
        for item in self.tree.get_children():
            self.tree.delete(item)
        txs = self.controller.get_filtered_transactions(period, search, self._tipo)
        for t in txs:
            desc = t.get("Descripcion", "")
            if str(desc) == "nan":
                desc = ""
            self.tree.insert(
                "", "end", iid=str(t["Id"]),
                values=(
                    t["Fecha"],
                    "Ingreso" if t["Tipo"] == "Ingreso" else "Gasto",
                    t["Item"],
                    int(t["Cantidad"]),
                    self.controller.format_currency(t["PrecioUnitario"]),
                    self.controller.format_currency(t["MontoTotal"]),
                    desc,
                ),
            )
