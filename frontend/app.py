"""
app.py - Aplicación Streamlit: Sistema de Gestión de Productos
Punto de entrada principal con configuración y navegación.
"""
import streamlit as st

# ============================================================
# CONFIGURACIÓN GLOBAL DE UI
# ============================================================
from ui_utils import render_global_ui
render_global_ui(page_title="Inicio - Sistema de Gestión")


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
