import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Inyección de CSS personalizado para estética premium (Glassmorphism y Tipografía)
def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        /* Modificar fuente de toda la aplicación */
        html, body, [class*="css"], [class*="st-"] {
            font-family: 'Outfit', sans-serif !important;
        }
        
        /* Asegurar que los iconos de Streamlit no se vean afectados por el cambio de fuente */
        .stIconMaterial, [data-testid="stIconMaterial"], [class*="st-Icon"], [class*="stIcon"] {
            font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        }
        
        /* Título principal con degradado cromático */
        .title-gradient {
            background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.8rem;
            margin-bottom: 0.2rem;
            text-align: center;
        }
        
        .subtitle-custom {
            color: #9ca3af;
            font-size: 1.1rem;
            font-weight: 400;
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Tarjeta con efecto Glassmorphism */
        .glass-card {
            background: rgba(31, 41, 55, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }
        .glass-card:hover {
            transform: translateY(-2px);
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 10px 40px rgba(99, 102, 241, 0.15);
        }

        /* Métricas personalizadas */
        .metric-val {
            font-size: 2.2rem;
            font-weight: 700;
            color: #818cf8;
            margin: 5px 0;
            text-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
        }
        .metric-lbl {
            font-size: 0.85rem;
            font-weight: 600;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-sub {
            font-size: 0.9rem;
            color: #cbd5e1;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. Cargar datos desde el CSV local con caché para optimizar el rendimiento
@st.cache_data
def load_data():
    file_path = 'cleaned_world_happiness.csv'
    if not os.path.exists(file_path):
        st.error("No se encontró el archivo de datos. Por favor, ejecuta 'etl_process.py' primero.")
        return pd.DataFrame()
    return pd.read_csv(file_path)

# Configurar vista de la página
inject_custom_css()

# Cargar dataset
df = load_data()

if not df.empty:
    st.markdown("<h1 class='title-gradient'>🌍 Análisis Global de la Felicidad</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle-custom'>Explora la distribución de la felicidad mundial y la correlación de sus factores socioeconómicos (2015-2023)</p>", unsafe_allow_html=True)

    # --- WIDGETS DE FILTRO LATERAL ---
    st.sidebar.markdown("<h3 style='color: #818cf8;'>⚙️ Parámetros del Mapa</h3>", unsafe_allow_html=True)
    
    # 1. Slider para seleccionar el año de análisis
    available_years = sorted(df['year'].unique())
    selected_year = st.sidebar.slider(
        "Año de análisis",
        min_value=int(min(available_years)),
        max_value=int(max(available_years)),
        value=int(max(available_years)),
        step=1
    )

    # 2. Selector de tipo de proyección del mapa
    map_projection_lbl = st.sidebar.selectbox(
        "Proyección del mapa",
        options=["🗺️ Plano (Equirrectangular)", "🌐 Globo 3D (Ortográfico)"],
        index=0
    )
    map_projection = "equirectangular" if "Plano" in map_projection_lbl else "orthographic"

    # 3. Selector de la variable a visualizar
    metric_dict = {
        "Puntaje de Felicidad": "score",
        "Contribución del PIB": "gdp",
        "Apoyo Social": "social",
        "Esperanza de Vida": "health",
        "Libertad de Elección": "freedom",
        "Generosidad": "generosity",
        "Confianza (Percepción de Corrupción)": "trust",
        "Residuo de Distopía": "dystopia_residual"
    }
    
    selected_metric_lbl = st.sidebar.selectbox(
        "Métrica a visualizar",
        options=list(metric_dict.keys()),
        index=0
    )
    selected_metric_col = metric_dict[selected_metric_lbl]

    # Filtrar datos por año
    df_year = df[df['year'] == selected_year]

    # --- SECCIÓN DE MÉTRICAS CLAVE (KPIs con Glassmorphic Design) ---
    col1, col2, col3 = st.columns(3)
    
    # Calcular estadísticas
    avg_value = df_year[selected_metric_col].mean()
    max_idx = df_year[selected_metric_col].idxmax()
    min_idx = df_year[selected_metric_col].idxmin()
    
    country_max = df_year.loc[max_idx, 'country']
    val_max = df_year.loc[max_idx, selected_metric_col]
    
    country_min = df_year.loc[min_idx, selected_metric_col]
    # Evitar errores si hay varios con el mismo valor mínimo, tomamos el primero
    row_min = df_year.loc[min_idx]
    country_min = row_min['country']
    val_min = row_min[selected_metric_col]

    with col1:
        st.markdown(f"""
            <div class='glass-card'>
                <div class='metric-lbl'>Promedio Global</div>
                <div class='metric-val'>{avg_value:.3f}</div>
                <div class='metric-sub'>Promedio ponderado global en {selected_year}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class='glass-card'>
                <div class='metric-lbl'>Líder del Factor</div>
                <div class='metric-val'>{val_max:.3f}</div>
                <div class='metric-sub'>🥇 {country_max}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class='glass-card'>
                <div class='metric-lbl'>Cola del Factor</div>
                <div class='metric-val'>{val_min:.3f}</div>
                <div class='metric-sub'>⚠️ {country_min}</div>
            </div>
        """, unsafe_allow_html=True)

    # --- MAPA DE COROPLETAS CON TABS ---
    st.markdown("<h3 style='margin-top: 1.5rem; margin-bottom: 0.5rem;'> Visualización de Mapas Interactivos</h3>", unsafe_allow_html=True)
    
    tab_map1, tab_map2 = st.tabs(["Estado Actual", "Variación Histórica (Delta)"])
    
    with tab_map1:
        st.markdown(f"<p style='color: #9ca3af; font-size: 0.95rem; margin-bottom: 1rem;'>Visualización interactiva de <b>{selected_metric_lbl}</b> en el año <b>{selected_year}</b>. Puedes interactuar directamente con el mapa para ver los detalles.</p>", unsafe_allow_html=True)
        
        # Crear mapa de coropletas interactivo con Plotly Express
        fig_map = px.choropleth(
            df_year,
            locations="iso_alpha",
            color=selected_metric_col,
            hover_name="country",
            hover_data={
                "iso_alpha": False,
                "score": ":.2f",
                "gdp": ":.2f",
                "social": ":.2f",
                "health": ":.2f",
                "freedom": ":.2f",
                "generosity": ":.2f",
                "trust": ":.2f"
            },
            color_continuous_scale=px.colors.sequential.Plasma,
            title=None
        )
        
        # Personalización del estilo del mapa
        fig_map.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type=map_projection,
                bgcolor='rgba(0,0,0,0)',
                landcolor='#1f2937',
                lakecolor='#0e1117',
                coastlinecolor='#4b5563',
                showland=True,
                showlakes=True,
                subunitcolor='#4b5563'
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis=dict(
                colorbar=dict(
                    title=dict(text=selected_metric_lbl, side='right', font=dict(size=12, color='#9ca3af')),
                    tickfont=dict(color='#9ca3af')
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=550
        )
        
        st.plotly_chart(fig_map, use_container_width=True, theme="streamlit")
        
    with tab_map2:
        st.markdown(f"<p style='color: #9ca3af; font-size: 0.95rem; margin-bottom: 1rem;'>Compara y analiza de forma interactiva la variación de <b>{selected_metric_lbl}</b> entre dos años seleccionados.</p>", unsafe_allow_html=True)
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            start_year = st.selectbox("Año inicial", options=available_years, index=0)
        with col_d2:
            end_year = st.selectbox("Año final", options=available_years, index=len(available_years)-1)
            
        if start_year >= end_year:
            st.warning("Selecciona un año inicial que sea estrictamente anterior al año final para poder ver la evolución de forma correcta.")
        else:
            # Calcular delta
            df_start = df[df['year'] == start_year][['country', 'iso_alpha', selected_metric_col]]
            df_end = df[df['year'] == end_year][['country', 'iso_alpha', selected_metric_col]]
            df_delta = pd.merge(df_start, df_end, on=['country', 'iso_alpha'], suffixes=('_start', '_end'))
            df_delta['delta'] = df_delta[selected_metric_col + '_end'] - df_delta[selected_metric_col + '_start']
            
            # Crear mapa de delta con escala de color divergente
            fig_delta = px.choropleth(
                df_delta,
                locations="iso_alpha",
                color="delta",
                hover_name="country",
                hover_data={
                    "iso_alpha": False,
                    selected_metric_col + '_start': ":.2f",
                    selected_metric_col + '_end': ":.2f",
                    "delta": ":.2f"
                },
                color_continuous_scale=px.colors.diverging.RdYlGn,
                color_continuous_midpoint=0,
                title=None
            )
            
            fig_delta.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type=map_projection,
                    bgcolor='rgba(0,0,0,0)',
                    landcolor='#1f2937',
                    lakecolor='#0e1117',
                    coastlinecolor='#4b5563',
                    showland=True,
                    showlakes=True,
                    subunitcolor='#4b5563'
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                coloraxis=dict(
                    colorbar=dict(
                        title=dict(text="Variación (Delta)", side='right', font=dict(size=12, color='#9ca3af')),
                        tickfont=dict(color='#9ca3af')
                    )
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=550
            )
            
            st.plotly_chart(fig_delta, use_container_width=True, theme="streamlit")


    st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.08); margin: 2rem 0;' />", unsafe_allow_html=True)

    # --- SECCIÓN DE ANÁLISIS DE CORRELACIÓN (SCATTER PLOT) ---
    st.markdown("<h3>Análisis de Correlación Socioeconómica</h3>", unsafe_allow_html=True)
    
    # Widgets de control para el Scatter Plot colocados en columnas
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        x_var_lbl = st.selectbox(
            "Variable Eje X",
            options=list(metric_dict.keys()),
            index=1 # Contribución del PIB por defecto
        )
        x_var_col = metric_dict[x_var_lbl]
        
    with s_col2:
        y_var_lbl = st.selectbox(
            "Variable Eje Y",
            options=list(metric_dict.keys()),
            index=0 # Puntaje de felicidad por defecto
        )
        y_var_col = metric_dict[y_var_lbl]

    # Crear Scatter Plot con Plotly Express
    fig_scatter = px.scatter(
        df_year,
        x=x_var_col,
        y=y_var_col,
        color="region",
        size="score",
        hover_name="country",
        hover_data={
            "score": ":.2f",
            "region": True
        },
        labels={
            x_var_col: x_var_lbl,
            y_var_col: y_var_lbl,
            "region": "Región",
            "score": "Felicidad"
        },
        color_discrete_sequence=px.colors.qualitative.Safe,
        opacity=0.85
    )

    # Estilo del Scatter Plot
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(17, 24, 39, 0.3)',
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)',
            title=dict(font=dict(size=14, color='#f3f4f6')),
            tickfont=dict(color='#9ca3af')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)',
            title=dict(font=dict(size=14, color='#f3f4f6')),
            tickfont=dict(color='#9ca3af')
        ),
        legend=dict(
            bgcolor='rgba(31, 41, 55, 0.6)',
            bordercolor='rgba(255,255,255,0.08)',
            borderwidth=1,
            font=dict(color='#f3f4f6')
        ),
        height=500
    )

    st.plotly_chart(fig_scatter, use_container_width=True, theme="streamlit")

    st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.08); margin: 2rem 0;' />", unsafe_allow_html=True)

    # --- SECCIÓN DE DISTRIBUCIÓN REGIONAL (VIOLIN PLOT) ---
    st.markdown("<h3>Distribución Regional del Bienestar</h3>", unsafe_allow_html=True)
    st.write(f"El siguiente diagrama de violín desglosa la distribución estadística y densidad del **{selected_metric_lbl}** en las distintas regiones del planeta para el año **{selected_year}**.")

    fig_violin = px.violin(
        df_year,
        y=selected_metric_col,
        x="region",
        color="region",
        box=True, # Mostrar boxplot dentro
        points="all", # Mostrar todos los puntos
        hover_name="country",
        labels={
            selected_metric_col: selected_metric_lbl,
            "region": "Región"
        },
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig_violin.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(17, 24, 39, 0.3)',
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            title=dict(font=dict(size=14, color='#f3f4f6')),
            tickfont=dict(color='#9ca3af')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)',
            title=dict(font=dict(size=14, color='#f3f4f6')),
            tickfont=dict(color='#9ca3af')
        ),
        showlegend=False,
        height=450
    )

    st.plotly_chart(fig_violin, use_container_width=True, theme="streamlit")
else:
    st.warning("No hay datos disponibles para mostrar. Asegúrate de ejecutar el script ETL.")

