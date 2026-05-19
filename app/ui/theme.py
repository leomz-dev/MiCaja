"""Design tokens — Mi Caja (desing/DESIGN.md + prd.md)."""

COLORS = {
    "bg_main": "#1A1A1A",
    "bg_sidebar": "#1E1E1E",
    "bg_card": "#2D2D2D",
    "bg_card_alt": "#252525",
    "bg_input": "#1E1E1E",
    "primary": "#00D09C",
    "primary_hover": "#00B88A",
    "primary_light": "#003828",
    "danger": "#FF5C5C",
    "danger_hover": "#FF4747",
    "danger_light": "#3d1a1a",
    "accent_blue": "#4DA6FF",
    "warning": "#FFB84D",
    "text_primary": "#FFFFFF",
    "text_secondary": "#A0A0A0",
    "text_muted": "#6B6B6B",
    "border": "#3A3A3A",
    "border_subtle": "#2A2A2A",
    "sidebar_active_bg": "#2A3D35",
    "tree_bg": "#252525",
    "tree_heading": "#333333",
    "tree_selected": "#00D09C",
}

SPACING = {
    "sidebar_width": 260,
    "container_pad": 32,
    "card_radius": 12,
    "btn_radius": 10,
    "badge_radius": 20,
}

FONTS = {
    "display_lg": ("Inter", 32, "bold"),
    "display_md": ("Inter", 24, "bold"),
    "title": ("Inter", 18, "bold"),
    "body": ("Inter", 14),
    "body_sm": ("Inter", 13),
    "label_sm": ("Inter", 11, "bold"),
    "caption": ("Inter", 11),
    "mono": ("Consolas", 13),
    "kpi_value": ("Inter", 28, "bold"),
    "kpi_label": ("Inter", 11),
}

NAV_ITEMS = [
    ("dashboard", "◫", "Dashboard"),
    ("transactions", "⇄", "Transacciones"),
    ("products", "▣", "Productos"),
    ("reports", "▤", "Reportes"),
    ("settings", "⚙", "Ajustes"),
]

PERIOD_OPTIONS = ["Este Mes", "Mes Anterior", "Todo el tiempo"]
