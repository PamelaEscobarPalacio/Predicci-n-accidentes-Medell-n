import os
import pandas as pd
import folium
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geopandas as gpd
from IPython.display import IFrame
from datetime import datetime, date, timedelta
import holidays_co

def lista_valores_unicos(columna):
    datos = pd.read_csv("data/data_limpia.csv",  sep=",", decimal=".")
    valores_distintos = datos[f'{columna}'].unique()
    return valores_distintos

def style_function(feature):
    return {
        'color': 'black',  # Color de las líneas
        'weight': 0.5  # Grosor de las líneas (ajusta este valor)
    }

def crear_mapa_todo():
  barrios_med = gpd.read_file('data/Barrios de Medellín/Barrio_Vereda.dbf')
  mapa = folium.Map(width=910, height=410, zoom_start=12, location=[6.27,-75.60])
  folium.TileLayer('openstreetmap').add_to(mapa)
  folium.GeoJson(data = barrios_med,style_function=style_function,
               name = 'NOMBRE',
               popup = folium.GeoJsonPopup(
                  fields = ['CODIGO', 'NOMBRE'],
                  aliases = ['Cod.', 'Barrio']
               )
               ).add_to(mapa)
  #folium.GeoJson(data = barrios_med,style_function=style_function).add_to(mapa)
  mapa.save('templates/mapa_sincolores.html')
  return mapa

def lista_cluster(cluster):
   datos = pd.read_csv("data/final_clusters.csv",  sep=",", decimal=".")
   datos_cluster = datos[datos['cluster'] == cluster] 
   lista_cluster = datos_cluster['barrio'].tolist()
   return lista_cluster


def prediccion_modelo(fecha_inicial, fecha_final):
    df = pd.read_csv("data/validacion.csv", sep=",", decimal=".")
    df['fecha'] = pd.to_datetime(df['fecha'])
    inicio = datetime.strptime(fecha_inicial, '%d/%m/%Y')
    fin = datetime.strptime(fecha_final, '%d/%m/%Y')
    mask = (df['fecha'] >= inicio) & (df['fecha'] <= fin)
    df_filtrado = df.loc[mask]
    accidentes = df_filtrado['prediccion'].sum()
    accidentes_entero = int(accidentes)
    rutas_graficos = {}
    for frecuencia in ['D', 'W', 'M']:
        df_agrupado = df_filtrado.groupby(pd.Grouper(key='fecha', freq=frecuencia))['prediccion'].sum().reset_index()
        
        # Generar el gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(df_agrupado['fecha'], df_agrupado['prediccion'], marker='o', linestyle='-', color='blue')
        plt.title(f'Predicción de Accidentes - Frecuencia {frecuencia}')
        plt.xlabel('Fecha')
        plt.ylabel('Número de Accidentes')
        plt.grid(True)
        plt.tight_layout()
        
        # Guardar la figura
        ruta_grafico = f'static/predicciones_{frecuencia}.png'
        plt.savefig(ruta_grafico)
        plt.close()
        
        rutas_graficos[frecuencia] = os.path.basename(ruta_grafico)

    return accidentes_entero, rutas_graficos


    

def crear_lista(fecha1,fecha2,barrio,tipo):
    datos = pd.read_csv('data/data_limpia-1.csv', sep=',', encoding='utf-8')
    datos_def = datos[['BARRIO', 'CLASE_ACCIDENTE', 'LATITUD', 'LONGITUD', 'FECHA_ACCIDENTE']]
    # Convierte las fechas en el DataFrame a objetos datetime
    datos_def['FECHA_ACCIDENTE'] = pd.to_datetime(datos_def['FECHA_ACCIDENTE'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    # Filtrar por fecha
    fecha1 = datetime.strptime(fecha1, '%d/%m/%Y %H:%M:%S')
    fecha2 = datetime.strptime(fecha2, '%d/%m/%Y %H:%M:%S')
    datos_def = datos_def.loc[(datos_def['FECHA_ACCIDENTE'] >= fecha1) & (datos_def['FECHA_ACCIDENTE'] <= fecha2)]
    # Filtrar por tipo de accidente
    if tipo != 'Todos':
        datos_def = datos_def.loc[datos_def['CLASE_ACCIDENTE'] == tipo]
    # Filtrar por barrio
    if barrio != 'Todos':
        datos_def = datos_def.loc[datos_def['BARRIO'] == barrio]
    lista = datos_def.to_dict(orient='records')
    cantidad_accidentes = len(lista)
    return lista ,cantidad_accidentes

def obtener_color(tipo_accidente):
    colores = {
        'Atropello': 'blue',
        'Caida Ocupante': 'green',
        'Choque': 'red',
        'Volcamiento': 'orange',
        'Incendio': 'purple'
    }
    return colores.get(tipo_accidente, 'gray')

def crear_mapa_historico(lista,barrio):
  barrios_med = gpd.read_file('data/Barrios de Medellín/Barrio_Vereda.dbf')
  # Obtiene las coordenadas del barrio seleccionado
  barrio_coords = barrios_med[barrios_med['NOMBRE'] == barrio].geometry.centroid
  # Crea el mapa centrado en las coordenadas del barrio seleccionado
  mapa = folium.Map(width=910, height=410, zoom_start=16, location=[barrio_coords.y.values[0], barrio_coords.x.values[0]])
  folium.TileLayer('openstreetmap').add_to(mapa)
  folium.GeoJson(data = barrios_med[barrios_med['NOMBRE']== barrio],style_function=style_function).add_to(mapa)
  for lista in lista:
    color = obtener_color(lista["CLASE_ACCIDENTE"])
    folium.Marker(
        location=[lista["LATITUD"], lista["LONGITUD"]],
        popup=f"Barrio: {lista['BARRIO']},\n Tipo accidente: {lista['CLASE_ACCIDENTE']},\n fecha y hora:{lista['FECHA_ACCIDENTE']} ",
        icon=folium.Icon(color=color)
    ).add_to(mapa)
  mapa.save('templates/mapa_historico.html')
  return mapa
