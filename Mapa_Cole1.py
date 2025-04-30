#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Para crear el enviroment ----------------------------
#--------------Creamos el enviroment
# conda create -n MapaCole python=3.11
#-------------Lo activamos
# conda activate MapaCole 
#------------Vamos a la ruta del txt
# cd Documents/GitHub/High-School-Access-Peru
#------------Instalamos
# pip install -r requirements.txt  


# In[13]:


#pip install geopy


# In[15]:


#pip install xlrd


# In[5]:


#pip install lxml


# In[1]:


#import os
#os.getcwd()


# In[65]:


##########Leer el archivo Excel-----------------
import streamlit as st
import pandas as pd

# Leer el archivo como tabla HTML
tables = pd.read_html("src/listado_iiee.xls")

# Ver cuántas tablas encontró
print(f"Se encontraron {len(tables)} tablas.")


# In[66]:


tables[0].head()


# In[22]:


import geopandas as gpd

# Ruta al archivo de distritos (nivel 3)
ruta_json = "src/gadm41_PER_3.json"

# Cargar el shapefile en formato GeoJSON
distritos = gpd.read_file(ruta_json)

# Verificar las primeras filas para inspeccionar el archivo
print(distritos.head())

# Verificar el sistema de coordenadas (crs)
print(distritos.crs)


