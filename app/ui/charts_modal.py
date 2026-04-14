import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class KPIModal(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.title("Panel de Métricas de Negocio")
        self.geometry("900x650")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()

        self.lbl_title = ctk.CTkLabel(self, text="Métricas Clave (KPIs)", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_title.pack(pady=15)

        # Plot frame
        self.plot_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.plot_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self._build_charts()

    def _build_charts(self):
        # Estética de las Gráficas
        plt.style.use('dark_background')
        fig = plt.Figure(figsize=(12, 8), dpi=100, facecolor="#2b2b2b")
        
        ax1 = fig.add_subplot(221) # Balance
        ax2 = fig.add_subplot(222) # Gastos
        ax3 = fig.add_subplot(212) # Ventas
        fig.subplots_adjust(hspace=0.4, wspace=0.3)

        # Métrica 1: Ingresos vs Egresos (Barras)
        ingresos, egresos = self.controller.get_kpi_ingresos_egresos()
        ax1.bar(["Ingresos", "Egresos"], [ingresos, egresos], color=["#00c896", "#ff4c4c"])
        ax1.set_title("Balance Operativo", color="white", fontsize=12, fontweight="bold")
        ax1.tick_params(colors="lightgray")
        # Quitar bordes innecesarios
        for spine in ax1.spines.values(): spine.set_visible(False)

        # Métrica 2: Distribución de Costos (Pastel)
        costos = self.controller.get_kpi_costos()
        if costos:
            labels = [c[0] for c in costos]
            sizes = [c[1] for c in costos]
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'color':"white"})
            ax2.set_title("Estructura de Gastos", color="white", fontsize=12, fontweight="bold")
        else:
            ax2.text(0.5, 0.5, "Sin Gastos", color="white", ha='center', va='center')
            ax2.axis('off')

        # Métrica 3: Productos más Vendidos (Barras Horizontales)
        top_prod = self.controller.get_kpi_top_productos()
        if top_prod:
            labels = [p[0] for p in top_prod]
            vals = [p[1] for p in top_prod]
            ax3.barh(labels, vals, color="#00c896")
            ax3.set_title("Top Productos Más Vendidos", color="white", fontsize=12, fontweight="bold")
            ax3.tick_params(colors="lightgray")
            for spine in ax3.spines.values(): spine.set_visible(False)
        else:
            ax3.text(0.5, 0.5, "Sin Ventas", color="white", ha='center', va='center')
            ax3.axis('off')

        # Empotrar Tkinter Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
