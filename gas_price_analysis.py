#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 14:05:43 2025

@author: abilezca
"""

"""
Análisis de precios de gas natural en Argentina (2019-2025)

Este script realiza:
- Exploración básica del dataset
- Consultas por cuenca y año
- Análisis estadístico de precios por tipo
- Visualización temporal de precios
- Análisis comparativo entre tipos de precios

Autor: Abigail Lezcano
"""

import pandas as pd
import matplotlib.pyplot as plt



# CARGA Y EXPLORACIÓN


def cargar_dataset(ruta_archivo):
    """
    Carga el dataset desde un archivo CSV.
    """
    df = pd.read_csv(ruta_archivo)
    return df




def explorar_dataset(df):
    """
    Realiza exploración básica del dataset.

    """
    print("\nValores NaN por columna:")
    print(df.isna().sum())

    print("\nInformación general:")
    print(df.info())




# FUNCIONES ANALÍTICAS


def obtener_precios_cuenca_anio(df, cuenca, anio):
    """
    Filtra precios de gas por cuenca y año.
    """
    filtro = (df['cuenca'] == cuenca) & (df['anio'] == anio)
    resultado = df[filtro]

    if resultado.empty:
        print("No se encontraron datos para esa cuenca y año.")
        return None

    return resultado


def analizar_precios_tipo(df, tipo_precio, cuenca='Total Cuenca'):
    """
    Calcula estadísticas de un tipo de precio para una cuenca.

    """
    tipos_validos = ["gnc", "usina", "industria", "exportacion"]

    tipo_precio = tipo_precio.lower()
    if tipo_precio not in tipos_validos:
        raise ValueError(f"Tipo de precio inválido. Opciones válidas: {tipos_validos}")

    columna = f'precio_{tipo_precio}'

    datos = df[df['cuenca'] == cuenca].copy()
    datos = datos[datos[columna] > 0]

    if datos.empty:
        print("No hay datos disponibles para ese tipo de precio en esa cuenca.")
        return None

    precio_promedio = datos[columna].mean()
    precio_maximo = datos[columna].max()
    precio_minimo = datos[columna].min()

    fila_max = datos[datos[columna] == precio_maximo].iloc[0]
    fecha_maximo = (fila_max['anio'], fila_max['mes'])

    return {
        'precio_promedio': round(precio_promedio, 2),
        'precio_maximo': round(precio_maximo, 2),
        'precio_minimo': round(precio_minimo, 2),
        'fecha_maximo': fecha_maximo
    }



# VISUALIZACIONES


def graficar_precio_usina_total(df):
    """
    Grafica evolución temporal del precio usina para Total Cuenca.
    """
    df_total = df[df['cuenca'] == 'Total Cuenca'].copy()

    df_total['fecha'] = pd.to_datetime(
        df_total['anio'].astype(str) + '-' + df_total['mes'].astype(str)
    )

    precio_prom = df_total['precio_usina'].mean()
    precio_max = df_total['precio_usina'].max()
    precio_min = df_total['precio_usina'].min()

    fecha_max = df_total[df_total['precio_usina'] == precio_max]['fecha'].iloc[0]
    fecha_min = df_total[df_total['precio_usina'] == precio_min]['fecha'].iloc[0]

    plt.figure()
    plt.plot(df_total['fecha'], df_total['precio_usina'], label='Precio Usina')

    plt.axhline(precio_prom, linestyle='--', label='Promedio')
    plt.scatter([fecha_max], [precio_max], label='Máximo')
    plt.scatter([fecha_min], [precio_min], label='Mínimo')

    plt.title("Evolución del Precio Usina - Total Cuenca")
    plt.xlabel("Fecha")
    plt.ylabel("Precio Usina (USD/MMBTU)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def graficar_comparacion_precios(df):
    """
    Grafica comparación temporal entre distintos tipos de precios.

    """
    df_total = df[df['cuenca'] == 'Total Cuenca'].copy()

    df_total['fecha'] = pd.to_datetime(
        df_total['anio'].astype(str) + '-' + df_total['mes'].astype(str)
    )

    plt.figure()
    plt.plot(df_total['fecha'], df_total['precio_gnc'], label='GNC')
    plt.plot(df_total['fecha'], df_total['precio_usina'], label='Usina')
    plt.plot(df_total['fecha'], df_total['precio_industria'], label='Industria')
    plt.plot(df_total['fecha'], df_total['precio_exportacion'], label='Exportación')

    plt.title("Comparación de precios de gas")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (USD/MMBTU)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()



# ANÁLISIS EJERCICIO 5


def analisis_cuenca_industria(df):
    """
    Determina la cuenca con precios industriales máximos históricos.

    """
    return df.groupby('cuenca')['precio_industria'].max()



# PROGRAMA PRINCIPAL

def main():

    ruta = 'precios-de-gas-natural-CLEANED.csv'
    gas_df = cargar_dataset(ruta)

    explorar_dataset(gas_df)

    print("\nConsulta ejemplo:")
    print(obtener_precios_cuenca_anio(gas_df, "Neuquina", 2023))

    print("\nAnálisis ejemplo:")
    print(analizar_precios_tipo(gas_df, 'industria', 'Noroeste'))

    graficar_precio_usina_total(gas_df)
    graficar_comparacion_precios(gas_df)

    print("\nPrecios máximos industriales por cuenca:")
    print(analisis_cuenca_industria(gas_df))


# CONCLUSIONES TÉCNICAS


    print("""
    CONCLUSIONES:

    - La cuenca Noroeste presenta los valores históricos más altos en precios industriales.

    - Se observa un incremento significativo en precios para generación termoeléctrica
      especialmente en el período 2024-2025, posiblemente asociado a variaciones en
      demanda energética y condiciones del mercado internacional.

    - Los precios de exportación tienden a ser superiores a los domésticos,
      lo que refleja condiciones diferenciales del mercado internacional.

    - Las variaciones observadas entre 2021 y 2022 podrían estar asociadas a efectos
      macroeconómicos globales, incluyendo disrupciones en cadenas de suministro
      y cambios en la demanda energética post-pandemia.

    - Desde una perspectiva de política energética, podría evaluarse la implementación
      de esquemas diferenciales de precios para exportación, con el objetivo de
      fortalecer la competitividad industrial local.
    """)


if __name__ == "__main__":
    main()