# import geopandas as gpd
# import matplotlib.pyplot as plt
# from shapely.geometry import Point
# from matplotlib.patches import Patch
# from matplotlib.legend_handler import HandlerPatch
# 
# # Cargar el archivo de distritos (nivel 3)
# #ruta_json = "ruta/a/tu/carpeta/gadm41_PER_3.json"
# #distritos = gpd.read_file(ruta_json)
# 
# # Asegurarse de que la geometría está en el CRS correcto
# distritos = distritos.to_crs(epsg=4326)
# 
# # Datos de las escuelas (usar las coordenadas de la tabla proporcionada)
# escuelas_data = [
#     {"nivel": "Inicial", "lat": -6.231760, "lon": -77.872430},
#     {"nivel": "Inicial", "lat": -6.231590, "lon": -77.870020},
#     {"nivel": "Inicial", "lat": -6.227000, "lon": -77.875520},
#     {"nivel": "Primaria", "lat": -6.229603, "lon": -77.864544},
#     {"nivel": "Primaria", "lat": -6.225840, "lon": -77.868020},
#     {"nivel": "Secundaria", "lat": -6.230000, "lon": -77.870000},
#     {"nivel": "Secundaria", "lat": -6.229000, "lon": -77.869000},
# ]
# 
# # Crear GeoDataFrame de las escuelas
# escuelas_gdf = gpd.GeoDataFrame(
#     escuelas_data,
#     geometry=[Point(lon, lat) for lat, lon in [(escuela['lat'], escuela['lon']) for escuela in escuelas_data]],
#     crs="EPSG:4326"
# )
# 
# # 1. Crear mapas de distribución de escuelas por nivel
# def plot_escuelas_por_nivel(escuelas_gdf, nivel, distritos_gdf):
#     # Filtrar las escuelas por nivel
#     escuelas_filtradas = escuelas_gdf[escuelas_gdf['nivel'] == nivel]
#     
#     # Contar las escuelas por distrito
#     distritos_gdf['escuelas_count'] = distritos_gdf.geometry.apply(lambda x: escuelas_filtradas[escuelas_filtradas.geometry.within(x)].shape[0])
# 
#     # Graficar
#     fig, ax = plt.subplots(1, 1, figsize=(10, 10))
#     distritos_gdf.boundary.plot(ax=ax, linewidth=1, color='k')
#     distritos_gdf.plot(column='escuelas_count', ax=ax, legend=True,
#                        legend_kwds={'label': "Número de Escuelas",
#                                     'orientation': "horizontal"})
#     ax.set_title(f"Distribución de escuelas - {nivel}")
#     st.pyplot(plt.gcf())
# 
# 
# # Crear mapas para cada nivel educativo
# plot_escuelas_por_nivel(escuelas_gdf, "Inicial", distritos)
# plot_escuelas_por_nivel(escuelas_gdf, "Primaria", distritos)
# plot_escuelas_por_nivel(escuelas_gdf, "Secundaria", distritos)
# 
# # 2. Proximidad de las escuelas primarias a las secundarias
# def proximidad_escuelas(escuelas_gdf, nivel_primaria, nivel_secundaria, radio_km=5):
#     # Filtrar las escuelas por nivel
#     primarias = escuelas_gdf[escuelas_gdf['nivel'] == nivel_primaria]
#     secundarias = escuelas_gdf[escuelas_gdf['nivel'] == nivel_secundaria]
#     
#     # Reproyectar a un CRS proyectado para trabajar con distancias en metros
#     primarias = primarias.to_crs(epsg=3395)  # Cambiar a un CRS proyectado adecuado (UTM)
#     secundarias = secundarias.to_crs(epsg=3395)
# 
#     # Crear círculos de 5 km alrededor de las primarias
#     primarias['geometry'] = primarias.geometry.buffer(radio_km * 1000)  # Convertir a metros
#     
#     # Volver al CRS original
#     primarias = primarias.to_crs(epsg=4326)
# 
#     # Contar cuántas secundarias caen dentro de cada círculo
#     proximidad = primarias.copy()
#     proximidad['escuelas_cercanas'] = proximidad.apply(
#         lambda row: sum(secundarias.geometry.within(row.geometry)), axis=1
#     )
#     
#     # Identificar la primaria con la mayor y menor cantidad de escuelas cercanas
#     primaria_mas_cercanas = proximidad.loc[proximidad['escuelas_cercanas'].idxmax()]
#     primaria_menos_cercanas = proximidad.loc[proximidad['escuelas_cercanas'].idxmin()]
# 
#     # Graficar
#     fig, ax = plt.subplots(1, 1, figsize=(10, 10))
#     distritos.boundary.plot(ax=ax, linewidth=1, color='k')
#     secundarias.plot(ax=ax, color='red', markersize=50, label='Escuelas Secundarias')
#     primarias.plot(ax=ax, color='blue', markersize=50, label='Escuelas Primarias')
# 
#     # Añadir círculos de 5 km alrededor de las primarias (usando centroides)
#     for idx, row in proximidad.iterrows():
#         centroid = row.geometry.centroid
#         ax.add_patch(plt.Circle((centroid.x, centroid.y), radio_km / 111.32, color='blue', alpha=0.2))
#     
#     # Leyenda personalizada
#     circle_patch = Patch(color='blue', alpha=0.2, label='Círculos de 5 km')
#     ax.legend(handles=[circle_patch], loc='upper left')
# 
#     ax.set_title(f"Proximidad de Escuelas Primarias a Secundarias")
#     st.pyplot(plt.gcf())
# 
# 
#     return primaria_mas_cercanas, primaria_menos_cercanas
# 
# # Análisis de proximidad
# primaria_mas, primaria_menos = proximidad_escuelas(escuelas_gdf, "Primaria", "Secundaria")
# print("Primaria con más escuelas cercanas:", primaria_mas)
# print("Primaria con menos escuelas cercanas:", primaria_menos)

# In[27]:


#Task 1: Static Maps by School Level - for all districts in the country
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# 1. Cargar distritos y escuelas
ruta_json = "src/gadm41_PER_3.json"
distritos_gdf = gpd.read_file(ruta_json)

escuelas_df = tables[0].copy()
escuelas_df['geometry'] = escuelas_df.apply(
    lambda row: Point(row['Longitud'], row['Latitud']), axis=1
)
escuelas_gdf = gpd.GeoDataFrame(escuelas_df, geometry='geometry', crs=distritos_gdf.crs)

# 2. Asegurarnos de tener un ID en distritos
distritos_gdf = distritos_gdf.reset_index().rename(columns={"index": "Distrito_ID"})

# 3. Definir niveles y crear mapas
niveles = ['Inicial', 'Primaria', 'Secundaria']

