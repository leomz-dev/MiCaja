# MiCaja - Gestión Financiera Minimalista 🚀

MiCaja es una solución integral de escritorio diseñada para la gestión contable y financiera de pequeños negocios. Con una interfaz moderna, oscura y de alto rendimiento, permite a los propietarios tomar el control total de sus flujos de caja, catálogos de productos y métricas operativas sin la complejidad de sistemas ERP pesados.

---

## ✨ Características Destacadas

### 📊 Dashboard Inteligente
- **Métricas en Tiempo Real**: Visualización instantánea de Saldo Actual, Ingresos y Egresos con tendencias comparativas.
- **Gráficas Operativas**: Balance semanal interactivo renderizado con Matplotlib para identificar picos de actividad.
- **Top de Productos**: Ranking visual de los artículos que más ingresos generan al negocio.
- **Acceso Rápido**: Botones directos para el ingreso de ventas y registro de gastos.

### 💼 Gestión de Transacciones
- **Historial Completo**: Tabla avanzada con filtros por tipo de operación y búsqueda global dinámica.
- **Edición Ágil**: Sistema de doble clic para modificar registros existentes y tecla *Suprimir* para eliminaciones rápidas.
- **Categorización Automática**: Uso de insignias visuales (Badges) para diferenciar ingresos de egresos de un vistazo.

### 📦 Catálogo y Productos
- **Control de Inventario**: Vista dedicada para gestionar productos de venta e ítems de gasto.
- **Valor del Catálogo**: Cálculo automático del valor referencial de tus productos disponibles.
- **Indicadores de Estado**: Barras de progreso visuales para monitorear el estado de los ítems en el catálogo.

### 🛠️ Configuración y Personalización
- **Identidad del Negocio**: Personalización del nombre de la empresa y símbolo de moneda.
- **Arquitectura Robusta**: Persistencia garantizada en Excel (`.xlsx`), permitiendo que tus datos sean tuyos y portátiles.

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue un patrón **MVC (Modelo-Vista-Controlador)** desacoplado para facilitar el mantenimiento y la escalabilidad:

```text
MiCaja/
├── app/
│   ├── controllers/    # Lógica de negocio y coordinación entre datos y UI.
│   ├── models/         # Gestión de persistencia (ExcelManager) y validaciones.
│   └── ui/             # Interfaz de Usuario modular:
│       ├── components/ # Widgets reutilizables (Sidebar, TopBar, KPI Cards, Badges).
│       ├── views/      # Pantallas principales (Dashboard, Transactions, Products, Reports, Settings).
│       ├── theme.py    # Definición global de colores, fuentes y espaciado.
│       └── modals.py   # Ventanas emergentes interactivas para formularios.
├── data/               # Directorio local de la base de datos Excel.
├── main.py             # Punto de entrada optimizado.
└── requirements.txt    # Dependencias del ecosistema Python.
```

---

## 🛠️ Tecnologías Utilizadas

- **Core**: Python 3.10+
- **UI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Interfaz moderna con soporte nativo de modo oscuro.
- **Data Engine**: [Pandas](https://pandas.pydata.org/) & [OpenPyXL](https://openpyxl.readthedocs.io/) - Procesamiento eficiente de hojas de cálculo.
- **Analytics**: [Matplotlib](https://matplotlib.org/) - Generación de gráficas embebidas en la UI.

---

## 🚀 Instalación y Uso

### Configuración del Entorno
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/micaja.git
   cd micaja
   ```
2. **Crear entorno virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```
3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Lanzar aplicación**:
   ```bash
   python main.py
   ```

### Generación de Ejecutable
Para crear una versión portable para Windows:
```bash
build.cmd
```
El archivo resultante estará disponible en la carpeta `dist/`.

---

## 🔒 Privacidad y Datos
MiCaja prioriza la soberanía de los datos. Toda la información se almacena localmente en `data/micaja_data.xlsx`. No hay procesos en segundo plano ni envío de información a servidores externos.

*Desarrollado con ❤️ por Leonardo Meza*
