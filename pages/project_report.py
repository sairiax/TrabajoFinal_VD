import streamlit as st
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
            padding: 24px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
        }
        .glass-card:hover {
            border-color: rgba(168, 85, 247, 0.3);
            box-shadow: 0 10px 40px rgba(168, 85, 247, 0.1);
        }

        /* Títulos de sección internos */
        .section-title {
            color: #a855f7;
            font-weight: 700;
            font-size: 1.6rem;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            border-bottom: 1px solid rgba(168, 85, 247, 0.2);
            padding-bottom: 6px;
        }
        
        /* Enfatizar texto */
        .highlight-text {
            color: #818cf8;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

# Configurar vista
inject_custom_css()

st.markdown("<h1 class='title-gradient'>📝 Memoria e Informe Académico</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-custom'>Documentación formal, metodología metodológica y conclusiones del análisis del bienestar mundial</p>", unsafe_allow_html=True)

st.markdown("""
<div class='glass-card'>
    <div class='section-title'>1. Resumen Ejecutivo</div>
    <p>
        Este proyecto presenta una plataforma interactiva de inteligencia de datos diseñada para analizar de forma 
        longitudinal los factores socioeconómicos que determinan la felicidad percibida a nivel mundial en el período 
        comprehendido entre <span class='highlight-text'>2015 y 2023</span>. Mediante técnicas avanzadas de visualización de datos 
        web y un robusto procesamiento ETL, el dashboard permite a investigadores, académicos y decisores políticos 
        explorar patrones macrogeográficos, desglosar dinámicas nacionales y realizar comparativas micro-analíticas 
        de bienestar multidimensional.
    </p>
</div>

<div class='glass-card'>
    <div class='section-title'>2. Metodología y Calidad del DataSet</div>
    <p>
        Para superar las limitaciones de los datasets de juguete tradicionales, esta aplicación se nutre de un 
        <b>proceso de fusión y estandarización de datos multi-fuente</b> totalmente automatizado en <code>etl_process.py</code>:
    </p>
    <ul>
        <li><b>World Happiness Report (2015-2023):</b> Extracción de los datasets históricos del repositorio de Gallup y Earth Institute, resolviendo la severa inconsistencia en los esquemas de nombres de columnas anuales (e.g., variando de <i>"Family"</i> a <i>"Social support"</i>).</li>
        <li><b>Base de Datos Geográfica Oficial (ISO-3166):</b> Integración del estándar internacional ISO de códigos de países y regiones geográficas de Luke's Repository para enriquecer cada fila con el código de tres letras <code>iso_alpha</code> y agrupaciones regionales/subregionales de la ONU.</li>
        <li><b>Cálculo del Residuo de Distopía:</b> Recalculado de forma matemática consistente: <code>Dystopia = Score - (GDP + Social + Health + Freedom + Generosity + Trust)</code> para garantizar la coherencia aditiva perfecta en la visualización apilada.</li>
    </ul>
    <p>
        El resultado de este pipeline es un conjunto unificado de <span class='highlight-text'>1367 registros</span>, con <b>cero datos faltantes (0 nulls)</b>, 100% georreferenciado de forma limpia y listo para la visualización geoespacial sin lagunas.
    </p>
</div>

<div class='glass-card'>
    <div class='section-title'>3. Análisis de Visualización Espacial (Mapas)</div>
    <p>
        La dimensión geopolítica del bienestar se aborda mediante dos herramientas geoespaciales avanzadas y de alta interacción:
    </p>
    <ol>
        <li>
            <b>Mapa del Estado Actual (2D vs. Globo 3D):</b> Permite cambiar entre la proyección clásica Equirrectangular y una 
            proyección Ortográfica que renderiza la Tierra como un globo tridimensional interactivo. Este mapa revela una 
            marcada segregación macro-regional: los niveles más altos de felicidad se concentran de forma persistente en 
            Europa del Norte, Norteamérica y Oceanía, mientras que el África subsahariana y zonas del sur de Asia registran 
            los niveles más bajos.
        </li>
        <li>
            <b>Mapa de Variación Histórica (Delta Map):</b> Es una herramienta analítica clave que calcula la diferencia 
            algebraica del índice seleccionado entre dos momentos temporales. Al usar una escala de color divergente 
            (rojo-amarillo-verde) centrada en cero, identifica de inmediato el progreso social (e.g., el crecimiento sostenido de 
            Europa del Este como Rumanía y Bulgaria) o el colapso institucional en regiones desestabilizadas.
        </li>
    </ol>
</div>

<div class='glass-card'>
    <div class='section-title'>4. Análisis de Correlaciones y Distribución Estadística</div>
    <p>
        El análisis multidimensional y estadístico de las gráficas aporta dos revelaciones primordiales:
    </p>
    <ul>
        <li>
            <b>Correlación Socioeconómica:</b> El diagrama de dispersión interactivo muestra una relación fuertemente positiva 
            y no lineal entre el PIB per cápita y el apoyo social frente al puntaje de felicidad general. No obstante, se observa 
            un efecto de rendimientos decrecientes: una vez alcanzado cierto umbral de desarrollo material (PIB > 1.5), la felicidad 
            tiende a estabilizarse, lo que corrobora la <i>Paradoja de Easterlin</i>.
        </li>
        <li>
            <b>Heterogeneidad y Dispersión Regional (Violin Plot):</b> El diagrama de violín expone con claridad que Europa 
            no solo tiene la media de felicidad más elevada, sino también la distribución más concentrada en la parte superior, 
            indicando baja desigualdad de bienestar. En contraste, América Latina muestra una gran dispersión, y África y Oriente 
            Medio revelan distribuciones bimodales o colas muy largas que delatan severas brechas y polarizaciones internas.
        </li>
    </ul>
</div>

<div class='glass-card'>
    <div class='section-title'>5. Casos de Estudio y Análisis Multidimensional (Radar)</div>
    <p>
        Mediante el <b>Gráfico de Radar Interactivo</b> implementado en el desglose de países, se pueden contrastar perfiles específicos:
    </p>
    <ul>
        <li>
            <b>El Modelo Nórdico (Finlandia vs. Resto del Mundo):</b> Finlandia, líder indiscutible del ranking, no siempre 
            sobresale con el PIB per cápita más alto, pero su perfil de bienestar es excepcionalmente equilibrado, registrando 
            los niveles máximos del planeta en <i>Apoyo Social</i> y <i>Confianza (Percepción de Corrupción extremadamente baja)</i>. 
            Esto demuestra que la estabilidad social y la gobernanza honesta son pilares más determinantes que el simple crecimiento industrial.
        </li>
        <li>
            <b>El Impacto de la Crisis (Caso Venezuela):</b> Al aplicar el mapa Delta o la línea de tiempo sobre Venezuela, se 
            visualiza una dramática caída de felicidad de más de 2 puntos entre 2015 y 2018, explicada directamente por el desplome 
            del PIB y de la <i>Libertad de Elección</i>, acompañada por un incremento masivo en la percepción de corrupción.
        </li>
    </ul>
</div>

<div class='glass-card'>
    <div class='section-title'>6. Conclusiones y Propuestas Políticas</div>
    <p>
        El análisis longitudinal del bienestar mundial conduce a tres conclusiones fundamentales:
    </p>
    <ol>
        <li>
            <b>El Bienestar es Multidimensional:</b> El crecimiento económico (PIB) es una condición necesaria pero no suficiente 
            para alcanzar niveles óptimos de felicidad colectiva. Los factores intangibles, como la red de seguridad social 
            (apoyo familiar y comunitario) y la libertad para tomar decisiones, actúan como los verdaderos cimientos del bienestar.
        </li>
        <li>
            <b>El Factor Corrupción como Ancla Social:</b> Los datos empíricos demuestran que una baja confianza institucional 
            (percepción de alta corrupción) actúa como un techo insalvable para el desarrollo subjetivo, limitando severamente la 
            efectividad de los ingresos económicos de un país.
        </li>
        <li>
            <b>Gobernanza basada en la Felicidad:</b> Este dashboard prueba la viabilidad y necesidad de que los gobiernos 
            adopten indicadores multidimensionales (como el Índice de Felicidad) como métricas de éxito del desarrollo nacional, 
            en lugar de depender de forma exclusiva de variables macroeconómicas crudas como el PIB monetario.
        </li>
    </ol>
</div>
""", unsafe_allow_html=True)