for nivel in niveles:
    # Filtrar escuelas por nivel
    mask = escuelas_gdf['Nivel / Modalidad'].str.contains(nivel, case=False, na=False)
    escuelas_nivel = escuelas_gdf[mask]

    # Spatial join: asignar cada escuela a su distrito
    joined = gpd.sjoin(distritos_gdf, escuelas_nivel, how="left", predicate='intersects')

    # Contar escuelas por Distrito_ID
    conteos = (
        joined
        .groupby('Distrito_ID')
        .size()
        .reset_index(name=f'Escuelas_{nivel}')
    )

    # Unir conteos al GeoDataFrame de distritos
    distritos_gdf = (
        distritos_gdf
        .merge(conteos, on='Distrito_ID', how='left')
        .fillna({f'Escuelas_{nivel}': 0})
    )

    # Graficar
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    distritos_gdf.plot(
        column=f'Escuelas_{nivel}',
        cmap='OrRd',
        linewidth=0.5,
        edgecolor='gray',
        legend=True,
        legend_kwds={'label': f"Número de escuelas ({nivel})", 'shrink': 0.6},
        ax=ax
    )
    ax.set_title(f"Distribución de Escuelas de Nivel {nivel} por Distrito")
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(plt.gcf())


# In[41]:


import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# --- 1. Filtrar distritos de Ayacucho y Huancavelica ---
regiones = ['Ayacucho', 'Huancavelica']
distritos_sel = distritos_gdf[distritos_gdf['NAME_1'].isin(regiones)]

# --- 2. Filtrar escuelas en esas regiones ---
escuelas_region = gpd.sjoin(
    escuelas_gdf, distritos_sel, how="inner", predicate="intersects"
).drop(columns=['index_right'])

# --- 3. Separar primarias y secundarias ---
primarias = escuelas_region[
    escuelas_region['Nivel / Modalidad'].str.contains("Primaria", case=False, na=False)
].copy()
secundarias = escuelas_region[
    escuelas_region['Nivel / Modalidad'].str.contains("Secundaria", case=False, na=False)
].copy()

# --- 4. Reproyectar a CRS en metros para cálculos ---
primarias = primarias.to_crs(epsg=32718)
secundarias = secundarias.to_crs(epsg=32718)

# --- 5. Calcular centroides y buffers de 5 km ---
# Guardamos el centroide en una nueva columna
primarias['centroide'] = primarias.geometry.centroid
# Luego creamos el buffer de 5 km (5 000 m)
primarias['buffer'] = primarias['centroide'].buffer(5000)

# --- 6. Contar secundarias dentro de cada buffer ---
primarias['Secundarias_cerca'] = primarias['buffer'].apply(
    lambda buf: secundarias.within(buf).sum()
)

# --- 7. Identificar casos extremos ---
primaria_max = primarias.loc[primarias['Secundarias_cerca'].idxmax()]
primaria_min = primarias.loc[primarias['Secundarias_cerca'].idxmin()]

# --- 8. Graficar cada caso (corregido) ---
for caso_label, primaria in [("MAYOR", primaria_max), ("MENOR", primaria_min)]:
    fig, ax = plt.subplots(figsize=(8, 8))

    # Verifica que la geometría del buffer no esté vacía o inválida
    if primaria['buffer'] is None or primaria['buffer'].is_empty:
        print(f"⚠️ Buffer vacío para primaria con {caso_label} secundarias.")
        continue

    # Reproyectar geometrías para graficar en lat/lon (EPSG:4326)
    try:
        buf_geo = gpd.GeoSeries([primaria['buffer']], crs="EPSG:32718").to_crs(epsg=4326)
        cent_geo = gpd.GeoSeries([primaria['centroide']], crs="EPSG:32718").to_crs(epsg=4326)
        sec_geo = secundarias.to_crs(epsg=4326)
    except Exception as e:
        print(f"❌ Error reproyectando: {e}")
        continue

    # Filtrar secundarias dentro del buffer (verificando geometrías válidas)
    try:
        sec_cercanas = sec_geo[sec_geo.geometry.within(buf_geo.iloc[0])]
    except Exception as e:
        print(f"❌ Error calculando secundarias dentro del buffer: {e}")
        continue

    # Plot
    buf_geo.plot(ax=ax, color='lightblue', edgecolor='blue', alpha=0.4, label='Área 5 km')
    cent_geo.plot(ax=ax, color='red', markersize=80, label='Primaria (centroide)')

    if not sec_cercanas.empty:
        sec_cercanas.plot(ax=ax, color='green', markersize=20, label='Secundarias cercanas')

    ax.set_title(f"Primaria con {caso_label} secundarias cercanas ({primaria['Secundarias_cerca']})")
    ax.legend()
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(plt.gcf())


