# 02_modelo_prophet_inventario.py
# Proyecto: La Predicción Mágica - Pronóstico de Demanda e Inventarios
# Objetivo: Entrenar Prophet en Top 20 combinaciones y calcular SS, ROP y Sugerencia de Pedido

import pandas as pd
import numpy as np
from pathlib import Path
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')


def ejecutar_prophet_y_supply_chain():
    print("=" * 70)
    print("🚀 FASE 3 Y 4: MODELADO CON PROPHET Y MOTOR DE DECISIÓN DE INVENTARIOS")
    print("=" * 70)

    ruta_raw = Path('data/raw')
    ruta_processed = Path('data/processed')

    # 1. CARGAR DATOS PROCESADOS Y FESTIVOS
    print("\n📂 Cargando datos filtrados y festivos...")
    try:
        df = pd.read_csv(ruta_processed / 'train_top20_cleaned.csv')
        holidays_raw = pd.read_csv(ruta_raw / 'holidays_events.csv')
    except FileNotFoundError as e:
        print(f"❌ Error: Verifica que existan los archivos en data/. Detalle: {e}")
        return

    df['date'] = pd.to_datetime(df['date'])

    # Formatear festivos para Prophet
    holidays_raw['date'] = pd.to_datetime(holidays_raw['date'])
    holidays_prophet = holidays_raw[['date', 'type']].rename(
        columns={'date': 'ds', 'type': 'holiday'}
    )

    # 2. PARÁMETROS DE SUPPLY CHAIN
    LEAD_TIME_DIAS = 3        # Tiempo de reabastecimiento del proveedor
    NIVEL_SERVICIO_Z = 1.65   # Z = 1.65 representa un Nivel de Servicio del 95%
    HORIZONTE_DIAS = 30       # Ventana de pronóstico futuro

    combinaciones = df.groupby(['store_nbr', 'family']).size().reset_index()[['store_nbr', 'family']]
    total_combs = len(combinaciones)
    print(f"\n⚙️ Configuración: {total_combs} combinaciones | Lead Time: {LEAD_TIME_DIAS} días | Z: {NIVEL_SERVICIO_Z} (95%)")

    resultados_forecast = []
    metricas_inventario = []

    # 3. BUCLE DE ENTRENAMIENTO Y CÁLCULOS DE INVENTARIO
    print("\n🤖 Entrenando modelos Prophet...")

    for idx, row in combinaciones.iterrows():
        tienda = row['store_nbr']
        familia = row['family']

        df_comb = df[(df['store_nbr'] == tienda) & (df['family'] == familia)].sort_values('date')

        df_prophet = df_comb[['date', 'sales', 'onpromotion']].rename(
            columns={'date': 'ds', 'sales': 'y'}
        )

        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            holidays=holidays_prophet
        )

        if 'onpromotion' in df_prophet.columns:
            model.add_regressor('onpromotion')

        model.fit(df_prophet)

        # Generar dataframe futuro
        future = model.make_future_dataframe(periods=HORIZONTE_DIAS)
        
        # Manejo de promociones futuras: Se asume 0 (escenario base sin promociones programadas)
        if 'onpromotion' in df_prophet.columns:
            future = future.merge(df_prophet[['ds', 'onpromotion']], on='ds', how='left')
            future['onpromotion'] = future['onpromotion'].fillna(0)

        forecast = model.predict(future)

        # Evaluación del error histórico
        eval_df = df_prophet.merge(forecast[['ds', 'yhat']], on='ds', how='inner')
        eval_df['residual'] = eval_df['y'] - eval_df['yhat']
        rmse = np.sqrt(np.mean(eval_df['residual']**2))
        sigma_demanda = eval_df['y'].std()

        # FORMULACIÓN DE INVENTARIO Y REABASTECIMIENTO
        # Stock de Seguridad (SS)
        stock_seguridad = NIVEL_SERVICIO_Z * sigma_demanda * np.sqrt(LEAD_TIME_DIAS)

        # Demanda esperada durante el Lead Time (Garantizando orden cronológico)
        forecast_futuro = (
            forecast[forecast['ds'] > df_prophet['ds'].max()]
            .sort_values('ds')
            .head(LEAD_TIME_DIAS)
        )
        demanda_lead_time = forecast_futuro['yhat'].clip(lower=0).sum()

        # Punto de Reorden (ROP)
        punto_reorden = demanda_lead_time + stock_seguridad

        # Simulación de Stock Actual y Sugerencia Operativa de Pedido
        stock_actual_simulado = int(np.ceil(punto_reorden * 0.5))
        sugerencia_pedido = max(0, int(np.ceil(punto_reorden)) - stock_actual_simulado)

        metricas_inventario.append({
            'store_nbr': tienda,
            'family': familia,
            'RMSE': round(rmse, 2),
            'Sigma_Demanda': round(sigma_demanda, 2),
            'Stock_Seguridad_SS': int(np.ceil(stock_seguridad)),
            'Demanda_LeadTime': int(np.ceil(demanda_lead_time)),
            'Punto_Reorden_ROP': int(np.ceil(punto_reorden)),
            'Stock_Actual_Simulado': stock_actual_simulado,
            'Sugerencia_Pedido': sugerencia_pedido
        })

        # Estructuración de datos diarios para Power BI
        forecast_out = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        forecast_out['store_nbr'] = tienda
        forecast_out['family'] = familia
        forecast_out['yhat'] = forecast_out['yhat'].clip(lower=0)

        forecast_out = forecast_out.merge(df_prophet[['ds', 'y']], on='ds', how='left')
        resultados_forecast.append(forecast_out)

        print(f"  [Progress {idx+1}/{total_combs}] Tienda {tienda} - {familia} | ROP: {int(np.ceil(punto_reorden))} | Pedido Sugerido: {sugerencia_pedido}")

    # 4. EXPORTAR ARCHIVOS ETL
    print("\n💾 Exportando Datasets Procesados...")

    df_final_forecast = pd.concat(resultados_forecast, ignore_index=True)
    df_final_metricas = pd.DataFrame(metricas_inventario)

    df_final_forecast.to_csv(ruta_processed / 'forecast_diario_powerbi.csv', index=False)
    df_final_metricas.to_csv(ruta_processed / 'metricas_inventario_powerbi.csv', index=False)

    print("  ✅ data/processed/forecast_diario_powerbi.csv")
    print("  ✅ data/processed/metricas_inventario_powerbi.csv")

    print("\n" + "=" * 70)
    print("✨ FASE 3 Y 4 FINALIZADAS CON ÉXITO")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_prophet_y_supply_chain()