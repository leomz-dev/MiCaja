import customtkinter as ctk
from datetime import datetime

class TransactionModal(ctk.CTkToplevel):
    def __init__(self, parent, controller, mode, on_save_callback, transaction_data=None):
        super().__init__(parent)
        self.controller = controller
        self.mode = mode # 'Ingreso' o 'Egreso'
        self.on_save_callback = on_save_callback
        self.transaction_data = transaction_data # Diccionario si se está editando, None si se está creando
        
        accion = "Editar" if transaction_data else "Registrar Nuevo"
        self.title(f"Añadir {self.mode}")
        self.geometry("450x500")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()

        self.color = "#00c896" if mode == "Ingreso" else "#ff4c4c"

        # Inicialización del catálogo
        self.catalog = self.controller.get_catalog_by_type(self.mode)
        if not self.catalog:
            self.catalog = [{"Nombre": "Elemento General", "PrecioPredeterminado": 0}]
            
        self.catalog_map = {item['Nombre']: item for item in self.catalog}
        self.item_names = list(self.catalog_map.keys())
        
        self._build_ui(accion)
        self._load_data()

    def _build_ui(self, accion):
        # Encabezado
        self.lbl_title = ctk.CTkLabel(self, text=f"{accion} {self.mode}", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.color)
        self.lbl_title.pack(pady=20)
        
        # Selector de Item
        self.item_var = ctk.StringVar(value=self.item_names[0])
        self.cb_item = ctk.CTkOptionMenu(self, variable=self.item_var, values=self.item_names, 
                                        height=40, font=ctk.CTkFont(size=14), command=self._on_item_select)
        self.cb_item.pack(padx=30, pady=(0, 15), fill="x")
        
        # Campos numéricos
        self.pc_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pc_frame.pack(padx=30, pady=(0, 15), fill="x")
        self.pc_frame.grid_columnconfigure((0,1), weight=1)
        
        # Precio Unitario
        self.entry_precio = ctk.CTkEntry(self.pc_frame, placeholder_text="Precio Unit. ($)", height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.entry_precio.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.entry_precio.bind("<KeyRelease>", self._update_total)
        
        # Cantidad
        self.entry_cantidad = ctk.CTkEntry(self.pc_frame, placeholder_text="Cantidad", height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.entry_cantidad.bind("<KeyRelease>", self._update_total)
        
        # Etiqueta de Total
        self.lbl_total = ctk.CTkLabel(self, text="Total: $0", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_total.pack(pady=(0, 15))
        
        # Descripción
        self.entry_desc = ctk.CTkEntry(self, placeholder_text="Anotación (Opcional)", height=40, font=ctk.CTkFont(size=14))
        self.entry_desc.pack(padx=30, pady=(0, 20), fill="x")
        
        # Etiqueta de Error
        self.lbl_error = ctk.CTkLabel(self, text="", text_color="#ff4c4c")
        self.lbl_error.pack(padx=30, pady=(0, 10))
        
        # Botón Guardar
        txt_btn = "Actualizar Movimiento" if self.transaction_data else "Guardar Movimiento"
        self.btn_guardar = ctk.CTkButton(self, text=txt_btn, height=50, font=ctk.CTkFont(size=16, weight="bold"), 
                                        fg_color=self.color, hover_color=self.color, command=self.save)
        self.btn_guardar.pack(padx=30, fill="x", side="bottom", pady=20)

    def _load_data(self):
        if self.transaction_data:
            t = self.transaction_data
            if t["Item"] in self.item_names:
                self.item_var.set(t["Item"])
            self.entry_precio.delete(0, 'end')
            p = float(t["PrecioUnitario"])
            self.entry_precio.insert(0, str(int(p) if p.is_integer() else p))
            
            self.entry_cantidad.delete(0, 'end')
            self.entry_cantidad.insert(0, str(int(t["Cantidad"])))
            
            desc = t["Descripcion"]
            if str(desc) != 'nan':
                self.entry_desc.insert(0, desc)

            self._update_total()
        else:
            self._update_prices()

    def _on_item_select(self, choice):
        self._update_prices()

    def _update_prices(self):
        sel_name = self.item_var.get()
        item = self.catalog_map.get(sel_name)
        if item:
            precio = float(item["PrecioPredeterminado"])
            self.entry_precio.delete(0, 'end')
            self.entry_precio.insert(0, str(int(precio) if precio.is_integer() else precio))
        self._update_total()

    def _update_total(self, event=None):
        try:
            p = float(self.entry_precio.get())
            c = float(self.entry_cantidad.get())
            total = p * c
            self.lbl_total.configure(text=f"Total: {self.controller.format_currency(total)}")
        except ValueError:
            self.lbl_total.configure(text="Total: -")

    def save(self):
        item = self.item_var.get()
        desc = self.entry_desc.get().strip()
        
        try:
            precio = float(self.entry_precio.get().strip())
            cantidad = float(self.entry_cantidad.get().strip())
            
            if precio < 0 or cantidad <= 0:
                raise ValueError()
                
            if self.transaction_data:
                # Actualizar
                self.controller.update_transaction(
                    self.transaction_data["Id"],
                    item, cantidad, precio, desc
                )
            else:
                # Crear
                fecha = datetime.now().strftime("%Y-%m-%d")
                self.controller.add_transaction(fecha, self.mode, item, cantidad, precio, desc)
                
            self.on_save_callback()
            self.destroy()
        except ValueError:
            self.lbl_error.configure(text="El precio y la cantidad deben ser números válidos mayores a 0.")
        except Exception as e:
            self.lbl_error.configure(text=str(e))