# #Task 1: Choropleth Map Creation
# import folium
# import geopandas as gpd
# from shapely.geometry import Point
# import pandas as pd
# 
# # --- 1. Filtrar distritos de Ayacucho y Huancavelica ---
# regiones = ['Ayacucho', 'Huancavelica']
# distritos_sel = distritos_gdf[distritos_gdf['NAME_1'].isin(regiones)]
# 
# # --- 2. Filtrar escuelas en esas regiones ---
# escuelas_region = gpd.sjoin(
#     escuelas_gdf, distritos_sel, how="inner", predicate="intersects"
# ).drop(columns=['index_right'])
# 
# # --- 3. Separar primarias y secundarias ---
# primarias = escuelas_region[
#     escuelas_region['Nivel / Modalidad'].str.contains("Primaria", case=False, na=False)
# ].copy()
# secundarias = escuelas_region[
#     escuelas_region['Nivel / Modalidad'].str.contains("Secundaria", case=False, na=False)
# ].copy()
# 
# # --- Task 1: Choropleth Map Creation ---
# # Agrupar por distrito y contar escuelas por nivel
# escuelas_inicial = escuelas_region[escuelas_region['Nivel / Modalidad'].str.contains("Inicial", case=False, na=False)].groupby('Distrito_ID').size()
# escuelas_primaria = primarias.groupby('Distrito_ID').size()
# escuelas_secundaria = secundarias.groupby('Distrito_ID').size()
# 
# # Crear un mapa base centrado en Perú
# m = folium.Map(location=[-9.19, -75.0152], zoom_start=6)
# 
# # Agregar capa choropleth para Inicial
# folium.Choropleth(
#     geo_data=distritos_sel,
#     name='Inicial',
#     data=escuelas_inicial,
#     columns=['Distrito_ID', 0],
#     key_on='feature.properties.Distrito_ID',
#     fill_color='YlGn',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Escuelas Iniciales',
# ).add_to(m)
# 
# # Agregar capa choropleth para Primaria
# folium.Choropleth(
#     geo_data=distritos_sel,
#     name='Primaria',
#     data=escuelas_primaria,
#     columns=['Distrito_ID', 0],
#     key_on='feature.properties.Distrito_ID',
#     fill_color='YlOrRd',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Escuelas Primarias',
# ).add_to(m)
# 
# # Agregar capa choropleth para Secundaria
# folium.Choropleth(
#     geo_data=distritos_sel,
#     name='Secundaria',
#     data=escuelas_secundaria,
#     columns=['Distrito_ID', 0],
#     key_on='feature.properties.Distrito_ID',
#     fill_color='BuGn',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Escuelas Secundarias',
# ).add_to(m)
# 
# # Agregar control de capas
# folium.LayerControl().add_to(m)
# 
# # Guardar el mapa como archivo HTML
# m.save('choropleth_map.html')
# 

# In[ ]:


import folium
import geopandas as gpd
import streamlit as st
from shapely.geometry import Point
import pandas as pd

# --- 1. Filtrar distritos de Ayacucho y Huancavelica ---
regiones = ['Ayacucho', 'Huancavelica']
distritos_sel = distritos_gdf[distritos_gdf['NAME_1'].isin(regiones)]

# --- 2. Filtrar escuelas en esas regiones ---
escuelas_region = gpd.sjoin(
    escuelas_gdf, distritos_sel, how="inner", predicate="intersects"
).drop(columns=['index_right'])

# --- 3. Separar primarias y secundarias ---
primarias = escuelas_region[
    escuelas_region['Nivel / Modalidad'].str.contains("Primaria", case=False, na=False)
].copy()
secundarias = escuelas_region[
    escuelas_region['Nivel / Modalidad'].str.contains("Secundaria", case=False, na=False)
].copy()

# --- Task 1: Choropleth Map Creation ---
# Agrupar por distrito y contar escuelas por nivel
escuelas_inicial = escuelas_region[escuelas_region['Nivel / Modalidad'].str.contains("Inicial", case=False, na=False)].groupby('Distrito_ID').size()
escuelas_primaria = primarias.groupby('Distrito_ID').size()
escuelas_secundaria = secundarias.groupby('Distrito_ID').size()

