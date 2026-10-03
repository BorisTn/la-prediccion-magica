# 01_exploracion_prediccion.py
# Proyecto: La Predicción Mágica - Pronóstico de Demanda
# Objetivo: Cargar, limpiar y seleccionar Top 20 combinaciones (tienda-familia)

import pandas as pd
import numpy as np
from pathlib import Path

def cargar_y_limpiar_datos():
    print("=" * 60)
    print("📦 FASE 1 & 2: EDA Y SELECCIÓN DE TOP COMBINACIONES")
    print("=" * 60)
    
    # Detectar la raíz del proyecto (sube un nivel desde scripts/)
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_raw = ruta_base / 'data' / 'raw'
    ruta_processed = ruta_base / 'data' / 'processed'
    ruta_processed.mkdir(parents=True, exist_ok=True)
    
    # Verificar rutas
    print(f"\n📂 Ruta raw: {ruta_raw}")
    print(f"📂 Ruta processed: {ruta_processed}")
    
    # 1. Cargar datasets
    print("\n📂 Cargando archivos...")
    try:
        train = pd.read_csv(ruta_raw / 'train.csv')
        stores = pd.read_csv(ruta_raw / 'stores.csv')
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"   Verifica que los archivos estén en: {ruta_raw}")
        return
    
    
    
    # Convertir fechas
    train['date'] = pd.to_datetime(train['date'])
    
    print(f"  ✅ Registros totales en train: {len(train):,}")
    print(f"  ✅ Rango de fechas: {train['date'].min().date()} a {train['date'].max().date()}")
    print(f"  ✅ Columnas disponibles: {train.columns.tolist()}")
    
    # 2. Identificar las Top 20 combinaciones (store_nbr + family) por volumen de ventas
    print("\n📊 Identificando Top 20 combinaciones (Tienda + Familia)...")
    top_combinaciones = (
        train.groupby(['store_nbr', 'family'])['sales']
        .sum()
        .reset_index()
        .sort_values(by='sales', ascending=False)
        .head(20)
    )
    
    print("\n🏆 Top 5 Combinaciones con mayor volumen:")
    print(top_combinaciones.head().to_string(index=False))
    
    # 3. Filtrar dataset original solo con esas Top 20 combinaciones
    train_top = train.merge(
        top_combinaciones[['store_nbr', 'family']], 
        on=['store_nbr', 'family'], 
        how='inner'
    )
    
    # 4. Enriquecer con información de tiendas
    train_top = train_top.merge(stores, on='store_nbr', how='left')
    
    # 5. TRATAMIENTO DE VALORES FALTANTES Y DÍAS SIN VENTA
    print("\n🧹 Limpiando datos...")
    
    # Rellenar nulos en sales con 0
    train_top['sales'] = train_top['sales'].fillna(0)
    
    # CRÍTICO: NO eliminar días con ventas = 0
    # Prophet necesita continuidad temporal para aprender patrones de cierre
    dias_cero = (train_top['sales'] == 0).sum()
    print(f"  ✅ Días con ventas = 0 detectados: {dias_cero:,} (se conservan para mantener la secuencia diaria continua)")
    
    # 6. FEATURE ENGINEERING
    print("\n🔧 Creando features adicionales...")
    
    # Variable is_weekend (útil para análisis y dashboard, no como regresor principal)
    train_top['is_weekend'] = train_top['date'].dt.dayofweek.isin([5, 6]).astype(int)
    print(f"  ✅ Variable 'is_weekend' creada (para análisis y dashboard)")
    
    # Verificar que onpromotion esté presente
    if 'onpromotion' in train_top.columns:
        print(f"  ✅ Variable 'onpromotion' presente (regresor clave para Prophet)")
    else:
        print(f"  ⚠️ Variable 'onpromotion' NO encontrada")
    
    # 7. GUARDAR
    output_path = ruta_processed / 'train_top20_cleaned.csv'
    train_top.to_csv(output_path, index=False)
    
    print(f"\n✅ Datos filtrados y guardados exitosamente en: {output_path}")
    print(f"  - Total de registros a procesar en Prophet: {len(train_top):,}")
    print(f"  - Total de combinaciones únicas: {train_top.groupby(['store_nbr', 'family']).ngroups}")
    print("=" * 60)

if __name__ == "__main__":
    cargar_y_limpiar_datos()