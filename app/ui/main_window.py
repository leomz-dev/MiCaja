import customtkinter as ctk
from tkinter import ttk, messagebox
from app.ui.modals import TransactionModal
from app.ui.charts_modal import KPIModal
from app.ui.catalog_modal import CatalogModal

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        config = self.controller.get_config()
        app_name = config.get("NombreNegocio", "MiCaja")
        
        self.title(f"{app_name} - Leonardo Meza")
        self.geometry("900x700")
        self.minsize(600, 600)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_action_buttons()
        self._build_history_table()
        
        self.refresh_ui()

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.header_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Panel de Balance
        self.lbl_saldo_title = ctk.CTkLabel(self.header_frame, text="SALDO ACTUAL", font=ctk.CTkFont(size=16, weight="bold"), text_color="#888888")
        self.lbl_saldo_title.grid(row=0, column=1, pady=(10, 0))
        
        self.lbl_saldo_val = ctk.CTkLabel(self.header_frame, text="$0", font=ctk.CTkFont(size=64, weight="bold"))
        self.lbl_saldo_val.grid(row=1, column=1)

        # Resumen Detallado
        self.summary_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.summary_frame.grid(row=2, column=1, pady=10)
        
        self.lbl_ingresos = ctk.CTkLabel(self.summary_frame, text="Ingresos: $0", font=ctk.CTkFont(size=14), text_color="#00c896")
        self.lbl_ingresos.pack(side="left", padx=20)
        
        self.lbl_egresos = ctk.CTkLabel(self.summary_frame, text="Egresos: $0", font=ctk.CTkFont(size=14), text_color="#ff4c4c")
        self.lbl_egresos.pack(side="left", padx=20)

        # Panel de Acciones Auxiliares
        util_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        util_frame.grid(row=0, column=2, rowspan=3, sticky="e", padx=20)

        self.btn_kpi = ctk.CTkButton(util_frame, text="📊 Métricas", width=150,
                                     font=ctk.CTkFont(size=13, weight="bold"),
                                     fg_color="#4da6ff", hover_color="#3380cc",
                                     command=self.open_kpi)
        self.btn_kpi.pack(pady=(0, 8))

        self.btn_catalog = ctk.CTkButton(util_frame, text="⚙️ Editar Catálogo", width=150,
                                         font=ctk.CTkFont(size=13, weight="bold"),
                                         fg_color="#888888", hover_color="#666666",
                                         command=self.open_catalog)
        self.btn_catalog.pack()

    def _build_action_buttons(self):
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.actions_frame.grid_columnconfigure((0,1), weight=1)
        
        self.btn_ingreso = ctk.CTkButton(self.actions_frame, text="➕ INGRESAR DINERO", 
                                        height=70, font=ctk.CTkFont(size=20, weight="bold"), 
                                        fg_color="#00c896", hover_color="#00a078",
                                        command=lambda: self.open_modal("Ingreso"))
        self.btn_ingreso.grid(row=0, column=0, sticky="ew", padx=10)
        
        self.btn_egreso = ctk.CTkButton(self.actions_frame, text="➖ REGISTRAR GASTO", 
                                        height=70, font=ctk.CTkFont(size=20, weight="bold"), 
                                        fg_color="#ff4c4c", hover_color="#cc0000",
                                        command=lambda: self.open_modal("Egreso"))
        self.btn_egreso.grid(row=0, column=1, sticky="ew", padx=10)

    def _build_history_table(self):
        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(20, 30))
        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)
        
        hdr_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        hdr_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)

        self.lbl_hist_title = ctk.CTkLabel(hdr_frame, text="Movimientos Recientes", font=ctk.CTkFont(size=14))
        self.lbl_hist_title.pack(side="left")

        # Configuración de estilos del Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, rowheight=30)
        style.map('Treeview', background=[('selected', '#00c896')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Helvetica', 10, 'bold'))
        
        self.tree = ttk.Treeview(self.history_frame, columns=("Fecha", "Tipo", "Item", "Cant", "Precio", "Total"), show="headings")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Item", text="Producto / Gasto")
        self.tree.heading("Cant", text="Cant.")
        self.tree.heading("Precio", text="Unitario")
        self.tree.heading("Total", text="Total")
        
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Tipo", width=80, anchor="center")
        self.tree.column("Item", width=220)
        self.tree.column("Cant", width=60, anchor="center")
        self.tree.column("Precio", width=100, anchor="e")
        self.tree.column("Total", width=110, anchor="e")
        
        self.tree.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Vinculaciones (Bindings)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<Delete>", self.on_tree_delete)

    def refresh_ui(self):
        summary = self.controller.get_dashboard_summary()
        self.lbl_saldo_val.configure(text=self.controller.format_currency(summary["saldo"]))
        if summary["saldo"] >= 0:
            self.lbl_saldo_val.configure(text_color="#00c896")
        else:
            self.lbl_saldo_val.configure(text_color="#ff4c4c")
            
        self.lbl_ingresos.configure(text=f"Ingresos: {self.controller.format_currency(summary['ingresos'])}")
        self.lbl_egresos.configure(text=f"Egresos: {self.controller.format_currency(summary['egresos'])}")
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        transactions = self.controller.get_transactions()
        # Mostrar el historial reciente (20 entradas)
        for t in transactions[:20]:
            p_fmt = self.controller.format_currency(t["PrecioUnitario"])
            t_fmt = self.controller.format_currency(t["MontoTotal"])
            self.tree.insert("", "end", iid=str(t["Id"]), values=(t["Fecha"], t["Tipo"], t["Item"], t["Cantidad"], p_fmt, t_fmt))

    def open_modal(self, mode, transaction_data=None):
        modal = TransactionModal(self, self.controller, mode, on_save_callback=self.refresh_ui, transaction_data=transaction_data)

    def open_kpi(self):
        KPIModal(self, self.controller)

    def open_catalog(self):
        CatalogModal(self, self.controller)

    def on_tree_double_click(self, event):
        selected = self.tree.selection()
        if not selected: return
        trans_id = int(selected[0])
        # Buscamos la transacción
        t_data = self.controller.get_transaction(trans_id)
        if t_data:
            self.open_modal(t_data["Tipo"], transaction_data=t_data)

    def on_tree_delete(self, event):
        selected = self.tree.selection()
        if not selected: return
        trans_id = int(selected[0])
        
        anwser = messagebox.askyesno("Eliminar Movimiento", "¿Estás seguro que deseas eliminar esta transacción permanentemente?")
        if anwser:
            self.controller.delete_transaction(trans_id)
            self.refresh_ui()