# Crear un mapa base centrado en Perú
m = folium.Map(location=[-9.19, -75.0152], zoom_start=6)

# Agregar capa choropleth para Inicial
folium.Choropleth(
    geo_data=distritos_sel,
    name='Inicial',
    data=escuelas_inicial,
    columns=['Distrito_ID', 0],
    key_on='feature.properties.Distrito_ID',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Escuelas Iniciales',
).add_to(m)

# Agregar capa choropleth para Primaria
folium.Choropleth(
    geo_data=distritos_sel,
    name='Primaria',
    data=escuelas_primaria,
    columns=['Distrito_ID', 0],
    key_on='feature.properties.Distrito_ID',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Escuelas Primarias',
).add_to(m)

# Agregar capa choropleth para Secundaria
folium.Choropleth(
    geo_data=distritos_sel,
    name='Secundaria',
    data=escuelas_secundaria,
    columns=['Distrito_ID', 0],
    key_on='feature.properties.Distrito_ID',
    fill_color='BuGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Escuelas Secundarias',
).add_to(m)

# Agregar control de capas
folium.LayerControl().add_to(m)

# Mostrar el mapa en Streamlit
st.title("Mapa de Escuelas en Ayacucho y Huancavelica")
st.markdown("Este mapa muestra las escuelas primarias, secundarias e iniciales en los distritos de Ayacucho y Huancavelica.")

# Renderizar el mapa en Streamlit usando folium
st.components.v1.html(m._repr_html_(), height=600)


# ####################ESTOY QUITANDO EL SEGUNDO MAPA INTERACTIVO PORQUE GENERABA PROBLEMAS POR SER ALGO PESADO Y TARDABA EN CARGAR
# 
# 
# 
# #################################################################################################
# #Task 2: High School Proximity Visualization (Huancavelica y Ayacucho)
# from shapely.geometry import Point
# import folium
# 
# # --- 1. Filtrar las escuelas primarias y secundarias en Huancavelica y Ayacucho ---
# escuelas_primarias_region = escuelas_region[
#     escuelas_region['Nivel / Modalidad'].str.contains("Primaria", case=False, na=False)
# ].copy()
# escuelas_secundarias_region = escuelas_region[
#     escuelas_region['Nivel / Modalidad'].str.contains("Secundaria", case=False, na=False)
# ].copy()
# 
# # --- 2. Crear un mapa base para la visualización ---
# m_proximidad = folium.Map(location=[-9.19, -75.0152], zoom_start=6)
# 
# # --- 3. Para cada escuela primaria en Huancavelica y Ayacucho: ---
# for index, primaria in escuelas_primarias_region.iterrows():
#     # Obtener las coordenadas de la escuela primaria
#     lat_primaria, lon_primaria = primaria['Latitud'], primaria['Longitud']
#     
#     # Crear un marcador para la escuela primaria
#     folium.Marker([lat_primaria, lon_primaria], popup=primaria['Nombre de SS.EE.'], icon=folium.Icon(color='blue')).add_to(m_proximidad)
#     
#     # Crear un círculo con radio de 5 km alrededor de la escuela primaria
#     folium.Circle(
#         location=[lat_primaria, lon_primaria],
#         radius=5000,
#         color='blue',
#         fill=True,
#         fill_color='blue',
#         fill_opacity=0.2
#     ).add_to(m_proximidad)
#     
#     # Filtrar las escuelas secundarias dentro del radio de 5 km
#     for index_secundaria, secundaria in escuelas_secundarias_region.iterrows():
#         lat_secundaria, lon_secundaria = secundaria['Latitud'], secundaria['Longitud']
#         
#         # Calcular la distancia entre la primaria y la secundaria
#         distancia = Point(lon_primaria, lat_primaria).distance(Point(lon_secundaria, lat_secundaria)) * 100000  # en metros
#         
#         # Si la secundaria está dentro de los 5 km
#         if distancia <= 5000:
#             folium.Marker(
#                 [lat_secundaria, lon_secundaria], 
#                 popup=secundaria['Nombre de SS.EE.'], 
#                 icon=folium.Icon(color='red')
#             ).add_to(m_proximidad)
# 
# # Guardar el mapa con las escuelas y proximidades
# m_proximidad.save('high_school_proximity_map.html')
# 

