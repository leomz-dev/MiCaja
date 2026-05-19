from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
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

    # --- Filtros por periodo ---

    def _period_bounds(self, period):
        today = datetime.now().date()
        if period == "Este Mes":
            start = today.replace(day=1)
            end = today
        elif period == "Mes Anterior":
            first_this = today.replace(day=1)
            end = first_this - relativedelta(days=1)
            start = end.replace(day=1)
        else:
            return None, None
        return start, end

    def _filter_df_period(self, df, period):
        if df.empty or period == "Todo el tiempo":
            return df
        start, end = self._period_bounds(period)
        if start is None:
            return df
        dates = pd.to_datetime(df["Fecha"])
        mask = (dates.dt.date >= start) & (dates.dt.date <= end)
        return df.loc[mask]

    def get_filtered_transactions(self, period="Todo el tiempo", search="", tipo=None):
        df = self.excel_manager.get_transactions()
        if df.empty:
            return []
        df = self._filter_df_period(df, period)
        if search:
            q = search.lower()
            mask = (
                df["Item"].astype(str).str.lower().str.contains(q, na=False)
                | df["Descripcion"].astype(str).str.lower().str.contains(q, na=False)
            )
            df = df.loc[mask]
        if tipo and tipo != "Todos":
            df = df.loc[df["Tipo"] == tipo]
        df = df.sort_values(by="Id", ascending=False)
        return df.to_dict("records")

    # Análisis y Resúmenes
    def get_dashboard_summary(self, period="Todo el tiempo"):
        df = self.excel_manager.get_transactions()
        df = self._filter_df_period(df, period)
        if df.empty:
            return {
                "ingresos": 0, "egresos": 0, "saldo": 0,
                "count_ingresos": 0, "count_egresos": 0,
            }
        ing_df = df[df["Tipo"] == "Ingreso"]
        egr_df = df[df["Tipo"] == "Egreso"]
        ingresos = ing_df["MontoTotal"].sum()
        egresos = egr_df["MontoTotal"].sum()
        return {
            "ingresos": ingresos,
            "egresos": egresos,
            "saldo": ingresos - egresos,
            "count_ingresos": len(ing_df),
            "count_egresos": len(egr_df),
        }

    def get_saldo_trend_pct(self, period="Este Mes"):
        """Variación % del saldo vs periodo anterior equivalente."""
        current = self.get_dashboard_summary(period)
        prev_period = "Mes Anterior" if period == "Este Mes" else "Todo el tiempo"
        if period == "Mes Anterior":
            return None
        previous = self.get_dashboard_summary(prev_period)
        prev_saldo = previous["saldo"]
        if prev_saldo == 0:
            return None
        return ((current["saldo"] - prev_saldo) / abs(prev_saldo)) * 100

    # KPIs e Informes Visuales
    def get_kpi_ingresos_egresos(self, period="Todo el tiempo"):
        summary = self.get_dashboard_summary(period)
        return summary["ingresos"], summary["egresos"]

    def get_kpi_costos(self, period="Todo el tiempo"):
        df = self.excel_manager.get_transactions()
        df = self._filter_df_period(df, period)
        if df.empty:
            return []
        egresos = df[df["Tipo"] == "Egreso"]
        if egresos.empty:
            return []
        costos = egresos.groupby("Item")["MontoTotal"].sum().sort_values(ascending=False)
        return [(str(k), float(v)) for k, v in costos.items()]

    def get_kpi_top_productos(self, limit=5, period="Todo el tiempo"):
        df = self.excel_manager.get_transactions()
        df = self._filter_df_period(df, period)
        if df.empty:
            return []
        ingresos = df[df["Tipo"] == "Ingreso"]
        if ingresos.empty:
            return []
        top = ingresos.groupby("Item")["MontoTotal"].sum().sort_values(ascending=False).head(limit)
        total = top.sum() or 1
        return [(str(k), float(v), float(v) / total * 100) for k, v in top.items()]

    def get_weekly_balance(self, period="Este Mes"):
        """Ingresos y egresos agrupados por semana del mes."""
        df = self.excel_manager.get_transactions()
        df = self._filter_df_period(df, period)
        if df.empty:
            return []
        df = df.copy()
        df["FechaDt"] = pd.to_datetime(df["Fecha"])
        df["Semana"] = ((df["FechaDt"].dt.day - 1) // 7) + 1
        weeks = sorted(df["Semana"].unique())
        result = []
        for w in weeks[:4]:
            wdf = df[df["Semana"] == w]
            ing = wdf[wdf["Tipo"] == "Ingreso"]["MontoTotal"].sum()
            egr = wdf[wdf["Tipo"] == "Egreso"]["MontoTotal"].sum()
            result.append((f"Sem {int(w)}", float(ing), float(egr)))
        return result

    def get_catalog_summary(self):
        items = self.get_all_catalog()
        ingresos = [i for i in items if i["Tipo"] == "Ingreso"]
        egresos = [i for i in items if i["Tipo"] == "Egreso"]
        valor = sum(i["PrecioPredeterminado"] for i in ingresos)
        return {
            "total_productos": len(ingresos),
            "total_gastos_cat": len(egresos),
            "valor_catalogo": valor,
            "items": items,
        }
