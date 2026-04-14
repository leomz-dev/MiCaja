import os
import pandas as pd
from datetime import datetime, timedelta

class ExcelManager:
    def __init__(self, file_path="data/micaja_data.xlsx"):
        self.file_path = file_path
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        """Inicializa el archivo de datos si no existe."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                # Transacciones iniciales
                today = datetime.now()
                initial_trans = [
                    {"Id": 1, "Fecha": (today - timedelta(days=20)).strftime("%Y-%m-%d"), "Tipo": "Egreso", "Item": "Arriendo Locales", "Cantidad": 1, "PrecioUnitario": 1200000.0, "MontoTotal": 1200000.0, "Descripcion": "Pago mes actual"},
                    {"Id": 2, "Fecha": (today - timedelta(days=19)).strftime("%Y-%m-%d"), "Tipo": "Egreso", "Item": "Servicios Públicos", "Cantidad": 1, "PrecioUnitario": 300000.0, "MontoTotal": 300000.0, "Descripcion": "Luz y Agua"},
                    {"Id": 3, "Fecha": (today - timedelta(days=15)).strftime("%Y-%m-%d"), "Tipo": "Egreso", "Item": "Carne x10", "Cantidad": 20, "PrecioUnitario": 15000.0, "MontoTotal": 300000.0, "Descripcion": "Stock fin de semana"},
                    {"Id": 4, "Fecha": (today - timedelta(days=14)).strftime("%Y-%m-%d"), "Tipo": "Ingreso", "Item": "Hamburguesa Especial", "Cantidad": 100, "PrecioUnitario": 20000.0, "MontoTotal": 2000000.0, "Descripcion": "Ventas fin de semana"},
                    {"Id": 5, "Fecha": (today - timedelta(days=10)).strftime("%Y-%m-%d"), "Tipo": "Ingreso", "Item": "Salchipapa", "Cantidad": 50, "PrecioUnitario": 18000.0, "MontoTotal": 900000.0, "Descripcion": "Viernes"},
                    {"Id": 6, "Fecha": (today - timedelta(days=2)).strftime("%Y-%m-%d"), "Tipo": "Ingreso", "Item": "Hamburguesa Sencilla", "Cantidad": 60, "PrecioUnitario": 15000.0, "MontoTotal": 900000.0, "Descripcion": "Ventas diarias"}
                ]
                df_trans = pd.DataFrame(initial_trans)
                df_trans.to_excel(writer, sheet_name="Transacciones", index=False)
                
                # Catálogo Base
                default_catalog = [
                    {"Id": 1, "Nombre": "Hamburguesa Sencilla", "Tipo": "Ingreso", "PrecioPredeterminado": 15000.0},
                    {"Id": 2, "Nombre": "Hamburguesa Especial", "Tipo": "Ingreso", "PrecioPredeterminado": 20000.0},
                    {"Id": 3, "Nombre": "Perro Caliente", "Tipo": "Ingreso", "PrecioPredeterminado": 10000.0},
                    {"Id": 4, "Nombre": "Salchipapa", "Tipo": "Ingreso", "PrecioPredeterminado": 18000.0},
                    {"Id": 5, "Nombre": "Gaseosa 400ml", "Tipo": "Ingreso", "PrecioPredeterminado": 4000.0},
                    {"Id": 6, "Nombre": "Jugo Natural", "Tipo": "Ingreso", "PrecioPredeterminado": 5000.0},
                    {"Id": 7, "Nombre": "Arriendo Locales", "Tipo": "Egreso", "PrecioPredeterminado": 1200000.0},
                    {"Id": 8, "Nombre": "Servicios Públicos", "Tipo": "Egreso", "PrecioPredeterminado": 300000.0},
                    {"Id": 9, "Nombre": "Nómina Empleado", "Tipo": "Egreso", "PrecioPredeterminado": 50000.0},
                    {"Id": 10, "Nombre": "Pan de Hamburguesa x12", "Tipo": "Egreso", "PrecioPredeterminado": 6000.0},
                    {"Id": 11, "Nombre": "Carne x10", "Tipo": "Egreso", "PrecioPredeterminado": 15000.0},
                    {"Id": 12, "Nombre": "Queso Tajado x50", "Tipo": "Egreso", "PrecioPredeterminado": 20000.0},
                    {"Id": 13, "Nombre": "Papas Fritas 2kg", "Tipo": "Egreso", "PrecioPredeterminado": 12000.0},
                    {"Id": 14, "Nombre": "Salsas y Aderezos", "Tipo": "Egreso", "PrecioPredeterminado": 10000.0},
                ]
                df_cat = pd.DataFrame(default_catalog)
                df_cat.to_excel(writer, sheet_name="Catalogo", index=False)
                
                # Configuración inicial
                default_config = [
                    {"Clave": "NombreNegocio", "Valor": "MiCaja"},
                    {"Clave": "Moneda", "Valor": "$"}
                ]
                df_config = pd.DataFrame(default_config)
                df_config.to_excel(writer, sheet_name="Configuracion", index=False)

    def _read_sheet(self, sheet_name):
        return pd.read_excel(self.file_path, sheet_name=sheet_name)
    
    def _write_shets(self, sheet_data_dict):
        with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='w') as writer:
            for name, df in sheet_data_dict.items():
                df.to_excel(writer, sheet_name=name, index=False)

    def _write_sheet_only(self, target_sheet_name, new_df):
        all_sheets = pd.read_excel(self.file_path, sheet_name=None)
        all_sheets[target_sheet_name] = new_df
        self._write_shets(all_sheets)

    # --- Transacciones ---
    
    def get_transactions(self):
        df = self._read_sheet("Transacciones")
        if not df.empty:
            df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime('%Y-%m-%d')
        return df

    def get_transaction(self, trans_id):
        df = self._read_sheet("Transacciones")
        row = df[df["Id"] == trans_id]
        if not row.empty:
            return row.iloc[0]
        return None

    def add_transaction(self, fecha, tipo, item, cantidad, precio_unitario, monto_total, descripcion):
        df = self._read_sheet("Transacciones")
        new_id = 1 if df.empty else df["Id"].max() + 1
        new_row = pd.DataFrame([{
            "Id": new_id,
            "Fecha": fecha,
            "Tipo": tipo,
            "Item": item,
            "Cantidad": int(cantidad),
            "PrecioUnitario": float(precio_unitario),
            "MontoTotal": float(monto_total),
            "Descripcion": descripcion
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        self._write_sheet_only("Transacciones", df)

    def update_transaction(self, trans_id, item, cantidad, precio_unitario, monto_total, descripcion):
        df = self._read_sheet("Transacciones")
        idx = df.index[df["Id"] == trans_id]
        if not idx.empty:
            df.loc[idx, "Item"] = item
            df.loc[idx, "Cantidad"] = int(cantidad)
            df.loc[idx, "PrecioUnitario"] = float(precio_unitario)
            df.loc[idx, "MontoTotal"] = float(monto_total)
            df.loc[idx, "Descripcion"] = descripcion
            self._write_sheet_only("Transacciones", df)

    def delete_transaction(self, trans_id):
        df = self._read_sheet("Transacciones")
        df = df[df["Id"] != trans_id]
        self._write_sheet_only("Transacciones", df)

    # --- Catálogo ---
    def get_catalog(self):
        return self._read_sheet("Catalogo")

    def add_catalog_item(self, nombre, tipo, precio):
        df = self._read_sheet("Catalogo")
        new_id = 1 if df.empty else int(df["Id"].max()) + 1
        new_row = pd.DataFrame([{
            "Id": new_id,
            "Nombre": nombre,
            "Tipo": tipo,
            "PrecioPredeterminado": float(precio)
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        self._write_sheet_only("Catalogo", df)

    def delete_catalog_item(self, cat_id):
        df = self._read_sheet("Catalogo")
        df = df[df["Id"] != cat_id]
        self._write_sheet_only("Catalogo", df)

    # --- Configuración ---
    def get_config(self):
        df = self._read_sheet("Configuracion")
        return dict(zip(df["Clave"], df["Valor"]))
