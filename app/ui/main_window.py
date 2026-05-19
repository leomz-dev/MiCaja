import customtkinter as ctk
from tkinter import messagebox
from app.ui.theme import COLORS, SPACING
from app.ui.components import Sidebar, TopBar
from app.ui.views import (
    DashboardView,
    TransactionsView,
    ProductsView,
    ReportsView,
    SettingsView,
)
from app.ui.modals import TransactionModal, OperationPickerModal


class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        config = controller.get_config()
        self.app_name = config.get("NombreNegocio", "Mi Caja")
        self.user_name = "Leonardo"
        self._period = "Este Mes"
        self._search = ""
        self._current_view_key = "dashboard"

        self.title(f"{self.app_name} — Gestión Financiera")
        self.geometry("1280x800")
        self.minsize(1024, 700)
        self.configure(fg_color=COLORS["bg_main"])

        self._callbacks = {
            "open_modal": self.open_modal,
            "edit_transaction": self._edit_transaction,
            "go_transactions": lambda: self._navigate("transactions"),
            "refresh_all": self.refresh_ui,
        }

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self,
            self.app_name,
            on_navigate=self._navigate,
            on_new_operation=self._open_operation_picker,
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content_shell = ctk.CTkFrame(self, fg_color=COLORS["bg_main"], corner_radius=0)
        self.content_shell.grid(row=0, column=1, sticky="nsew")
        self.content_shell.grid_rowconfigure(1, weight=1)
        self.content_shell.grid_columnconfigure(0, weight=1)

        self.topbar = TopBar(
            self.content_shell,
            self.user_name,
            on_search=self._on_search,
            on_period_change=self._on_period_change,
        )
        self.topbar.grid(row=0, column=0, sticky="ew", padx=SPACING["container_pad"], pady=(24, 8))

        self.view_container = ctk.CTkFrame(self.content_shell, fg_color="transparent")
        self.view_container.grid(row=1, column=0, sticky="nsew", padx=SPACING["container_pad"], pady=(0, 24))
        self.view_container.grid_rowconfigure(0, weight=1)
        self.view_container.grid_columnconfigure(0, weight=1)

        self.views = {
            "dashboard": DashboardView(self.view_container, controller, self._callbacks),
            "transactions": TransactionsView(self.view_container, controller, self._callbacks),
            "products": ProductsView(self.view_container, controller, self._callbacks),
            "reports": ReportsView(self.view_container, controller),
            "settings": SettingsView(self.view_container, controller),
        }
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

        self._show_view("dashboard")
        self.refresh_ui()

    def _show_view(self, key):
        self._current_view_key = key
        for k, view in self.views.items():
            if k == key:
                view.grid()
            else:
                view.grid_remove()

    def _navigate(self, key):
        self._show_view(key)
        if hasattr(self, "sidebar"):
            self.sidebar._highlight(key)
        self.refresh_ui()

    def _on_search(self, query):
        self._search = query
        self.refresh_ui()

    def _on_period_change(self, period):
        self._period = period
        self.refresh_ui()

    def refresh_ui(self, *_args):
        period = self.topbar.get_period() if hasattr(self, "topbar") else self._period
        self._period = period
        for view in self.views.values():
            if hasattr(view, "refresh"):
                view.refresh(period=period, search=self._search)

    def _open_operation_picker(self):
        OperationPickerModal(
            self,
            on_ingreso=lambda: self.open_modal("Ingreso"),
            on_egreso=lambda: self.open_modal("Egreso"),
        )

    def open_modal(self, mode, transaction_data=None):
        TransactionModal(
            self, self.controller, mode,
            on_save_callback=self.refresh_ui,
            transaction_data=transaction_data,
        )

    def _edit_transaction(self, trans_id):
        t_data = self.controller.get_transaction(trans_id)
        if t_data:
            self.open_modal(t_data["Tipo"], transaction_data=t_data)
