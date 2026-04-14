from app.models.excel_manager import ExcelManager

class MainController:
    def __init__(self):
        self.excel_manager = ExcelManager()
        self.config = self.excel_manager.get_config()
        self.moneda = self.config.get("Moneda", "$")

    def get_config(self):
        return self.config

    def format_currency(self, amount):
        try:
            return f"{self.moneda} {amount:,.0f}".replace(",", ".")
        except:
            return f"{self.moneda} 0"

    # Catálogo
    def get_catalog_by_type(self, tipo):
        df = self.excel_manager.get_catalog()
        f_df = df[df["Tipo"] == tipo]
        return f_df.to_dict('records')

    def get_all_catalog(self):
        df = self.excel_manager.get_catalog()
        return df.to_dict('records')

    def add_catalog_item(self, nombre, tipo, precio):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        self.excel_manager.add_catalog_item(nombre.strip(), tipo, precio)

    def delete_catalog_item(self, cat_id):
        self.excel_manager.delete_catalog_item(cat_id)

    # Transacciones
    def get_transactions(self):
        df = self.excel_manager.get_transactions()
        df = df.sort_values(by="Id", ascending=False)
        return df.to_dict('records')

    def get_transaction(self, trans_id):
        raw = self.excel_manager.get_transaction(trans_id)
        return raw.to_dict() if raw is not None else None

    def add_transaction(self, fecha, tipo, item, cantidad, precio, descripcion):
        monto_total = cantidad * precio
        self.excel_manager.add_transaction(fecha, tipo, item, cantidad, precio, monto_total, descripcion)

    def update_transaction(self, trans_id, item, cantidad, precio, descripcion):
        monto_total = cantidad * precio
        self.excel_manager.update_transaction(trans_id, item, cantidad, precio, monto_total, descripcion)

    def delete_transaction(self, trans_id):
        self.excel_manager.delete_transaction(trans_id)

    # Análisis y Resúmenes
    def get_dashboard_summary(self):
        df = self.excel_manager.get_transactions()
        if df.empty:
            return {"ingresos": 0, "egresos": 0, "saldo": 0}
            
        ingresos = df[df["Tipo"] == "Ingreso"]["MontoTotal"].sum()
        egresos = df[df["Tipo"] == "Egreso"]["MontoTotal"].sum()
        saldo = ingresos - egresos
        return {
            "ingresos": ingresos,
            "egresos": egresos,
            "saldo": saldo
        }

    # KPIs e Informes Visuales
    def get_kpi_ingresos_egresos(self):
        df = self.excel_manager.get_transactions()
        if df.empty: return (0, 0)
        ingresos = df[df["Tipo"] == "Ingreso"]["MontoTotal"].sum()
        egresos = df[df["Tipo"] == "Egreso"]["MontoTotal"].sum()
        return (ingresos, egresos)
        
    def get_kpi_top_productos(self, limit=5):
        df = self.excel_manager.get_transactions()
        if df.empty: return []
        ingresos = df[df["Tipo"] == "Ingreso"]
        if ingresos.empty: return []
        top = ingresos.groupby("Item")["MontoTotal"].sum().sort_values(ascending=True).tail(limit)
        return [(str(k), float(v)) for k,v in top.items()]
        
    def get_kpi_costos(self):
        df = self.excel_manager.get_transactions()
        if df.empty: return []
        egresos = df[df["Tipo"] == "Egreso"]
        if egresos.empty: return []
        costos = egresos.groupby("Item")["MontoTotal"].sum().sort_values(ascending=False)
        return [(str(k), float(v)) for k,v in costos.items()]
