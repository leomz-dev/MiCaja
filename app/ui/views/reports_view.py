import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.ui.theme import COLORS, SPACING


class ReportsView(ctk.CTkScrollableFrame):
    def __init__(self, master, controller, **_kwargs):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._period = "Este Mes"
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self, text="Reportes y Análisis", anchor="w",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 20))

        self.charts_container = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_container.pack(fill="both", expand=True)

    def refresh(self, period="Este Mes", **_kwargs):
        self._period = period
        for w in self.charts_container.winfo_children():
            w.destroy()

        plt.style.use("dark_background")
        fig = plt.Figure(figsize=(10, 7), dpi=100, facecolor=COLORS["bg_main"])
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(212)

        ing, egr = self.controller.get_kpi_ingresos_egresos(period)
        ax1.bar(["Ingresos", "Egresos"], [ing, egr], color=[COLORS["primary"], COLORS["danger"]])
        ax1.set_title("Balance Operativo", color="white", fontsize=11, fontweight="bold")
        ax1.tick_params(colors=COLORS["text_secondary"])
        for spine in ax1.spines.values():
            spine.set_visible(False)

        costos = self.controller.get_kpi_costos(period)
        if costos:
            labels = [c[0][:18] for c in costos[:6]]
            sizes = [c[1] for c in costos[:6]]
            ax2.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=140,
                    textprops={"color": "white", "fontsize": 8})
        else:
            ax2.text(0.5, 0.5, "Sin gastos", color="white", ha="center", va="center")
        ax2.set_title("Estructura de Gastos", color="white", fontsize=11, fontweight="bold")

        top = self.controller.get_kpi_top_productos(8, period)
        if top:
            labels = [p[0][:22] for p in top]
            vals = [p[1] for p in top]
            ax3.barh(labels, vals, color=COLORS["primary"])
            ax3.set_title("Top Productos por Ingresos", color="white", fontsize=11, fontweight="bold")
            ax3.tick_params(colors=COLORS["text_secondary"])
            for spine in ax3.spines.values():
                spine.set_visible(False)
        else:
            ax3.text(0.5, 0.5, "Sin ventas", color="white", ha="center", va="center")

        fig.subplots_adjust(hspace=0.45, wspace=0.35)
        card = ctk.CTkFrame(
            self.charts_container, fg_color=COLORS["bg_card"],
            corner_radius=SPACING["card_radius"],
        )
        card.pack(fill="both", expand=True)
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)
