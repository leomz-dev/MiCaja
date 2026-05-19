import customtkinter as ctk
from datetime import datetime
from app.ui.theme import COLORS, SPACING


class OperationPickerModal(ctk.CTkToplevel):
    def __init__(self, parent, on_ingreso, on_egreso):
        super().__init__(parent)
        self.title("Nueva Operación")
        self.geometry("360x220")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=COLORS["bg_main"])

        ctk.CTkLabel(
            self, text="¿Qué deseas registrar?",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(pady=(24, 16))

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=24)
        btns.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btns, text="+ Ingreso", height=48,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            text_color=COLORS["primary_light"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: (self.destroy(), on_ingreso()),
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            btns, text="− Gasto", height=48,
            fg_color="transparent", border_width=2, border_color=COLORS["danger"],
            text_color=COLORS["danger"], hover_color=COLORS["danger_light"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: (self.destroy(), on_egreso()),
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))


class TransactionModal(ctk.CTkToplevel):
    def __init__(self, parent, controller, mode, on_save_callback, transaction_data=None):
        super().__init__(parent)
        self.controller = controller
        self.mode = mode
        self.on_save_callback = on_save_callback
        self.transaction_data = transaction_data

        accion = "Editar" if transaction_data else "Registrar"
        self.title(f"{accion} {self.mode}")
        self.geometry("480x520")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=COLORS["bg_main"])

        self.color = COLORS["primary"] if mode == "Ingreso" else COLORS["danger"]

        self.catalog = self.controller.get_catalog_by_type(self.mode)
        if not self.catalog:
            self.catalog = [{"Nombre": "Elemento General", "PrecioPredeterminado": 0}]
        self.catalog_map = {item["Nombre"]: item for item in self.catalog}
        self.item_names = list(self.catalog_map.keys())

        self._build_ui(accion)
        self._load_data()

    def _build_ui(self, accion):
        card = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=SPACING["card_radius"])
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            card, text=f"{accion} {self.mode}",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=self.color,
        ).pack(pady=(24, 20))

        self.item_var = ctk.StringVar(value=self.item_names[0])
        ctk.CTkOptionMenu(
            card, variable=self.item_var, values=self.item_names,
            height=42, font=ctk.CTkFont(size=14),
            fg_color=COLORS["bg_input"], command=self._on_item_select,
        ).pack(padx=24, pady=(0, 12), fill="x")

        pc = ctk.CTkFrame(card, fg_color="transparent")
        pc.pack(padx=24, pady=(0, 12), fill="x")
        pc.grid_columnconfigure((0, 1), weight=1)

        self.entry_precio = ctk.CTkEntry(
            pc, placeholder_text="Precio unitario", height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["bg_input"],
        )
        self.entry_precio.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.entry_precio.bind("<KeyRelease>", self._update_total)

        self.entry_cantidad = ctk.CTkEntry(
            pc, placeholder_text="Cantidad", height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["bg_input"],
        )
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        self.entry_cantidad.bind("<KeyRelease>", self._update_total)

        self.lbl_total = ctk.CTkLabel(
            card, text="Total: $0",
            font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
            text_color=COLORS["text_primary"],
        )
        self.lbl_total.pack(pady=(0, 12))

        self.entry_desc = ctk.CTkEntry(
            card, placeholder_text="Notas (opcional)", height=42,
            fg_color=COLORS["bg_input"],
        )
        self.entry_desc.pack(padx=24, pady=(0, 12), fill="x")

        self.lbl_error = ctk.CTkLabel(card, text="", text_color=COLORS["danger"])
        self.lbl_error.pack(padx=24)

        txt = "Actualizar" if self.transaction_data else "Guardar movimiento"
        ctk.CTkButton(
            card, text=txt, height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.color,
            hover_color=COLORS["primary_hover"] if self.mode == "Ingreso" else COLORS["danger_hover"],
            command=self.save,
        ).pack(padx=24, fill="x", pady=(16, 24))

    def _load_data(self):
        if self.transaction_data:
            t = self.transaction_data
            if t["Item"] in self.item_names:
                self.item_var.set(t["Item"])
            self.entry_precio.delete(0, "end")
            p = float(t["PrecioUnitario"])
            self.entry_precio.insert(0, str(int(p) if p == int(p) else p))
            self.entry_cantidad.delete(0, "end")
            self.entry_cantidad.insert(0, str(int(t["Cantidad"])))
            desc = t.get("Descripcion", "")
            if desc and str(desc) != "nan":
                self.entry_desc.insert(0, desc)
            self._update_total()
        else:
            self._update_prices()

    def _on_item_select(self, _choice):
        self._update_prices()

    def _update_prices(self):
        item = self.catalog_map.get(self.item_var.get())
        if item:
            precio = float(item["PrecioPredeterminado"])
            self.entry_precio.delete(0, "end")
            self.entry_precio.insert(0, str(int(precio) if precio == int(precio) else precio))
        self._update_total()

    def _update_total(self, _event=None):
        try:
            total = float(self.entry_precio.get()) * float(self.entry_cantidad.get())
            self.lbl_total.configure(text=f"Total: {self.controller.format_currency(total)}")
        except ValueError:
            self.lbl_total.configure(text="Total: —")

    def save(self):
        item = self.item_var.get()
        desc = self.entry_desc.get().strip()
        try:
            precio = float(self.entry_precio.get().strip())
            cantidad = float(self.entry_cantidad.get().strip())
            if precio < 0 or cantidad <= 0:
                raise ValueError()
            if self.transaction_data:
                self.controller.update_transaction(
                    self.transaction_data["Id"], item, cantidad, precio, desc,
                )
            else:
                fecha = datetime.now().strftime("%Y-%m-%d")
                self.controller.add_transaction(fecha, self.mode, item, cantidad, precio, desc)
            self.on_save_callback()
            self.destroy()
        except ValueError:
            self.lbl_error.configure(text="Precio y cantidad deben ser números válidos > 0.")
        except Exception as e:
            self.lbl_error.configure(text=str(e))
