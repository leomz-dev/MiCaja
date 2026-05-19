import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.ui.theme import COLORS, SPACING, FONTS
from app.ui.components.kpi_card import KpiCard
from app.ui.components.badge import TypeBadge


class DashboardView(ctk.CTkScrollableFrame):
    def __init__(self, master, controller, callbacks, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self.callbacks = callbacks
        self._chart_canvas = None
        self._build()

    def _build(self):
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(0, 20))
        actions.grid_columnconfigure((0, 1), weight=1, uniform="act")

        ctk.CTkButton(
            actions, text="+  Ingresar Dinero", height=52,
            corner_radius=SPACING["btn_radius"],
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            text_color=COLORS["primary_light"],
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: self.callbacks["open_modal"]("Ingreso"),
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            actions, text="−  Registrar Gasto", height=52,
            corner_radius=SPACING["btn_radius"],
            fg_color="transparent", hover_color=COLORS["danger_light"],
            border_width=2, border_color=COLORS["danger"],
            text_color=COLORS["danger"],
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: self.callbacks["open_modal"]("Egreso"),
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        kpi_row = ctk.CTkFrame(self, fg_color="transparent")
        kpi_row.pack(fill="x", pady=(0, 20))
        kpi_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="kpi")

        self.card_saldo = KpiCard(
            kpi_row, "Saldo Actual", icon="$",
            value_color=COLORS["primary"],
            accent_icon_bg=COLORS["primary_light"],
        )
        self.card_saldo.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.card_ingresos = KpiCard(
            kpi_row, "Ingresos (Mensual)", icon="↑",
            value_color=COLORS["text_primary"],
            accent_icon_bg=COLORS["primary_light"],
        )
        self.card_ingresos.grid(row=0, column=1, sticky="nsew", padx=8)

        self.card_egresos = KpiCard(
            kpi_row, "Egresos (Mensual)", icon="↓",
            value_color=COLORS["danger"],
            accent_icon_bg=COLORS["danger_light"],
        )
        self.card_egresos.grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        self._build_movements(body)
        self._build_sidebar_widgets(body)

    def _build_movements(self, parent):
        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=SPACING["card_radius"])
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        card.grid_rowconfigure(2, weight=1)
        card.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            hdr, text="Movimientos Recientes", anchor="w",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS["text_primary"],
        ).grid(row=0, column=0, sticky="w")
        

        cols = ctk.CTkFrame(card, fg_color="transparent")
        cols.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 4))
        col_specs = [
            ("FECHA", 72), ("TIPO", 72), ("CONCEPTO", None),
            ("CANT.", 48), ("UNITARIO", 80), ("TOTAL", 90),
        ]
        for i, (text, w) in enumerate(col_specs):
            if w is None:
                cols.grid_columnconfigure(i, weight=1)
            kw = dict(
                text=text, font=ctk.CTkFont(size=10, weight="bold"),
                text_color=COLORS["text_muted"],
            )
            if w is not None:
                kw["width"] = w
            ctk.CTkLabel(cols, **kw).grid(
                row=0, column=i, sticky="w" if w is None else "ew", padx=4,
            )

        self.rows_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.rows_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 8))

        ctk.CTkButton(
            card, text="Ver todas las transacciones →",
            fg_color="transparent", hover_color=COLORS["bg_card_alt"],
            text_color=COLORS["accent_blue"], font=ctk.CTkFont(size=13),
            command=self.callbacks["go_transactions"],
        ).grid(row=3, column=0, pady=(4, 16))

    def _build_sidebar_widgets(self, parent):
        right = ctk.CTkFrame(parent, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")

        chart_card = ctk.CTkFrame(
            right, fg_color=COLORS["bg_card"], corner_radius=SPACING["card_radius"],
        )
        chart_card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(
            chart_card, text="Balance Operativo", anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=16, pady=(14, 4))
        self.chart_frame = ctk.CTkFrame(chart_card, fg_color="transparent", height=160)
        self.chart_frame.pack(fill="x", padx=8, pady=(0, 12))

        top_card = ctk.CTkFrame(
            right, fg_color=COLORS["bg_card"], corner_radius=SPACING["card_radius"],
        )
        top_card.pack(fill="both", expand=True, pady=(0, 12))
        ctk.CTkLabel(
            top_card, text="Top Productos (Ingresos)", anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=16, pady=(14, 8))
        self.top_products_frame = ctk.CTkFrame(top_card, fg_color="transparent")
        self.top_products_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ctk.CTkButton(
            right, text="🔒  Realizar Cierre de Caja", height=48,
            corner_radius=SPACING["btn_radius"],
            fg_color=COLORS["bg_card"], hover_color=COLORS["border"],
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(fill="x")

    def _render_movement_row(self, t):
        row = ctk.CTkFrame(self.rows_frame, fg_color="transparent", height=44)
        row.pack(fill="x", pady=1)
        row.grid_columnconfigure(2, weight=1)

        fecha = str(t["Fecha"])[5:].replace("-", "/") if t.get("Fecha") else ""
        ctk.CTkLabel(
            row, text=fecha, width=72, font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"],
        ).grid(row=0, column=0, padx=4)

        badge_wrap = ctk.CTkFrame(row, fg_color="transparent", width=72)
        badge_wrap.grid(row=0, column=1, padx=4)
        TypeBadge(badge_wrap, t["Tipo"]).pack()

        concepto = t["Item"]
        desc = t.get("Descripcion", "")
        if desc and str(desc) != "nan":
            concepto = f"{t['Item']}\n{desc}"[:60]
        ctk.CTkLabel(
            row, text=concepto, anchor="w", justify="left",
            font=ctk.CTkFont(size=12), text_color=COLORS["text_primary"],
        ).grid(row=0, column=2, sticky="w", padx=4)

        ctk.CTkLabel(
            row, text=str(int(t["Cantidad"])), width=48,
            font=ctk.CTkFont(size=12), text_color=COLORS["text_secondary"],
        ).grid(row=0, column=3, padx=4)

        ctk.CTkLabel(
            row, text=self.controller.format_currency(t["PrecioUnitario"]),
            width=80, font=ctk.CTkFont(family="Consolas", size=11),
            text_color=COLORS["text_secondary"],
        ).grid(row=0, column=4, padx=4)

        is_ing = t["Tipo"] == "Ingreso"
        sign = "+" if is_ing else "−"
        color = COLORS["primary"] if is_ing else COLORS["danger"]
        ctk.CTkLabel(
            row, text=f"{sign} {self.controller.format_currency(t['MontoTotal'])}",
            width=100, anchor="e",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=color,
        ).grid(row=0, column=5, padx=4)

        row.bind("<Double-1>", lambda e, tid=t["Id"]: self.callbacks["edit_transaction"](tid))
        for child in row.winfo_children():
            child.bind("<Double-1>", lambda e, tid=t["Id"]: self.callbacks["edit_transaction"](tid))

    def _draw_chart(self, weekly_data):
        for w in self.chart_frame.winfo_children():
            w.destroy()
        if not weekly_data:
            ctk.CTkLabel(
                self.chart_frame, text="Sin datos en el periodo",
                text_color=COLORS["text_muted"],
            ).pack(pady=40)
            return

        fig, ax = plt.subplots(figsize=(3.2, 1.6), dpi=100, facecolor=COLORS["bg_card"])
        labels = [d[0] for d in weekly_data]
        ing = [d[1] for d in weekly_data]
        egr = [d[2] for d in weekly_data]
        x = range(len(labels))
        w = 0.35
        ax.bar([i - w / 2 for i in x], ing, w, color=COLORS["primary"], label="Ing")
        ax.bar([i + w / 2 for i in x], egr, w, color=COLORS["danger"], label="Egr")
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, color=COLORS["text_muted"], fontsize=8)
        ax.tick_params(colors=COLORS["text_muted"], labelsize=7)
        ax.set_facecolor(COLORS["bg_card"])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.yaxis.set_visible(False)
        fig.tight_layout(pad=0.5)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x")

    def _render_top_products(self, products):
        for w in self.top_products_frame.winfo_children():
            w.destroy()
        if not products:
            ctk.CTkLabel(
                self.top_products_frame, text="Sin ventas registradas",
                text_color=COLORS["text_muted"],
            ).pack(pady=20)
            return
        for name, _amount, pct in products[:5]:
            row = ctk.CTkFrame(self.top_products_frame, fg_color="transparent")
            row.pack(fill="x", pady=6)
            ctk.CTkLabel(
                row, text=name[:28], anchor="w", font=ctk.CTkFont(size=12),
                text_color=COLORS["text_primary"],
            ).pack(anchor="w")
            bar_row = ctk.CTkFrame(row, fg_color="transparent")
            bar_row.pack(fill="x", pady=(4, 0))
            bar_bg = ctk.CTkFrame(bar_row, fg_color=COLORS["bg_card_alt"], height=6, corner_radius=3)
            bar_bg.pack(side="left", fill="x", expand=True)
            ctk.CTkFrame(
                bar_bg, fg_color=COLORS["primary"], corner_radius=3,
            ).place(relx=0, rely=0, relheight=1, relwidth=min(pct / 100, 1))
            ctk.CTkLabel(
                bar_row, text=f"{pct:.0f}%", width=36,
                font=ctk.CTkFont(size=11), text_color=COLORS["text_secondary"],
            ).pack(side="right", padx=(6, 0))

    def refresh(self, period="Este Mes", search=""):
        summary = self.controller.get_dashboard_summary(period)
        trend = self.controller.get_saldo_trend_pct(period)
        trend_txt = ""
        if trend is not None:
            sign = "+" if trend >= 0 else ""
            trend_txt = f"{sign}{trend:.1f}% vs mes anterior"
            trend_color = COLORS["primary"] if trend >= 0 else COLORS["danger"]
        else:
            trend_color = COLORS["text_secondary"]

        saldo_color = COLORS["primary"] if summary["saldo"] >= 0 else COLORS["danger"]
        self.card_saldo.update(
            self.controller.format_currency(summary["saldo"]),
            trend_txt, saldo_color,
        )
        self.card_ingresos.update(
            self.controller.format_currency(summary["ingresos"]),
            f"{summary['count_ingresos']} operaciones",
        )
        self.card_egresos.update(
            self.controller.format_currency(summary["egresos"]),
            f"{summary['count_egresos']} operaciones",
        )

        for w in self.rows_frame.winfo_children():
            w.destroy()
        txs = self.controller.get_filtered_transactions(period, search)[:8]
        for t in txs:
            self._render_movement_row(t)
        if not txs:
            ctk.CTkLabel(
                self.rows_frame, text="No hay movimientos",
                text_color=COLORS["text_muted"],
            ).pack(pady=24)

        self._draw_chart(self.controller.get_weekly_balance(period))
        self._render_top_products(self.controller.get_kpi_top_productos(5, period))
