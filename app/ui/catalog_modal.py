import customtkinter as ctk
from tkinter import ttk, messagebox


class CatalogModal(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title("Gestión de Catálogo")
        self.geometry("700x580")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._refresh_table()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Encabezado
        ctk.CTkLabel(self, text="Catálogo de Productos y Gastos",
                     font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(20, 10))

        # Tabla de Items
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Cat.Treeview",
                        background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=28)
        style.map("Cat.Treeview", background=[("selected", "#4da6ff")])
        style.configure("Cat.Treeview.Heading",
                        background="#565b5e", foreground="white",
                        relief="flat", font=("Helvetica", 10, "bold"))

        self.tree = ttk.Treeview(table_frame,
                                 columns=("Tipo", "Nombre", "Precio"),
                                 show="headings", style="Cat.Treeview")
        self.tree.heading("Tipo",   text="Tipo")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio Unitario")
        self.tree.column("Tipo",   width=90,  anchor="center")
        self.tree.column("Nombre", width=300)
        self.tree.column("Precio", width=140, anchor="e")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Formulario de Entrada
        form_frame = ctk.CTkFrame(self, width=200)
        form_frame.grid(row=1, column=1, sticky="ns", padx=(0, 20), pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Nuevo Item",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 15))

        # Tipo (Ingreso / Egreso)
        self.tipo_var = ctk.StringVar(value="Ingreso")
        ctk.CTkSegmentedButton(form_frame, values=["Ingreso", "Egreso"],
                               variable=self.tipo_var).pack(padx=15, pady=(0, 12), fill="x")

        # Nombre
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre del item",
                                         height=38, font=ctk.CTkFont(size=13))
        self.entry_nombre.pack(padx=15, pady=(0, 10), fill="x")

        # Precio
        self.entry_precio = ctk.CTkEntry(form_frame, placeholder_text="Precio ($)",
                                          height=38, font=ctk.CTkFont(size=13, weight="bold"))
        self.entry_precio.pack(padx=15, pady=(0, 10), fill="x")

        # Mensajes de error
        self.lbl_err = ctk.CTkLabel(form_frame, text="", text_color="#ff4c4c",
                                    wraplength=170, font=ctk.CTkFont(size=11))
        self.lbl_err.pack(padx=15)

        # Botón Agregar
        ctk.CTkButton(form_frame, text="➕ Agregar", height=40,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="#00c896", hover_color="#00a078",
                      command=self._add_item).pack(padx=15, pady=10, fill="x")

        # Separador visual
        ctk.CTkFrame(form_frame, height=2, fg_color="#444").pack(padx=15, fill="x", pady=5)

        # Botón Eliminar seleccionado
        ctk.CTkButton(form_frame, text="🗑 Eliminar Seleccionado", height=40,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color="#ff4c4c", hover_color="#cc0000",
                      command=self._delete_selected).pack(padx=15, pady=(5, 20), fill="x")

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        items = self.controller.get_all_catalog()
        for it in items:
            precio_fmt = self.controller.format_currency(it["PrecioPredeterminado"])
            self.tree.insert("", "end", iid=str(int(it["Id"])),
                             values=(it["Tipo"], it["Nombre"], precio_fmt))

    def _add_item(self):
        self.lbl_err.configure(text="")
        nombre = self.entry_nombre.get().strip()
        tipo   = self.tipo_var.get()
        try:
            precio = float(self.entry_precio.get().strip())
            self.controller.add_catalog_item(nombre, tipo, precio)
            self.entry_nombre.delete(0, "end")
            self.entry_precio.delete(0, "end")
            self._refresh_table()
        except ValueError as e:
            self.lbl_err.configure(text=str(e) if str(e) else "Precio inválido.")
        except Exception as e:
            self.lbl_err.configure(text=str(e))

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        cat_id = int(selected[0])
        if messagebox.askyesno("Eliminar Item",
                               "¿Eliminar este item del catálogo?\n"
                               "No afecta los movimientos ya registrados."):
            self.controller.delete_catalog_item(cat_id)
            self._refresh_table()
