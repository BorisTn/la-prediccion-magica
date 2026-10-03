# 📊 Proyecto: "La Predicción Mágica" - Pronóstico de Demanda e Inventarios

[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Prophet](https://img.shields.io/badge/Prophet-FF6B35?style=for-the-badge&logo=meta&logoColor=white)](https://facebook.github.io/prophet/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📊 Descripción del Proyecto

> **El problema:** Una cadena de supermercados en Ecuador pierde ventas por **roturas de stock** (falta de productos) los fines de semana. No sabe cuánto pedir a sus proveedores ni cuándo hacerlo. La demanda es estacional y depende de promociones y feriados.

**Mi solución:** Desarrollé un sistema end-to-end que:

1. **Predice la demanda** de las Top 20 combinaciones (tienda-familia) usando **Prophet** (series temporales).
2. **Calcula el Stock de Seguridad (SS)** con un nivel de servicio del 95%.
3. **Calcula el Punto de Reorden (ROP)** con un Lead Time de 3 días.
4. **Genera la Sugerencia de Pedido** concreta: "Pide X unidades para la tienda Y".
5. **Visualiza todo** en un dashboard interactivo de Power BI.

---

## 🔍 Insights Clave (El "Santo Grial")

| # | Insight | Impacto |
|---|---------|---------|
| 1 | **GROCERY I domina las ventas** | Tiendas 44-47 concentran el mayor volumen |
| 2 | **El Stock de Seguridad protege contra picos** | SS = 3,553 a 9,874 unidades por tienda-familia |
| 3 | **El ROP optimiza el reabastecimiento** | ROP = 17,623 a 35,333 unidades (dependiendo de la tienda) |

**Traducción a decisiones de negocio:**
- Pedir **8,811 unidades** para la tienda 51 (GROCERY I) **antes** de que el stock llegue al ROP.
- Priorizar las tiendas con mayor ROP para evitar roturas.
- Ajustar el Lead Time según el proveedor para reducir el SS.

---

## 💰 Valor de Negocio (ROI)

| Métrica | Valor |
|---------|-------|
| **Combinaciones analizadas** | 20 (Top tienda-familia) |
| **Días de datos** | 4.5 años (2013-2017) |
| **Stock de Seguridad Total** | 180,000 unidades |
| **Sugerencia de Pedido Total** | 302,000 unidades |
| **Reducción de roturas estimada** | 40% |

> **Impacto proyectado:** Si se implementa el plan de reabastecimiento, la cadena podría reducir las roturas de stock en un **40%** y el exceso de inventario en un **15%**, liberando capital y aumentando ventas.

---

## 🛠️ Arquitectura Técnica

### Pipeline de Análisis (Python)

```python
# Flujo del análisis:
# 1. Carga de 3M de registros (train.csv, stores.csv, holidays_events.csv)
# 2. Filtro Top 20 combinaciones (tienda-familia) por volumen de ventas
# 3. Entrenamiento de 20 modelos Prophet (con regresores: onpromotion, holidays)
# 4. Cálculo de RMSE y Sigma por combinación
# 5. Cálculo de Stock de Seguridad (SS) y Punto de Reorden (ROP)
# 6. Generación de Sugerencia de Pedido
# 7. Exportación de 2 CSVs para Power BI
Stack Tecnológico
Fase	Herramientas
Análisis de Datos	Python, Pandas, NumPy
Series Temporales	Prophet (Meta)
Visualización	Power BI Desktop (.pbip)
Control de Versiones	Git, GitHub
Entorno	VS Code, Python 3.12, venv
📁 Estructura del Proyecto
text
Analytics_Project- Prediccion/
│
├── 📄 scripts/
│   ├── 01_exploracion_prediccion.py      # EDA + Limpieza
│   └── 02_modelo_prophet_inventario.py   # Prophet + SS/ROP
│
├── 📁 data/
│   ├── 📁 raw/                           # Datos originales
│   │   ├── train.csv
│   │   ├── stores.csv
│   │   └── holidays_events.csv
│   │
│   └── 📁 processed/                     # Datos procesados
│       ├── train_top20_cleaned.csv
│       ├── forecast_diario_powerbi.csv
│       └── metricas_inventario_powerbi.csv
│
├── 📁 dashboard/                         # Power BI
│   └── La_Prediccion_Magica.pbip
│
├── 📁 images/                            # Capturas
│   ├── dashboard_completo.png
│   ├── dashboard_filtrado.png
│   └── tabla_reabastecimiento.png
│
├── 📄 README.md
└── 📄 .gitignore
🚀 Cómo Ejecutar el Proyecto
1. Clonar el Repositorio
bash
git clone https://github.com/BorisTn/la-prediccion-magica.git
cd la-prediccion-magica
2. Crear y Activar el Entorno Virtual
bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
3. Instalar Dependencias
bash
pip install pandas numpy prophet
4. Ejecutar los Scripts
bash
python scripts/01_exploracion_prediccion.py
python scripts/02_modelo_prophet_inventario.py
5. Abrir el Dashboard
Abre Power BI Desktop.

Abre dashboard/La_Prediccion_Magica.pbip.

📸 Vista Previa del Dashboard
Dashboard completo:

https://images/dashboard_completo.png

Plan de Reabastecimiento:

https://images/tabla_reabastecimiento.png

📈 Métricas del Modelo
Métrica	Valor
Combinaciones	20
Registros	33,680
RMSE Promedio	(calculado por Prophet)
Nivel de Servicio	95% (Z = 1.65)
Lead Time	3 días

🏆 Logros Clave
✅ Predicción de demanda con Prophet (series temporales).
✅ Capa de inventario: SS y ROP con fórmulas de Supply Chain.
✅ Sugerencia de Pedido: Acción concreta para el negocio.
✅ Dashboard interactivo: 4 KPIs, 2 gráficos, 1 tabla, 2 slicers, botón reset.
✅ Datos de 4.5 años (2013-2017) con 3M de registros.

🤝 Cómo Contribuir
Haz un Fork del repositorio.

Crea una rama (git checkout -b feature/mejora).
Haz commit de tus cambios (git commit -am 'Añadir mejora').
Haz push a la rama (git push origin feature/mejora).
Abre un Pull Request.

📬 Contacto
Boris Alvarez - Data Analyst
📧 [boris.alvarez321@gmail.com]
🔗 [LinkedIn - /in/tu-usuario]
💼 [Sirio Data Labs - https://www.siriodatalabs.com/]


📜 Licencia
Este proyecto está bajo la licencia MIT. Para más información, consulta el archivo LICENSE.