# import folium
# import geopandas as gpd
# import streamlit as st
# from shapely.geometry import Point
# import pandas as pd
# 
# # --- 1. Filtrar las escuelas primarias y secundarias en Huancavelica y Ayacucho ---
# escuelas_primarias_region = escuelas_region[
#     escuelas_region['Nivel / Modalidad'].str.contains("Primaria", case=False, na=False)
# ].copy()
# escuelas_secundarias_region = escuelas_region[
#     escuelas_region['Nivel / Modalidad'].str.contains("Secundaria", case=False, na=False)
# ].copy()
# 
# # --- 2. Crear un mapa base para la visualización ---
# m_proximidad = folium.Map(location=[-9.19, -75.0152], zoom_start=6)
# 
# # --- 3. Para cada escuela primaria en Huancavelica y Ayacucho: ---
# for index, primaria in escuelas_primarias_region.iterrows():
#     # Obtener las coordenadas de la escuela primaria
#     lat_primaria, lon_primaria = primaria['Latitud'], primaria['Longitud']
#     
#     # Crear un marcador para la escuela primaria
#     folium.Marker([lat_primaria, lon_primaria], popup=primaria['Nombre de SS.EE.'], icon=folium.Icon(color='blue')).add_to(m_proximidad)
#     
#     # Crear un círculo con radio de 5 km alrededor de la escuela primaria
#     folium.Circle(
#         location=[lat_primaria, lon_primaria],
#         radius=5000,
#         color='blue',
#         fill=True,
#         fill_color='blue',
#         fill_opacity=0.2
#     ).add_to(m_proximidad)
#     
#     # Filtrar las escuelas secundarias dentro del radio de 5 km
#     for index_secundaria, secundaria in escuelas_secundarias_region.iterrows():
#         lat_secundaria, lon_secundaria = secundaria['Latitud'], secundaria['Longitud']
#         
#         # Calcular la distancia entre la primaria y la secundaria
#         distancia = Point(lon_primaria, lat_primaria).distance(Point(lon_secundaria, lat_secundaria)) * 100000  # en metros
#         
#         # Si la secundaria está dentro de los 5 km
#         if distancia <= 5000:
#             folium.Marker(
#                 [lat_secundaria, lon_secundaria], 
#                 popup=secundaria['Nombre de SS.EE.'], 
#                 icon=folium.Icon(color='red')
#             ).add_to(m_proximidad)
# 
# # Mostrar el mapa en Streamlit
# st.title("Mapa de Proximidad de Escuelas Secundarias a Escuelas Primarias")
# st.markdown("Este mapa muestra las escuelas primarias en Huancavelica y Ayacucho, junto con las escuelas secundarias dentro de un radio de 5 km.")
# 
# # Renderizar el mapa en Streamlit usando folium
# st.components.v1.html(m_proximidad._repr_html_(), height=600)

# Terreno: La región de Huancavelica y Ayacucho tiene terrenos montañosos, lo que podría dificultar el acceso a escuelas secundarias cercanas, especialmente en áreas rurales.
# 
# Accesibilidad: La conectividad vial en estas regiones puede ser limitada, lo que afecta la proximidad real a otras escuelas, a pesar de las distancias geográficas.
# 
# Urbanización vs. Ruralidad: Las escuelas primarias en áreas rurales podrían estar más aisladas, lo que obliga a los estudiantes a recorrer largas distancias para llegar a una secundaria, a pesar de que el mapa muestra proximidad geográfica.

# In[57]:


import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
from io import BytesIO
from streamlit_folium import folium_static  # Asegúrate de importar folium_static

# --- Cargar los datos ---
# Asegúrate de tener los datos previamente cargados en tus variables: distritos_gdf, escuelas_gdf

