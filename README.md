# MiCaja - Gestión Contable 

MiCaja es una aplicación de escritorio diseñada para la gestión contable simplificada de pequeños negocios. Ofrece una interfaz moderna, oscura y minimalista para el registro de ingresos y egresos, visualización de métricas clave y persistencia de datos local mediante Excel.

## 🚀 Características Principales

- **Panel de Control Intuitivo**: Visualización inmediata del saldo actual, ingresos y egresos totales.
- **Registro Rápido**: Modales optimizados para ingresar ventas o registrar gastos en segundos.
- **Gestión de Catálogo**: Sistema de productos y servicios preestablecidos para agilizar la entrada de datos.
- **Métricas Visuales (KPIs)**: Gráficas interactivas que muestran el balance operativo, distribución de costos y top de ventas.
- **Persistencia en Excel**: Todos los datos se guardan en un archivo `.xlsx` local, permitiendo la portabilidad y fácil manipulación externa de la información.
- **Modo Offline**: No requiere conexión a internet para funcionar.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.x
- **Interfaz Gráfica**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (una evolución estética de Tkinter).
- **Procesamiento de Datos**: [Pandas](https://pandas.pydata.org/) y [OpenPyXL](https://openpyxl.readthedocs.io/).
- **Visualización**: [Matplotlib](https://matplotlib.org/).
- **Empaquetado**: [PyInstaller](https://pyinstaller.org/).

## 📂 Estructura del Proyecto

```text
MiCaja/
├── app/
│   ├── controllers/    # Lógica de negocio y puentes entre UI y Modelos.
│   ├── models/         # Gestión de persistencia y acceso a datos (Excel).
│   └── ui/             # Componentes de la interfaz de usuario y modales.
├── data/               # Directorio donde se almacena la base de datos Excel.
├── build.cmd           # Script para generar el ejecutable de Windows.
├── main.py             # Punto de entrada de la aplicación.
└── requirements.txt    # Dependencias del proyecto.
```

## ⚙️ Cómo Funciona

### 1. Modelo de Datos
La aplicación utiliza un archivo llamado `micaja_data.xlsx` ubicado en la carpeta `data/`. Este archivo contiene tres hojas principales:
- **Transacciones**: Historial completo de movimientos con ID, fecha, tipo, item, cantidad y montos.
- **Catalogo**: Lista de productos/servicios con sus precios sugeridos.
- **Configuracion**: Ajustes generales como el nombre del negocio y el símbolo de moneda.

### 2. Flujo de Usuario
- Al iniciar, el `ExcelManager` verifica la existencia del archivo de datos. Si no existe, lo inicializa con valores base.
- El usuario puede registrar un **Ingreso** (selecciona un producto del catálogo, define cantidad y el sistema calcula el total) o un **Egreso** (gastos operativos, nómina, etc.).
- La tabla de movimientos en la ventana principal muestra los últimos 20 registros, permitiendo editarlos con doble click o eliminarlos con la tecla `Suprimir`.

### 3. Visualización de Resultados
Al pulsar en **Métricas**, se genera un panel dinámico usando Matplotlib que analiza los datos en tiempo real para mostrar:
- Balances operativos (Barras).
- Estructura de gastos por categoría (Pastel).
- Productos más vendidos por volumen de ingresos.

## 📦 Instalación y Ejecución

### Para desarrolladores:
1. Clonar el repositorio.
2. Crear un entorno virtual: `python -m venv .venv`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `python main.py`

### Para generar el Ejecutable (.exe):
Simplemente ejecute el archivo `build.cmd`. El resultado aparecerá en la carpeta `dist/MiCaja`.

---
*Desarrollado por Leonardo Meza*
