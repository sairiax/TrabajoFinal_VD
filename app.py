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

# Definir las páginas utilizando el sistema recomendado en el temario (st.Page)
pages = [
    st.Page(
        dir_path / "pages" / "global_analysis.py",
        title="Análisis Global",
        icon=":material/public:"
    ),
    st.Page(
        dir_path / "pages" / "country_deepdive.py",
        title="Análisis por País",
        icon=":material/analytics:"
    )
]

# Configurar la barra lateral y navegación
st.sidebar.markdown(
    "<h2 style='text-align: center; color: #6366f1; font-weight: 700;'>🌍 Menú de Navegación</h2>",
    unsafe_allow_html=True
)
st.sidebar.divider()

# Crear y ejecutar la navegación
pg = st.navigation(pages)
pg.run()
