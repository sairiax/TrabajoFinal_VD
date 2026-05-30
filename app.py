import streamlit as st
import pathlib

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Felicidad Mundial",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definir la ruta base
dir_path = pathlib.Path(__file__).parent

# Definir las páginas estructuradas como diccionario para habilitar cabeceras de sección nativas
pages = {
    "Menú de Navegación": [
        st.Page(
            dir_path / "pages" / "global_analysis.py",
            title="Análisis Global",
            icon="🌍"
        ),
        st.Page(
            dir_path / "pages" / "country_deepdive.py",
            title="Análisis por País",
            icon="📊"
        )
    ]
}

# Crear y ejecutar la navegación nativa (coloca la sección "Menú de Navegación" arriba)
pg = st.navigation(pages)
pg.run()
