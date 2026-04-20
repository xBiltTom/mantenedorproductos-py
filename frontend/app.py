"""
app.py - Aplicación Streamlit: Sistema de Gestión de Productos
Punto de entrada principal con configuración y navegación.
"""
import streamlit as st

# ============================================================
# CONFIGURACIÓN DE PÁGINA (debe ser lo primero)
# ============================================================
st.set_page_config(
    page_title="Gestión de Productos",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "**Sistema de Gestión de Productos** v1.0\nDesarrollado con FastAPI + Streamlit"
    }
)

# ============================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================
st.markdown("""
<style>
/* Importando fuentes modernas y elegantes */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Syne:wght@500;700;800&display=swap');

/* Variables Core - Dark Neon Aesthetic */
:root {
    --bg-base: #050507;
    --surface-dark: #0a0b10;
    --surface-glass: rgba(255, 255, 255, 0.02);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --text-primary: #FFFFFF;
    --text-muted: #8E939C;
    --accent-glow: #CAFA04; /* Lime Neon */
    --accent-cyber: #00E5FF;
    --accent-danger: #FF2E63;
}

/* Modificando cuerpo completo (Streamlit wrapper) */
.stApp {
    background-color: var(--bg-base);
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(202, 250, 4, 0.03), transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(0, 229, 255, 0.03), transparent 40%);
}

/* Tipografía Global */
html, body, [class*="css"], p, span, div {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: -0.02em;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--surface-dark) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text-muted) !important;
}
section[data-testid="stSidebar"] .stRadio > label {
    font-size: 0.85rem;
}

/* Métricas KPIs */
[data-testid="stMetric"] {
    background: var(--surface-glass);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.5rem !important;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(202, 250, 4, 0.3);
    box-shadow: 0 10px 40px rgba(202, 250, 4, 0.05);
}
[data-testid="stMetricLabel"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}

/* Tablas DataFrame */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border-subtle);
}
[data-testid="stDataFrame"] > div {
    background-color: #0a0b10 !important;
}

/* Botones Primary */
.stButton > button {
    background: transparent !important;
    color: var(--accent-glow) !important;
    border: 1px solid var(--accent-glow) !important;
    border-radius: 50px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 0.5rem 1.5rem;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 10px rgba(202, 250, 4, 0.0);
}
.stButton > button:hover {
    background: var(--accent-glow) !important;
    color: #000 !important;
    box-shadow: 0 0 20px rgba(202, 250, 4, 0.4);
    transform: scale(1.02);
}

/* Botones Danger */
.btn-danger > button {
    color: var(--accent-danger) !important;
    border-color: var(--accent-danger) !important;
}
.btn-danger > button:hover {
    background: var(--accent-danger) !important;
    color: #FFF !important;
    box-shadow: 0 0 20px rgba(255, 46, 99, 0.4) !important;
}

/* Formularios - Inputs */
.stTextInput>div>div>input,
.stSelectbox>div>div,
.stNumberInput>div>div>input,
.stTextArea>div>div>textarea {
    background-color: rgba(0,0,0,0.5) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    transition: all 0.2s ease;
}
.stTextInput>div>div>input:focus,
.stSelectbox>div>div:focus-within,
.stNumberInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color: var(--accent-cyber) !important;
    box-shadow: 0 0 0 1px var(--accent-cyber) !important;
}

/* Alertas */
.alert-warning {
    background: rgba(255, 166, 0, 0.05);
    border-left: 2px solid #FFA600;
    padding: 1rem 1.25rem;
    border-radius: 4px;
    margin: 0.5rem 0;
    color: #FFF;
    border-right: 1px solid rgba(255, 166, 0, 0.1);
    backdrop-filter: blur(5px);
}
.alert-danger {
    background: rgba(255, 46, 99, 0.05);
    border-left: 2px solid var(--accent-danger);
    padding: 1rem 1.25rem;
    border-radius: 4px;
    margin: 0.5rem 0;
    color: #FFF;
    border-right: 1px solid rgba(255, 46, 99, 0.1);
    backdrop-filter: blur(5px);
}
.alert-success {
    background: rgba(0, 230, 118, 0.05);
    border-left: 2px solid #00E676;
    padding: 1rem 1.25rem;
    border-radius: 4px;
    margin: 0.5rem 0;
    color: #FFF;
    border-right: 1px solid rgba(0, 230, 118, 0.1);
    backdrop-filter: blur(5px);
}

/* Cards Generales */
.card {
    background: var(--surface-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.card:hover {
    transform: translateY(-2px);
    border-color: rgba(255, 255, 255, 0.15);
}

/* Título de página */
.page-header {
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 0.25em 0.8em;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-danger  { background: rgba(255,46,99,0.1); color: #FF2E63; border: 1px solid rgba(255,46,99,0.2); }
.badge-success { background: rgba(0,230,118,0.1); color: #00E676; border: 1px solid rgba(0,230,118,0.2); }
.badge-warning { background: rgba(255,166,0,0.1); color: #FFA600; border: 1px solid rgba(255,166,0,0.2); }

/* Ocultar Streamlit branding */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    border-bottom: 1px solid var(--border-subtle);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important;
    padding: 1rem 1.5rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    font-size: 0.85rem;
    color: var(--text-muted);
}
.stTabs [aria-selected="true"] {
    background-color: transparent !important;
    color: var(--accent-glow) !important;
    border-bottom: 2px solid var(--accent-glow) !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid var(--border-subtle);
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# PÁGINA PRINCIPAL DE BIENVENIDA
# ============================================================

# Logo y título en sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem;">
        <div style="font-size:3rem; filter: drop-shadow(0 0 10px rgba(202,250,4,0.3));">📦</div>
        <div style="font-family:'Syne', sans-serif; font-size:1.25rem; font-weight:800; color:#FFF; margin-top:0.5rem; text-transform:uppercase; letter-spacing:1px;">
            Sist. Gestión
        </div>
        <div style="font-size:0.75rem; color:#8E939C; margin-top:0.2rem; letter-spacing:0.5px;">
            INVENTARIO INTELIGENTE
        </div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.08); margin: 0.5rem 0 1rem;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 0.5rem 0;">
        <div style="font-family:'Outfit',sans-serif; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.2em;
                    color:#CAFA04; font-weight:600; margin-bottom:0.5rem;">
            NAVEGACIÓN
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("app.py",               label="🏠  Inicio",      )
    st.page_link("pages/1_Dashboard.py", label="📊  Dashboard",   )
    st.page_link("pages/2_Productos.py", label="📋  Productos",   )
    st.page_link("pages/3_Reportes.py",  label="📄  Reportes",    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:1rem 0;'>", unsafe_allow_html=True)

    # Configuración de API
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.2em;
                color:#CAFA04; font-weight:600; margin-bottom:0.5rem;">
        CONFIGURACIÓN
    </div>
    """, unsafe_allow_html=True)

    api_url = st.text_input(
        "URL del Backend",
        value="http://localhost:8000",
        key="api_url_global",
        help="URL donde está corriendo el servidor FastAPI"
    )
    if api_url:
        st.session_state["API_URL"] = api_url

    st.markdown("""
    <div style="margin-top:2rem; font-size:0.75rem; color:#5D636B; text-align:center; font-family:'Outfit',sans-serif;">
        v2.0 · CORE ENGINE
    </div>
    """, unsafe_allow_html=True)


