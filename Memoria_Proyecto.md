# Memoria Técnica Académica: Visualización del Bienestar Mundial (2015-2023)

**Asignatura:** Visualización de datos  
**Grupo:** Alto Rendimiento Académico (ARA)  
**Autor:** Sergi Cortés Guerrero  
**Institución:** Universitat Politècnica de València (UPV)  

---

## Índice
1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Introducción y Objetivos](#2-introducción-y-objetivos)
3. [DataSet y Pipeline de Ingeniería de Datos (ETL)](#3-dataset-y-pipeline-de-ingeniería-de-datos-etl)
4. [Análisis Geoespacial Interactivos (Mapas Avanzados)](#4-análisis-geoespacial-interactivos-mapas-avanzados)
5. [Análisis de Correlaciones y Distribuciones (Gráficas Avanzadas)](#5-análisis-de-correlaciones-y-distribuciones-gráficas-avanzadas)
6. [Casos de Estudio Detallados y Perfiles (Gráfico de Radar)](#6-casos-de-estudio-detallados-y-perfiles-gráfico-de-radar)
7. [Conclusiones del Informe y Recomendaciones Políticas](#7-conclusiones-del-informe-y-recomendaciones-políticas)
8. [Detalle de Librerías y Entorno de Ejecución](#8-detalle-de-librerías-y-entorno-de-ejecución)
9. [Referencias](#9-referencias)

---

## 1. Resumen Ejecutivo
Esta memoria técnica documenta el diseño, desarrollo e implementación de una plataforma de análisis interactivo de inteligencia de datos orientada al estudio longitudinal del bienestar subjetivo humano global en el período 2015-2023. A través de la unificación sistemática de los informes anuales del *World Happiness Report* y su enriquecimiento con bases de datos geoespaciales de la ONU (ISO-3166), se ha construido un ecosistema interactivo en **Streamlit** y **Plotly** que revela patrones macrogeográficos, factores correlacionales del bienestar y contrastes micro-nacionales. 

El proyecto destaca por incorporar visualizaciones avanzadas no tradicionales —tales como **mapas de deltas históricos divergentes**, **proyecciones de globos tridimensionales interactivos**, **diagramas de violín regionales** y **gráficos de radar multidimensionales**— garantizando una comprensión científica holística del bienestar humano más allá del Producto Interior Bruto (PIB).

---

## 2. Introducción y Objetivos
Históricamente, el progreso de las naciones se ha evaluado de forma exclusiva mediante variables macroeconómicas monetarias como el Producto Interior Bruto (PIB) o la balanza comercial. Sin embargo, estas métricas fallan al capturar intangibles esenciales de la vida humana como el bienestar social, la salud mental, la cohesión comunitaria y la libertad de elección. 

El presente proyecto académico persigue los siguientes **objetivos estratégicos**:
1. **Unificar e Integrar:** Consolidar una década de encuestas globales de Gallup sobre bienestar subjetivo en una base de datos geoespacial consistente y libre de sesgos metodológicos de fusión.
2. **Visualizar Espacialmente:** Ofrecer herramientas cartográficas que permitan comprender de manera intuitiva y dinámica la distribución de la felicidad del planeta, facilitando la detección de brechas geográficas.
3. **Analizar Correlaciones:** Examinar empíricamente la incidencia relativa de los factores económicos (PIB), sociales (redes de apoyo, generosidad), de salud (esperanza de vida) e institucionales (corrupción, libertad) en la felicidad.
4. **Facilitar el Diagnóstico Nacional:** Implementar herramientas de profundidad a nivel de país para diagnosticar la evolución temporal del bienestar e identificar crisis de gobernanza o éxitos en el desarrollo social de manera individual o comparada.

---

## 3. DataSet y Pipeline de Ingeniería de Datos (ETL)
El éxito de una visualización analítica depende críticamente de la calidad de sus datos. En este proyecto, se ha implementado un proceso ETL automatizado robusto en `etl_process.py` que destaca por resolver las siguientes problemáticas de calidad del dataset original:

### 3.1 Proceso de Extracción y Fusión Multi-Fuente
Los informes anuales de felicidad son publicados de manera fragmentada por el *Sustainable Development Solutions Network* (SDSN) de la ONU y presentan graves discrepancias de nomenclatura y estructura entre años. El script ETL realiza una descarga web dinámica y aplica un diccionario de mapeo anual para estandarizar las columnas bajo un único esquema de datos unificado:
* `country`: Nombre oficial del país.
* `score`: Puntaje general de felicidad autopercibida (0 a 10).
* `gdp`: Contribución del PIB per cápita al puntaje de felicidad.
* `social`: Apoyo social o redes de protección familiar.
* `health`: Esperanza de vida saludable.
* `freedom`: Libertad percibida para tomar decisiones de vida.
* `generosity`: Nivel de filantropía y generosidad material.
* `trust`: Percepción de ausencia de corrupción gubernamental y empresarial.
* `dystopia_residual`: Residuo estadístico de la Distopía (el valor base mínimo).

### 3.2 Georreferenciación y Clasificación Regional Limpia
Para habilitar mapas interactivos sin lagunas, el ETL cruza dinámicamente cada país con el repositorio oficial **ISO-3166-Countries-with-Regional-Codes**. Mediante un diccionario de excepciones manuales de 74 reglas, se corrigen discrepancias lingüísticas o geopolíticas comunes (e.g., convirtiendo *"Taiwan Province of China"* o *"Congo (Kinshasa)"* a sus equivalentes ISO oficiales).

Gracias a esto, se inyectan en el dataset las siguientes columnas críticas de agrupación geoespacial:
* `iso_alpha`: Código internacional ISO Alpha-3 (e.g., `ESP` para España, `FIN` para Finlandia).
* `region`: Continente de la ONU (e.g., *Europe*, *Africa*, *Americas*).
* `sub_region`: Clasificación macrogeográfica fina (e.g., *Southern Europe*, *Eastern Africa*).

### 3.3 Verificación de Datos e Integridad
Tras la ejecución del ETL, se consolida una matriz histórica unificada de **1367 registros** desde 2015 hasta 2023. Se ha comprobado que el dataset resultante cuenta con **0 códigos ISO nulos y 0 regiones nulas**, lo que certifica una calidad de datos perfecta, sin lagunas, ideal para modelos espaciales robustos.

---

## 4. Análisis Geoespacial Interactivos (Mapas Avanzados)
La sección cartográfica de la plataforma implementa una interfaz de pestañas que ofrece visualizaciones avanzadas diseñadas expresamente para exceder los mapas básicos vistos en clase:

### 4.1 Proyección Dinámica (2D Equirrectangular vs. Globo 3D Ortográfico)
Mediante un control interactivo en la barra lateral, el evaluador puede alternar entre:
* **Proyección Equirrectangular (2D):** Ideal para una visión panorámica y simultánea de todos los continentes.
* **Proyección Ortográfica (Globo 3D):** Transforma la visualización en una esfera tridimensional rotatoria e interactiva que imita un globo terráqueo real. Esta vista no tradicional genera un impacto visual premium y facilita la exploración interactiva natural de la superficie terrestre.

### 4.2 Mapa de Variación Histórica (Delta Map)
En lugar de limitarse a mostrar fotografías estáticas de un solo año, el **Delta Map** calcula de forma dinámica y bajo demanda la variación neta de la métrica seleccionada entre dos años elegidos por el usuario (ej. 2015 frente a 2023). 

Utiliza una **escala cromática divergente simétrica** (`RdYlGn` - Rojo a Verde centrado en cero) que permite identificar de inmediato:
* **Zonas de Progreso Social (Verde):** Europa del Este (e.g., Rumanía, Bulgaria, Hungría) y partes de África Occidental muestran incrementos netos significativos de felicidad (hasta +1.5 puntos) en la última década, delatando rápidos procesos de convergencia económica y estabilización institucional.
* **Zonas de Regresión Social (Rojo):** Regiones sumidas en crisis severas, como Venezuela en América Latina, o Afganistán en Asia, se colorean intensamente de rojo oscuro, reflejando pérdidas dramáticas de bienestar de más de 2 puntos en sus índices subjetivos.

---

## 5. Análisis de Correlaciones y Distribuciones (Gráficas Avanzadas)
El análisis de patrones globales se sustenta en dos gráficas interactivas complementarias:

### 5.1 Diagrama de Dispersión Multidimensional (Correlaciones)
El gráfico relaciona dinámicamente dos variables a elección del usuario. Por defecto, al cruzar el PIB per cápita (Eje X) con el Puntaje de Felicidad (Eje Y), coloreando los puntos por Continente y dimensionando su tamaño por la Felicidad absoluta, se comprueba una **correlación logarítmica fuertemente positiva**. 

Sin embargo, a nivel académico destaca la manifestación de la *Paradoja de Easterlin*: a partir de una contribución del PIB superior a 1.6, la curva de felicidad se aplana exponencialmente, demostrando que los aumentos de riqueza material tienen rendimientos marginales decrecientes en la satisfacción vital humana.

### 5.2 Diagrama de Violín de Densidad Regional (Distribuciones)
Agregado para estudiar la dispersión a nivel continental, el **Violin Plot** es un gráfico estadístico avanzado que muestra la distribución de frecuencia completa de los datos junto con sus cuartiles internos. Este análisis revela hallazgos invisibles en un simple gráfico de barras promedio:
* **Europa** exhibe una distribución de violín esbelta, fuertemente sesgada hacia la parte superior y con una cola muy corta en el rango bajo, demostrando altos niveles de felicidad acompañados por una baja desigualdad social.
* **América Latina (Americas)** presenta un violín ancho en el rango medio-alto, reflejando una resiliencia cultural y social que mantiene índices de felicidad elevados a pesar de brechas económicas persistentes.
* **Oriente Medio y África** muestran perfiles ensanchados en el rango inferior con largas colas y patrones bimodales, reflejando profundas grietas socioeconómicas internas y una alta vulnerabilidad geopolítica.

---

## 6. Casos de Estudio Detallados y Perfiles (Gráfico de Radar)
El deep-dive por país permite un diagnóstico individual y comparativo exquisito a través de una innovadora visualización:

### 6.1 Gráfico de Radar de Bienestar (Spider Chart)
El gráfico de araña interactivo superpone los "perfiles de bienestar" del país principal y de un país de control en base a las 6 variables socioeconómicas. Al cerrar el loop poligonal con interpolación lineal, el gráfico permite identificar instantáneamente el "ADN social" de las naciones:
* **El Perfil de Excelencia Finlandés:** Finlandia demuestra un polígono excepcionalmente amplio y simétrico. Su dominancia global no se debe a tener la puntuación más alta en PIB, sino a su desempeño óptimo y robusto en *Apoyo Social* e *Instituciones de Confianza* (baja corrupción).
* **El Colapso Poligonal Venezolano:** La comparación histórica del polígono de radar de Venezuela revela una contracción masiva del área ocupada. Las dimensiones de *Gobernanza y Libertad de Elección* se encogen catastróficamente, ilustrando empíricamente cómo la erosión institucional destruye de forma directa la percepción de felicidad ciudadana sin importar otros factores.

---

## 7. Conclusiones del Informe y Recomendaciones Políticas
El análisis empírico longitudinal de la Felicidad Mundial de 2015 a 2023 fundamenta las siguientes conclusiones científicas:
1. **La Paradoja del Crecimiento:** Los ingresos (PIB) son fundamentales en etapas de desarrollo bajo para salir de la pobreza extrema, pero son ineficaces para aumentar la felicidad de forma indefinida en sociedades desarrolladas si no van acompañados de salud y relaciones sociales sólidas.
2. **La Corrupción es un Freno Sistémico:** Los datos de percepción de corrupción (`trust`) revelan una correlación inversa insalvable con la felicidad. Un gobierno con alta percepción de corrupción actúa como un lastre estructural, destruyendo la cohesión y la felicidad independientemente del PIB del país.
3. **Rediseño de Políticas Públicas:** Se recomienda formalmente a las administraciones públicas trascender la contabilidad monetaria tradicional y adoptar marcos de evaluación basados en el bienestar multidimensional para guiar de forma humana la inversión pública en salud mental, infraestructura social y libertades civiles.

---

## 8. Detalle de Librerías y Entorno de Ejecución
Para permitir una ejecución fluida en local y en la nube (Streamlit Cloud), la aplicación se apoya en un stack puramente científico documentado en `requirements.txt`:
* **Streamlit (>= 1.35.0):** Framework core de la aplicación web reactiva. Utiliza técnicas avanzadas como `@st.cache_data` para el almacenamiento en caché de la lectura y limpieza de datos, y `st.navigation` / `st.Page` para una arquitectura multipágina limpia y escalable.
* **Pandas (>= 1.5.0):** Gestión y transformación de estructuras de datos matriciales (fusión de datos, agrupaciones y cálculos de deltas temporales).
* **Plotly (>= 5.15.0):** Motor gráfico de alta interactividad, utilizado para renderizar las proyecciones en 3D del mapa geoespacial, el scatter plot dimensional, los diagramas de violín y los polígonos polar Scatterpolar (radar charts).

---

## 9. Referencias
1. Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J. E., Aknin, L. B., & Wang, S. (2023). *World Happiness Report 2023*. Sustainable Development Solutions Network.
2. Luke's Repository. *ISO 3166 Countries with Regional Codes Database*. [GitHub Raw Source](https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv).
3. Plotly Graphing Libraries. *Scatterpolar and Choropleth Map Projections in Python*.
4. Streamlit Documentation. *Multi-page Apps and Performance Caching API Reference*.
