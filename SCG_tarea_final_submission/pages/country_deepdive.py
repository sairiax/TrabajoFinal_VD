import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. Inyección de CSS personalizado para estética premium
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

        /* Tarjeta Glassmorphic */
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
            color: #ec4899;
            margin: 5px 0;
            text-shadow: 0 0 10px rgba(236, 72, 153, 0.2);
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

# 2. Cargar datos con caché
@st.cache_data
def load_data():
    file_path = 'cleaned_world_happiness.csv'
    if not os.path.exists(file_path):
        st.error("No se encontró el archivo de datos. Por favor, ejecuta 'etl_process.py' primero.")
        return pd.DataFrame()
    return pd.read_csv(file_path)

# Configurar vista
inject_custom_css()

# Cargar dataset
df = load_data()

if not df.empty:
    st.markdown("<h1 class='title-gradient'>📊 Análisis de Detalle por País</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle-custom'>Examina la evolución temporal de un país, desglosa los factores de su felicidad y realiza comparativas directas</p>", unsafe_allow_html=True)

    # --- WIDGETS DE FILTRO LATERAL ---
    st.sidebar.markdown("<h3 style='color: #ec4899;'>⚙️ Selección de País</h3>", unsafe_allow_html=True)
    
    # 1. Selector de país principal
    country_list = sorted(df['country'].unique())
    
    # Intentar seleccionar un país por defecto que sea de interés (e.g. España si está disponible)
    default_country_index = 0
    if "Spain" in country_list:
        default_country_index = country_list.index("Spain")
    elif "España" in country_list:
        default_country_index = country_list.index("España")
        
    selected_country = st.sidebar.selectbox(
        "País principal",
        options=country_list,
        index=default_country_index
    )

    # 2. Selector de año para el desglose de factores
    available_years = sorted(df[df['country'] == selected_country]['year'].unique())
    selected_year = st.sidebar.slider(
        "Año de desglose",
        min_value=int(min(available_years)),
        max_value=int(max(available_years)),
        value=int(max(available_years)),
        step=1
    )

    # Filtrar datos para el país principal
    df_country = df[df['country'] == selected_country].sort_values('year')
    df_country_year = df_country[df_country['year'] == selected_year]

    if not df_country_year.empty:
        # Calcular estadísticas rápidas para la cabecera
        current_score = df_country_year['score'].values[0]
        region_country = df_country_year['region'].values[0]
        subregion_country = df_country_year['sub_region'].values[0]
        
        # Calcular ranking del país en el año seleccionado
        df_year_ranking = df[df['year'] == selected_year].sort_values('score', ascending=False).reset_index(drop=True)
        ranking = df_year_ranking[df_year_ranking['country'] == selected_country].index[0] + 1
        total_countries = len(df_year_ranking)

        # KPIs del País
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class='glass-card'>
                    <div class='metric-lbl'>Puntaje General</div>
                    <div class='metric-val'>{current_score:.3f}</div>
                    <div class='metric-sub'>Indice de felicidad en {selected_year}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='glass-card'>
                    <div class='metric-lbl'>Posición en Ranking</div>
                    <div class='metric-val'>#{ranking} / {total_countries}</div>
                    <div class='metric-sub'>Puesto mundial en el año {selected_year}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class='glass-card'>
                    <div class='metric-lbl'>Ubicación Geográfica</div>
                    <div class='metric-val' style='font-size: 1.6rem; color: #a855f7; margin-top: 13px;'>{region_country}</div>
                    <div class='metric-sub'>{subregion_country}</div>
                </div>
            """, unsafe_allow_html=True)

        # --- 1. GRÁFICA DE LÍNEA: EVOLUCIÓN HISTÓRICA CON ROLLING MEAN ---
        st.markdown(f"<h3>Evolución Temporal del Puntaje de Felicidad: {selected_country}</h3>", unsafe_allow_html=True)
        
        # Calcular media móvil (Rolling Mean) de 2 años en Streamlit para suavizar la tendencia
        df_country['rolling_score'] = df_country['score'].rolling(window=2, min_periods=1).mean()
        
        # Unir ambas columnas para graficar con Plotly
        df_melted = df_country.melt(
            id_vars=['year'],
            value_vars=['score', 'rolling_score'],
            var_name='Tipo',
            value_name='Puntaje'
        )
        df_melted['Tipo'] = df_melted['Tipo'].replace({
            'score': 'Puntaje Anual',
            'rolling_score': 'Media Móvil (2 años)'
        })

        fig_line = px.line(
            df_melted,
            x='year',
            y='Puntaje',
            color='Tipo',
            markers=True,
            color_discrete_sequence=['#ec4899', '#a855f7'],
            labels={'year': 'Año', 'Puntaje': 'Puntaje de Felicidad'}
        )
        
        # Configurar estilo de línea discontinua para la media móvil
        fig_line.data[1].line.dash = 'dash'
        fig_line.data[1].line.width = 2
        fig_line.data[0].line.width = 4

        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17, 24, 39, 0.3)',
            margin=dict(l=40, r=40, t=20, b=40),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                zerolinecolor='rgba(255,255,255,0.1)',
                title=dict(font=dict(size=14, color='#f3f4f6')),
                tickfont=dict(color='#9ca3af'),
                tickmode='linear',
                tick0=2015,
                dtick=1
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                zerolinecolor='rgba(255,255,255,0.1)',
                title=dict(font=dict(size=14, color='#f3f4f6')),
                tickfont=dict(color='#9ca3af'),
                range=[max(0.0, df_country['score'].min() - 0.5), min(10.0, df_country['score'].max() + 0.5)]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f3f4f6')
            ),
            height=350
        )
        st.plotly_chart(fig_line, use_container_width=True, theme="streamlit")

        st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.08); margin: 2rem 0;' />", unsafe_allow_html=True)

        # --- 2. GRÁFICA DE BARRAS APILADAS: DESGLOSE DE FACTORES DE FELICIDAD ---
        st.markdown(f"<h3>Desglose de Contribución por Factores ({selected_year})</h3>", unsafe_allow_html=True)
        st.write("El puntaje total de felicidad es la suma de los valores explicados por el PIB, Apoyo Social, Salud, Libertad, Generosidad y Confianza, más el residuo de la Distopía (un país hipotético con la felicidad más baja del mundo en cada dimensión).")
        
        # Organizar factores para el gráfico
        factors_names = {
            'gdp': 'Contribución PIB',
            'social': 'Apoyo Social',
            'health': 'Esperanza de Vida',
            'freedom': 'Libertad de Elección',
            'generosity': 'Generocidad',
            'trust': 'Confianza (Corrupción)',
            'dystopia_residual': 'Residuo de Distopía'
        }
        
        # Extraer fila
        row = df_country_year.iloc[0]
        factor_values = []
        for col_name, display_name in factors_names.items():
            factor_values.append({
                'Factor': display_name,
                'Contribución': row[col_name],
                'País': selected_country
            })
        df_factors = pd.DataFrame(factor_values)

        # Gráfico de barras apiladas horizontales (una sola barra que muestra la composición total)
        fig_bar_stack = px.bar(
            df_factors,
            x='Contribución',
            y='País',
            color='Factor',
            orientation='h',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={'Contribución': 'Puntaje acumulado', 'País': 'País'}
        )

        fig_bar_stack.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=10, b=40),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                title=dict(font=dict(size=14, color='#f3f4f6')),
                tickfont=dict(color='#9ca3af'),
                range=[0, 8.0] # La puntuación máxima histórica ronda 7.8-7.9
            ),
            yaxis=dict(
                showticklabels=False,
                title=None
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.5,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f3f4f6')
            ),
            height=250
        )
        st.plotly_chart(fig_bar_stack, use_container_width=True, theme="streamlit")

        st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.08); margin: 2.5rem 0;' />", unsafe_allow_html=True)

        # --- 3. COMPARATIVA LADO A LADO ENTRE DOS PAÍSES (GRÁFICA DE BARRAS AGRUPADAS) ---
        st.markdown("<h3>Comparador Comparativo entre Países</h3>", unsafe_allow_html=True)
        
        # Eliminar el país principal de la lista para la comparación
        compare_country_list = [c for c in country_list if c != selected_country]
        
        # Seleccionar país para comparar
        default_comp_index = 0
        if "Finland" in compare_country_list:
            default_comp_index = compare_country_list.index("Finland")
            
        selected_compare_country = st.selectbox(
            "Selecciona un segundo país para comparar:",
            options=compare_country_list,
            index=default_comp_index
        )
        
        # Filtrar datos de ambos países para el año seleccionado
        df_comp_a = df_country_year
        df_comp_b = df[(df['country'] == selected_compare_country) & (df['year'] == selected_year)]
        
        if not df_comp_b.empty:
            # Crear DataFrame unificado de factores para la comparación
            comparison_rows = []
            for col_name, display_name in factors_names.items():
                if col_name != 'dystopia_residual': # Comparar solo las dimensiones primarias
                    comparison_rows.append({
                        'Dimensión': display_name,
                        'Valor': df_comp_a[col_name].values[0],
                        'País': selected_country
                    })
                    comparison_rows.append({
                        'Dimensión': display_name,
                        'Valor': df_comp_b[col_name].values[0],
                        'País': selected_compare_country
                    })
            df_compare = pd.DataFrame(comparison_rows)

            # Gráfico de barras agrupadas
            fig_compare = px.bar(
                df_compare,
                x='Dimensión',
                y='Valor',
                color='País',
                barmode='group',
                color_discrete_sequence=['#6366f1', '#10b981'],
                labels={'Valor': 'Valor de Contribución', 'Dimensión': 'Dimensión de Bienestar'}
            )

            fig_compare.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(17, 24, 39, 0.3)',
                margin=dict(l=40, r=40, t=20, b=40),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    title=None,
                    tickfont=dict(color='#9ca3af')
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    zerolinecolor='rgba(255,255,255,0.1)',
                    title=dict(font=dict(size=14, color='#f3f4f6')),
                    tickfont=dict(color='#9ca3af')
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#f3f4f6')
                ),
                height=400
            )

            # --- NUEVA GRÁFICA DE RADAR (SPIDER CHART) PARA COMPARACIÓN MULTIDIMENSIONAL ---
            dimensions = ['gdp', 'social', 'health', 'freedom', 'generosity', 'trust']
            dimension_names = ['PIB per Cápita', 'Apoyo Social', 'Esperanza de Vida', 'Libertad', 'Generosidad', 'Confianza']
            
            # Obtener valores máximos históricos en todo el dataset para normalizar en el rango [0, 1]
            # Esto corrige la distorsión visual causada por las diferentes escalas de las métricas (ej. PIB vs Confianza).
            max_values = {col: df[col].max() if df[col].max() > 0 else 1.0 for col in dimensions}
            
            val_a = [df_comp_a[col].values[0] for col in dimensions]
            val_b = [df_comp_b[col].values[0] for col in dimensions]
            
            # Calcular valores normalizados
            val_a_norm = [val_a[i] / max_values[dimensions[i]] for i in range(len(dimensions))]
            val_b_norm = [val_b[i] / max_values[dimensions[i]] for i in range(len(dimensions))]
            
            # Para cerrar el loop del gráfico de radar en Plotly
            val_a_close = val_a_norm + [val_a_norm[0]]
            val_b_close = val_b_norm + [val_b_norm[0]]
            dimension_names_close = dimension_names + [dimension_names[0]]
            
            # Textos informativos de alta calidad para el tooltip (hovertext)
            hover_text_a = [
                f"<b>{selected_country} - {dimension_names[i]}</b><br>"
                f"Porcentaje del Máx Histórico: {val_a_norm[i]*100:.1f}%<br>"
                f"Contribución Real Bruta: {val_a[i]:.3f}"
                for i in range(len(dimensions))
            ]
            hover_text_b = [
                f"<b>{selected_compare_country} - {dimension_names[i]}</b><br>"
                f"Porcentaje del Máx Histórico: {val_b_norm[i]*100:.1f}%<br>"
                f"Contribución Real Bruta: {val_b[i]:.3f}"
                for i in range(len(dimensions))
            ]
            
            hover_text_a_close = hover_text_a + [hover_text_a[0]]
            hover_text_b_close = hover_text_b + [hover_text_b[0]]
            
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=val_a_close,
                theta=dimension_names_close,
                fill='toself',
                name=selected_country,
                line_color='#6366f1',
                fillcolor='rgba(99, 102, 241, 0.15)',
                hovertext=hover_text_a_close,
                hoverinfo="text"
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=val_b_close,
                theta=dimension_names_close,
                fill='toself',
                name=selected_compare_country,
                line_color='#10b981',
                fillcolor='rgba(16, 185, 129, 0.15)',
                hovertext=hover_text_b_close,
                hoverinfo="text"
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1.05],
                        tickformat=".0%", # Mostrar escala de porcentaje en los ejes
                        gridcolor='rgba(255, 255, 255, 0.08)',
                        linecolor='rgba(255, 255, 255, 0.1)',
                        tickfont=dict(color='#9ca3af')
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(255, 255, 255, 0.08)',
                        linecolor='rgba(255, 255, 255, 0.1)',
                        tickfont=dict(color='#cbd5e1')
                    ),
                    bgcolor='rgba(17, 24, 39, 0.3)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=30, b=30),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.18,
                    xanchor="center",
                    x=0.5,
                    font=dict(color='#f3f4f6')
                ),
                height=450
            )

            # Renderizado de pestañas comparativas
            tab_comp1, tab_comp2 = st.tabs(["Perfil Multidimensional Normalizado (Radar)", "Magnitudes Comparadas Reales (Barras)"])
            
            with tab_comp1:
                st.markdown(f"<p style='color: #9ca3af; font-size: 0.95rem; margin-bottom: 1rem;'>El gráfico de radar superpone los perfiles multidimensionales normalizados (donde 100% representa el valor máximo histórico registrado en todo el conjunto de datos para cada factor). Esto permite evaluar fortalezas y debilidades relativas de forma equilibrada y comparable.</p>", unsafe_allow_html=True)
                st.plotly_chart(fig_radar, use_container_width=True, theme="streamlit")
                
            with tab_comp2:
                st.markdown(f"<p style='color: #9ca3af; font-size: 0.95rem; margin-bottom: 1rem;'>Visualización de magnitudes de contribución reales y absolutas en un diagrama de barras agrupadas.</p>", unsafe_allow_html=True)
                st.plotly_chart(fig_compare, use_container_width=True, theme="streamlit")
        else:
            st.info(f"No hay datos registrados de {selected_compare_country} para el año {selected_year}.")

    else:
        st.warning("No hay registros disponibles para el año seleccionado.")
else:
    st.warning("No hay datos disponibles para mostrar. Asegúrate de ejecutar el script ETL.")