# Contenido de inicio
st.markdown("""
<div class="page-header">
    <h1 style="margin:0; text-transform:uppercase; background: linear-gradient(90deg, #FFF, #8E939C); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🏠 CORE CENTRAL</h1>
    <p style="margin:0.5rem 0 0; color:#8E939C; font-size:1rem; letter-spacing:0.5px;">
        Plataforma inteligente de control de inventario y análisis de datos en tiempo real.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card" style="border-top: 2px solid var(--accent-cyber);">
        <div style="font-size:2.5rem; margin-bottom:1rem; display:inline-block; filter:drop-shadow(0 0 10px rgba(0,229,255,0.4));">📊</div>
        <h3 style="margin:0 0 0.5rem; font-size:1.1rem; color:#FFF;">Dashboard</h3>
        <p style="color:#8E939C; font-size:0.9rem; margin:0; line-height:1.5;">
            Visualiza KPIs en tiempo real, distribuciones avanzadas
            y alertas tempranas de bajo stock.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card" style="border-top: 2px solid var(--accent-glow);">
        <div style="font-size:2.5rem; margin-bottom:1rem; display:inline-block; filter:drop-shadow(0 0 10px rgba(202,250,4,0.4));">📋</div>
        <h3 style="margin:0 0 0.5rem; font-size:1.1rem; color:#FFF;">Operaciones</h3>
        <p style="color:#8E939C; font-size:0.9rem; margin:0; line-height:1.5;">
            CRUD optimizado: control preciso de ítems, precios 
            y proveedores con arquitectura escalable.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card" style="border-top: 2px solid var(--accent-danger);">
        <div style="font-size:2.5rem; margin-bottom:1rem; display:inline-block; filter:drop-shadow(0 0 10px rgba(255,46,99,0.4));">📄</div>
        <h3 style="margin:0 0 0.5rem; font-size:1.1rem; color:#FFF;">Generación</h3>
        <p style="color:#8E939C; font-size:0.9rem; margin:0; line-height:1.5;">
            Motor de exportación documental de alta precisión 
            para reportes estratégicos inmediatos.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:2rem; padding:1.5rem; background:rgba(0, 229, 255, 0.05);
            border-radius:12px; border: 1px solid rgba(0, 229, 255, 0.15); display:flex; align-items:center; gap:1rem;">
    <div style="font-size:2rem; animation: pulse 2s infinite;">🚀</div>
    <div>
        <strong style="color:var(--accent-cyber); text-transform:uppercase; letter-spacing:1px; display:block; margin-bottom:0.25rem;">Terminal lista:</strong>
        <span style="color:#8E939C; font-size:0.9rem;">
            Sistema en línea. Backend local detectado en <code>http://localhost:8000</code>. Proceda con la navegación desde la interfaz lateral.
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
