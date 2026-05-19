import customtkinter as ctk
from tkinter import messagebox
from app.ui.theme import COLORS, SPACING
from app.ui.components.kpi_card import KpiCard


class ProductsView(ctk.CTkScrollableFrame):
    def __init__(self, master, controller, callbacks, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self.callbacks = callbacks
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self, text="Inventario y Productos", anchor="w",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 20))

        kpi_row = ctk.CTkFrame(self, fg_color="transparent")
        kpi_row.pack(fill="x", pady=(0, 20))
        kpi_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="p")

        self.card_prod = KpiCard(kpi_row, "Productos (venta)", icon="▣")
        self.card_prod.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.card_gastos = KpiCard(kpi_row, "Items de gasto", icon="◎")
        self.card_gastos.grid(row=0, column=1, sticky="nsew", padx=8)
        self.card_valor = KpiCard(
            kpi_row, "Valor catálogo ventas", icon="◈",
            value_color=COLORS["primary"],
        )
        self.card_valor.grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(0, 12))
        ctk.CTkButton(
            actions, text="+ Agregar producto / gasto", height=44,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            text_color=COLORS["primary_light"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._show_add_form,
        ).pack(side="left")

        self.list_frame = ctk.CTkFrame(
            self, fg_color=COLORS["bg_card"], corner_radius=SPACING["card_radius"],
        )
        self.list_frame.pack(fill="both", expand=True)

        self.add_panel = ctk.CTkFrame(
            self, fg_color=COLORS["bg_card"], corner_radius=SPACING["card_radius"],
        )

    def _show_add_form(self):
        if self.add_panel.winfo_ismapped():
            self.add_panel.pack_forget()
            return
        for w in self.add_panel.winfo_children():
            w.destroy()
        self.add_panel.pack(fill="x", pady=12, padx=0)

        inner = ctk.CTkFrame(self.add_panel, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)
        inner.grid_columnconfigure((1, 2), weight=1)

        ctk.CTkLabel(
            inner, text="Nuevo item", font=ctk.CTkFont(size=15, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))

        self.new_tipo = ctk.StringVar(value="Ingreso")
        ctk.CTkSegmentedButton(
            inner, values=["Ingreso", "Egreso"], variable=self.new_tipo,
        ).grid(row=1, column=0, sticky="w", padx=(0, 8))

        self.entry_nombre = ctk.CTkEntry(inner, placeholder_text="Nombre", height=40)
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=8)

        self.entry_precio = ctk.CTkEntry(inner, placeholder_text="Precio", height=40, width=120)
        self.entry_precio.grid(row=1, column=2, sticky="e")

        self.lbl_err = ctk.CTkLabel(inner, text="", text_color=COLORS["danger"])
        self.lbl_err.grid(row=2, column=0, columnspan=3, sticky="w", pady=4)

        ctk.CTkButton(
            inner, text="Guardar", width=100, height=36,
            fg_color=COLORS["primary"], command=self._add_item,
        ).grid(row=1, column=3, padx=(8, 0))

    def _add_item(self):
        try:
            precio = float(self.entry_precio.get().strip())
            self.controller.add_catalog_item(
                self.entry_nombre.get(), self.new_tipo.get(), precio,
            )
            self.add_panel.pack_forget()
            self.callbacks["refresh_all"]()
        except Exception as e:
            self.lbl_err.configure(text=str(e))

    def _render_item_row(self, item):
        row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=8)

        is_ing = item["Tipo"] == "Ingreso"
        color = COLORS["primary"] if is_ing else COLORS["danger"]
        tipo_lbl = ctk.CTkLabel(
            row, text="VENTA" if is_ing else "GASTO", width=56,
            font=ctk.CTkFont(size=10, weight="bold"), text_color=color,
        )
        tipo_lbl.pack(side="left", padx=(0, 12))

        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            info, text=item["Nombre"], anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text=self.controller.format_currency(item["PrecioPredeterminado"]),
            anchor="w", font=ctk.CTkFont(family="Consolas", size=12),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        bar_wrap = ctk.CTkFrame(row, fg_color=COLORS["bg_card_alt"], width=80, height=6, corner_radius=3)
        bar_wrap.pack(side="left", padx=16)
        bar_wrap.pack_propagate(False)
        stock_pct = min(100, (item["Id"] % 10) * 10 + 30)
        if stock_pct < 40:
            bar_color = COLORS["danger"]
        elif stock_pct < 70:
            bar_color = COLORS["warning"]
        else:
            bar_color = COLORS["primary"]
        ctk.CTkFrame(
            bar_wrap, fg_color=bar_color, corner_radius=3,
        ).place(relx=0, rely=0, relheight=1, relwidth=stock_pct / 100)

        ctk.CTkButton(
            row, text="✕", width=32, height=32,
            fg_color="transparent", hover_color=COLORS["danger_light"],
            text_color=COLORS["text_muted"],
            command=lambda iid=int(item["Id"]): self._delete(iid),
        ).pack(side="right")

    def _delete(self, cat_id):
        if messagebox.askyesno("Eliminar", "¿Eliminar este item del catálogo?"):
            self.controller.delete_catalog_item(cat_id)
            self.callbacks["refresh_all"]()

    def refresh(self, **_kwargs):
        summary = self.controller.get_catalog_summary()
        self.card_prod.update(str(summary["total_productos"]), "en catálogo de ventas")
        self.card_gastos.update(str(summary["total_gastos_cat"]), "conceptos de egreso")
        self.card_valor.update(
            self.controller.format_currency(summary["valor_catalogo"]),
            "suma precios referencia",
        )
        for w in self.list_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self.list_frame, text="CATÁLOGO", anchor="w",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(16, 8))
        for item in summary["items"]:
            self._render_item_row(item)
