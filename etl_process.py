#!/usr/bin/env python3
"""
Proceso ETL (Extracción, Transformación y Carga)
Asignatura: Visualización de datos
Proyecto: Web Visualización de datos (Felicidad Mundial 2015-2023)

Este script descarga los datasets anuales del World Happiness Report desde un repositorio público,
estandariza las columnas cuyos nombres cambian de año en año, limpia los nombres de los países,
les asigna su correspondiente código ISO Alpha-3 y región/subregión geográfica, calcula el
residuo de distopía de manera consistente, y guarda el conjunto de datos unificado en un CSV.
"""

import urllib.request
import pandas as pd
import io
import os

def run_etl():
    print("Iniciando el proceso ETL...")
    
    # 1. Cargar el mapeo de países a códigos ISO Alpha-3 y regiones desde el repositorio oficial
    print("Descargando base de datos de códigos ISO-3166 y regiones...")
    iso_url = 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv'
    try:
        req_iso = urllib.request.urlopen(iso_url)
        df_iso = pd.read_csv(io.StringIO(req_iso.read().decode('utf-8')))
        
        # Crear diccionarios de mapeo
        iso_map = df_iso.set_index('name')['alpha-3'].to_dict()
        region_map = df_iso.set_index('alpha-3')['region'].to_dict()
        subregion_map = df_iso.set_index('alpha-3')['sub-region'].to_dict()
    except Exception as e:
        print(f"Error al descargar la base de datos ISO: {e}")
        return False

    # Diccionario de correcciones manuales para nombres de países que difieren de los nombres oficiales ISO
    alternative_names = {
        'Bolivia': 'BOL', 'Bolivia (Plurinational State of)': 'BOL',
        'Russia': 'RUS', 'Russian Federation': 'RUS',
        'Venezuela': 'VEN', 'Venezuela (Bolivarian Republic of)': 'VEN',
        'Iran': 'IRN', 'Iran (Islamic Republic of)': 'IRN',
        'Syria': 'SYR', 'Syrian Arab Republic': 'SYR',
        'Moldova': 'MDA', 'Republic of Moldova': 'MDA',
        'Vietnam': 'VNM', 'Viet Nam': 'VNM',
        'Tanzania': 'TZA', 'United Republic of Tanzania': 'TZA',
        'South Korea': 'KOR', 'Republic of Korea': 'KOR',
        'North Korea': 'PRK', 'Democratic People\'s Republic of Korea': 'PRK',
        'Taiwan': 'TWN', 'Taiwan, Province of China': 'TWN',
        'Taiwan Province of China': 'TWN',
        'Hong Kong': 'HKG', 'Hong Kong SAR, China': 'HKG',
        'Hong Kong S.A.R. of China': 'HKG',
        'Hong Kong S.A.R., China': 'HKG',
        'Macau': 'MAC', 'Macao SAR, China': 'MAC',
        'Laos': 'LAO', 'Lao People\'s Democratic Republic': 'LAO',
        'Congo (Kinshasa)': 'COD', 'Democratic Republic of the Congo': 'COD',
        'Congo (Brazzaville)': 'COG', 'Congo': 'COG',
        'Ivory Coast': 'CIV', 'Côte d\'Ivoire': 'CIV',
        'Brunei': 'BRN', 'Brunei Darussalam': 'BRN',
        'United States': 'USA', 'United States of America': 'USA',
        'United Kingdom': 'GBR',
        'Czech Republic': 'CZE', 'Czechia': 'CZE',
        'Palestine': 'PSE', 'Palestinian Territory': 'PSE', 'State of Palestine': 'PSE',
        'Palestinian Territories': 'PSE',
        'Swaziland': 'SWZ', 'Eswatini': 'SWZ',
        'Eswatini, Kingdom of': 'SWZ',
        'Kosovo': 'XKX',  # Código de usuario asignado comúnmente para Kosovo
        'Somaliland Region': 'SOM', 'Somalia': 'SOM', 'Somaliland region': 'SOM',
        'North Macedonia': 'MKD', 'Macedonia': 'MKD',
        'Northern Cyprus': 'CYP', 'North Cyprus': 'CYP',
        'Trinidad & Tobago': 'TTO', 'Trinidad and Tobago': 'TTO',
        'Turkey': 'TUR', 'Turkiye': 'TUR',
        'Netherlands': 'NLD',
        'Gambia': 'GMB', 'The Gambia': 'GMB'
    }
    
    # Actualizar los diccionarios con las excepciones y asignar regiones manuales
    iso_map.update(alternative_names)
    
    # Regiones personalizadas para códigos especiales no estándar o ausentes en el CSV original
    region_map['XKX'] = 'Europe'
    subregion_map['XKX'] = 'Southern Europe'
    region_map['TWN'] = 'Asia'
    subregion_map['TWN'] = 'Eastern Asia'
    region_map['SOM'] = 'Africa'
    subregion_map['SOM'] = 'Eastern Africa'

    # Base URL del repositorio con los datasets anuales
    base_url = 'https://raw.githubusercontent.com/evanfrang/world_happiness/master/'
    years = range(2015, 2024)

    # Definir los mapeos de columnas por año para unificar el esquema de datos
    # Esquema final deseado:
    # - country: Nombre del país
    # - score: Puntaje general de felicidad (0 a 10)
    # - gdp: Contribución del PIB per cápita
    # - social: Contribución del apoyo social (o familia)
    # - health: Contribución de la esperanza de vida saludable
    # - freedom: Contribución de la libertad para tomar decisiones
    # - generosity: Contribución de la generosidad
    # - trust: Contribución de la percepción de la corrupción
    mappings = {
        2015: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'Economy (GDP per Capita)',
            'social': 'Family',
            'health': 'Health (Life Expectancy)',
            'freedom': 'Freedom',
            'generosity': 'Generosity',
            'trust': 'Trust (Government Corruption)'
        },
        2016: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'Economy (GDP per Capita)',
            'social': 'Family',
            'health': 'Health (Life Expectancy)',
            'freedom': 'Freedom',
            'generosity': 'Generosity',
            'trust': 'Trust (Government Corruption)'
        },
        2017: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'Economy..GDP.per.Capita.',
            'social': 'Family',
            'health': 'Health..Life.Expectancy.',
            'freedom': 'Freedom',
            'generosity': 'Generosity',
            'trust': 'Trust..Government.Corruption.'
        },
        2018: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'GDP per capita',
            'social': 'Social support',
            'health': 'Healthy life expectancy',
            'freedom': 'Freedom to make life choices',
            'generosity': 'Generosity',
            'trust': 'Perceptions of corruption'
        },
        2019: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'GDP per capita',
            'social': 'Social support',
            'health': 'Healthy life expectancy',
            'freedom': 'Freedom to make life choices',
            'generosity': 'Generosity',
            'trust': 'Perceptions of corruption'
        },
        2020: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'Explained by: Log GDP per capita',
            'social': 'Explained by: Social support',
            'health': 'Explained by: Healthy life expectancy',
            'freedom': 'Explained by: Freedom to make life choices',
            'generosity': 'Explained by: Generosity',
            'trust': 'Explained by: Perceptions of corruption'
        },
        2021: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'Explained by: Log GDP per capita',
            'social': 'Explained by: Social support',
            'health': 'Explained by: Healthy life expectancy',
            'freedom': 'Explained by: Freedom to make life choices',
            'generosity': 'Explained by: Generosity',
            'trust': 'Explained by: Perceptions of corruption'
        },
        2022: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'Explained by: GDP per capita',
            'social': 'Explained by: Social support',
            'health': 'Explained by: Healthy life expectancy',
            'freedom': 'Explained by: Freedom to make life choices',
            'generosity': 'Explained by: Generosity',
            'trust': 'Explained by: Perceptions of corruption'
        },
        2023: {
            'country': 'Country',
            'score': 'Score',
            'gdp': 'Explained by: Log GDP per capita',
            'social': 'Explained by: Social support',
            'health': 'Explained by: Healthy life expectancy',
            'freedom': 'Explained by: Freedom to make life choices',
            'generosity': 'Explained by: Generosity',
            'trust': 'Explained by: Perceptions of corruption'
        }
    }

    all_dfs = []
    
    # Descargar, mapear y limpiar los datos de cada año
    for y in years:
        url = f'{base_url}{y}.csv'
        print(f"Descargando datos del año {y}...")
        try:
            req = urllib.request.urlopen(url)
            df_raw = pd.read_csv(io.StringIO(req.read().decode('utf-8')))
            
            mapping = mappings[y]
            # Seleccionar y renombrar las columnas según el estándar
            cols_to_use = {v: k for k, v in mapping.items()}
            df_year = df_raw[list(cols_to_use.keys())].rename(columns=cols_to_use)
            df_year['year'] = y
            
            # Limpiar nombre del país y mapear su código ISO
            df_year['country'] = df_year['country'].apply(lambda c: c.replace('*', '').strip())
            df_year['iso_alpha'] = df_year['country'].map(iso_map)
            
            # Asignar región y subregión
            df_year['region'] = df_year['iso_alpha'].map(region_map)
            df_year['sub_region'] = df_year['iso_alpha'].map(subregion_map)
            
            # Estandarizar valores nulos o vacíos en variables numéricas
            df_year['trust'] = pd.to_numeric(df_year['trust'], errors='coerce').fillna(0.0)
            df_year['generosity'] = pd.to_numeric(df_year['generosity'], errors='coerce').fillna(0.0)
            df_year['freedom'] = pd.to_numeric(df_year['freedom'], errors='coerce').fillna(0.0)
            df_year['health'] = pd.to_numeric(df_year['health'], errors='coerce').fillna(0.0)
            df_year['social'] = pd.to_numeric(df_year['social'], errors='coerce').fillna(0.0)
            df_year['gdp'] = pd.to_numeric(df_year['gdp'], errors='coerce').fillna(0.0)
            df_year['score'] = pd.to_numeric(df_year['score'], errors='coerce').fillna(0.0)
            
            # Calcular la contribución de la Distopía (Residual) de manera consistente:
            # score = gdp + social + health + freedom + generosity + trust + dystopia_residual
            # Por tanto, dystopia_residual = score - (gdp + social + health + freedom + generosity + trust)
            df_year['dystopia_residual'] = df_year['score'] - (
                df_year['gdp'] + df_year['social'] + df_year['health'] + 
                df_year['freedom'] + df_year['generosity'] + df_year['trust']
            )
            
            all_dfs.append(df_year)
            print(f"Año {y} procesado: {len(df_year)} registros.")
        except Exception as e:
            print(f"Error procesando el año {y}: {e}")
            return False

    # Combinar todos los datasets anuales
    df_all = pd.concat(all_dfs, ignore_index=True)
    
    # Comprobar calidad de datos
    null_iso = df_all['iso_alpha'].isna().sum()
    null_reg = df_all['region'].isna().sum()
    
    print(f"\nCalidad de datos unificados:")
    print(f"- Total registros: {len(df_all)}")
    print(f"- Registros con código ISO nulo: {null_iso}")
    print(f"- Registros con región geográfica nula: {null_reg}")
    
    if null_iso > 0 or null_reg > 0:
        print("Advertencia: Hay códigos ISO o regiones nulas en el dataset unificado.")
        
    output_file = 'cleaned_world_happiness.csv'
    df_all.to_csv(output_file, index=False)
    print(f"Dataset unificado guardado en: {output_file}")
    print("ETL finalizado con éxito.\n")
    return True

if __name__ == '__main__':
    run_etl()