# Crear el mapa base para la visualización dinámica
def create_folium_map():
    m = folium.Map(location=[-9.19, -75.0152], zoom_start=6)

    # Agregar las capas de choropleth (como en el código anterior)
    folium.Choropleth(
        geo_data=distritos_gdf,
        name='Inicial',
        data=escuelas_inicial,
        columns=['district_id', 0],
        key_on='feature.properties.district_id',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Escuelas Iniciales',
    ).add_to(m)

    folium.Choropleth(
        geo_data=distritos_gdf,
        name='Primaria',
        data=escuelas_primaria,
        columns=['district_id', 0],
        key_on='feature.properties.district_id',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Escuelas Primarias',
    ).add_to(m)

    folium.Choropleth(
        geo_data=distritos_gdf,
        name='Secundaria',
        data=escuelas_secundaria,
        columns=['district_id', 0],
        key_on='feature.properties.district_id',
        fill_color='BuGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Escuelas Secundarias',
    ).add_to(m)

    return m

# Función para crear mapas de proximidad de escuelas (según el Task 2)
def create_proximity_map():
    # Aquí pones el código de la visualización de proximidad
    m_proximity = folium.Map(location=[-13.4, -74.2], zoom_start=7)
    # Añadir la lógica para crear el mapa de proximidad usando folium y las escuelas más cercanas
    # Agregar los círculos y las marcas para las escuelas más cercanas
    return m_proximity

# --- Streamlit App ---
st.title("Análisis de Distribución de Escuelas en Ayacucho y Huancavelica")

# Tabs
tabs = st.selectbox("Selecciona una pestaña", ["Data Description", "Static Maps", "Dynamic Maps"])

if tabs == "Data Description":
    st.header("Descripción de los Datos")
    st.write("""
        En este análisis se estudian las escuelas de los distritos de Ayacucho y Huancavelica, con enfoque en los niveles educativos de 
        Inicial, Primaria y Secundaria. Se han utilizado datos geoespaciales de distritos y escuelas, y se aplicó análisis espacial 
        para determinar la distribución de las escuelas en estos distritos.

        ### Fuentes de los Datos:
        - Los datos de los distritos provienen del [Instituto Nacional de Estadística e Informática (INEI)].
        - Los datos de las escuelas provienen del Ministerio de Educación de Perú (MINEDU).

        ### Preprocesamiento:
        - Se realizaron uniones espaciales para filtrar las escuelas dentro de los distritos de Ayacucho y Huancavelica.
        - Los datos de escuelas fueron segmentados según los niveles educativos: Inicial, Primaria y Secundaria.
    """)
    st.write("""
        ### Asunciones:
        - Los distritos y las escuelas están representados en un sistema de coordenadas geográficas WGS84 (latitud y longitud).
        - El análisis de proximidad considera un radio de 5 km para la cercanía entre escuelas primarias y secundarias.
    """)

elif tabs == "Static Maps":
    st.header("Mapas Estáticos")
    st.write("Los siguientes mapas muestran la distribución de las escuelas de acuerdo con su nivel educativo en los distritos de Ayacucho y Huancavelica.")

    # Aquí, insertamos las imágenes estáticas generadas por GeoPandas (como mapas con matplotlib)
    # Asumiendo que ya tienes los mapas generados previamente como imágenes (por ejemplo, en formato PNG)
    st.image("static_map_inicial.png", caption="Distribución de Escuelas Iniciales", use_column_width=True)
    st.image("static_map_primaria.png", caption="Distribución de Escuelas Primarias", use_column_width=True)
    st.image("static_map_secundaria.png", caption="Distribución de Escuelas Secundarias", use_column_width=True)

elif tabs == "Dynamic Maps":
    st.header("Mapas Interactivos")
    st.write("A continuación, puedes interactuar con los mapas dinámicos de distribución de las escuelas y las proximidades entre ellas.")

    # Crear el mapa de Folium con choropleth y proximidad
    m = create_folium_map()
    m_proximity = create_proximity_map()

    # Mostrar los mapas interactivos en Streamlit
    # Usamos `folium` con Streamlit para renderizar los mapas
    folium_static(m)
    folium_static(m_proximity)


# In[ ]:


#conda activate MapaCole
#cd "C:\Users\Fabrizio\Documents\GitHub\High-School-Access-Peru"
#jupyter nbconvert --to script Mapa_Cole1.ipynb
#streamlit run Mapa_Cole1.py

