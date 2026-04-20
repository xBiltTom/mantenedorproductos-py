"""
pages/3_Reportes.py - Generación de reportes PDF
"""
import streamlit as st
import requests
import sys
import os
from datetime import datetime

# Importar el generador de PDFs desde el directorio padre del frontend
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pdf_reports import generar_reporte_inventario, generar_reporte_analisis

API_URL = st.session_state.get("API_URL", "http://localhost:8000")


# ─────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────

def fetch_productos(categoria=None):
    params = {"limit": 5000}
    if categoria:
        params["categoria"] = categoria
    try:
        r = requests.get(f"{API_URL}/productos", params=params, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def fetch_stats():
    try:
        r = requests.get(f"{API_URL}/stats/dashboard", timeout=8)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def fetch_categorias_stats():
    try:
        r = requests.get(f"{API_URL}/stats/categorias", timeout=8)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def fetch_bajo_stock():
    try:
        r = requests.get(f"{API_URL}/stats/bajo-stock", timeout=8)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def fetch_categorias():
    try:
        r = requests.get(f"{API_URL}/productos/categorias", timeout=5)
        r.raise_for_status()
        return r.json()
    except:
        return []


# ─────────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────────

st.markdown("""
<div class="page-header">
    <h1 style="margin:0; text-transform:uppercase; background: linear-gradient(90deg, #FFF, #8E939C); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📄 Reportes</h1>
    <p style="margin:0.3rem 0 0; color:#8E939C; font-size:0.95rem;">
        Generación de informes profesionales en formato PDF
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# TARJETAS DE REPORTES
# ─────────────────────────────────────────────────

st.markdown("### Reportes Disponibles")

rep1_col, rep2_col = st.columns(2)

# ══════════════════════════════════════════════════
# REPORTE 1: INVENTARIO ACTUAL
# ══════════════════════════════════════════════════

with rep1_col:
    st.markdown("""
    <div class="card" style="border-top: 2px solid var(--accent-cyber); min-height: 160px; background:var(--surface-glass);">
        <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem;">
            <span style="font-size:1.8rem; filter:drop-shadow(0 0 10px rgba(0,229,255,0.4));">📦</span>
            <div>
                <h3 style="margin:0; color:#FFF; font-size:1rem; text-transform:uppercase; letter-spacing:1px;">Reporte Operacional</h3>
                <p style="margin:0; color:#8E939C; font-size:0.8rem;">Listado del Inventario Actual</p>
            </div>
        </div>
        <p style="color:#A0AEC0; font-size:0.85rem; margin-bottom:0.5rem; line-height:1.5;">
            Tabla detallada de todos los productos con SKU, nombre, stock, precios y valor total.
            Puede filtrarse por categoría antes de generar.
        </p>
        <div style="font-size:0.78rem; color:#8E939C; background:rgba(0,0,0,0.3); padding:0.4rem; border-radius:4px; margin-top:0.5rem;">
            <strong style="color:var(--accent-cyber);">INCLUYE:</strong> tabla de productos · resumen estadístico · KPIs
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filtro por categoría
    categorias = ["Todas las categorías"] + fetch_categorias()
    cat_reporte1 = st.selectbox(
        "Filtrar por categoría",
        categorias,
        key="cat_reporte1",
        help="Selecciona una categoría para el reporte, o deja 'Todas' para incluir todo"
    )

    if st.button("📥 Generar Reporte de Inventario", use_container_width=True, key="btn_rep1"):
        with st.spinner("Generando PDF..."):
            cat_filtro = None if cat_reporte1 == "Todas las categorías" else cat_reporte1
            productos, err = fetch_productos(categoria=cat_filtro)

            if err:
                st.error(f"❌ Error al obtener datos: {err}")
            elif not productos:
                st.warning("No hay productos para generar el reporte.")
            else:
                try:
                    pdf_bytes = generar_reporte_inventario(
                        productos=productos,
                        categoria_filtro=cat_filtro
                    )
                    fecha_str = datetime.now().strftime("%Y%m%d_%H%M")
                    cat_str   = f"_{cat_filtro.replace(' ', '_')}" if cat_filtro else ""
                    filename  = f"inventario_actual{cat_str}_{fecha_str}.pdf"

                    st.download_button(
                        label="⬇ Descargar PDF — Inventario Actual",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_rep1"
                    )
                    st.success(f"✅ PDF generado exitosamente con {len(productos)} productos.")
                except Exception as e:
                    st.error(f"❌ Error al generar PDF: {str(e)}")


# ══════════════════════════════════════════════════
# REPORTE 2: ANÁLISIS ESTRATÉGICO
# ══════════════════════════════════════════════════

with rep2_col:
    st.markdown("""
    <div class="card" style="border-top: 2px solid var(--accent-danger); min-height: 160px; background:var(--surface-glass);">
        <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem;">
            <span style="font-size:1.8rem; filter:drop-shadow(0 0 10px rgba(255,46,99,0.4));">📊</span>
            <div>
                <h3 style="margin:0; color:#FFF; font-size:1rem; text-transform:uppercase; letter-spacing:1px;">Reporte de Gestión</h3>
                <p style="margin:0; color:#8E939C; font-size:0.8rem;">Análisis de Inventario y Bajo Stock</p>
            </div>
        </div>
        <p style="color:#A0AEC0; font-size:0.85rem; margin-bottom:0.5rem; line-height:1.5;">
            Informe estratégico con KPIs del tablero, distribución por categoría y
            lista completa de productos que requieren reorden urgente.
        </p>
        <div style="font-size:0.78rem; color:#8E939C; background:rgba(0,0,0,0.3); padding:0.4rem; border-radius:4px; margin-top:0.5rem;">
            <strong style="color:var(--accent-danger);">INCLUYE:</strong> KPIs · análisis por categoría · tabla de bajo stock
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

    if st.button("📥 Generar Análisis Estratégico", use_container_width=True, key="btn_rep2"):
        with st.spinner("Generando PDF con análisis completo..."):
            stats, err1       = fetch_stats()
            categorias_s, err2 = fetch_categorias_stats()
            bajo_stock, err3  = fetch_bajo_stock()

            errors = [e for e in [err1, err2, err3] if e]
            if errors:
                st.error(f"❌ Error al obtener datos: {'; '.join(errors)}")
            else:
                try:
                    pdf_bytes = generar_reporte_analisis(
                        stats=stats,
                        categorias=categorias_s,
                        bajo_stock=bajo_stock
                    )
                    fecha_str = datetime.now().strftime("%Y%m%d_%H%M")
                    filename  = f"analisis_inventario_{fecha_str}.pdf"

                    st.download_button(
                        label="⬇ Descargar PDF — Análisis Estratégico",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_rep2"
                    )
                    st.success(
                        f"✅ PDF generado. "
                        f"{bajo_stock and len(bajo_stock) or 0} productos con bajo stock incluidos."
                    )
                except Exception as e:
                    st.error(f"❌ Error al generar PDF: {str(e)}")

# ─────────────────────────────────────────────────
# INFO
# ─────────────────────────────────────────────────

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); border-radius:10px;
            padding:1.5rem; font-size:0.85rem; color:#A0AEC0;">
    <strong style="color:#FFF; font-family:'Syne',sans-serif; text-transform:uppercase; letter-spacing:1px; display:block; margin-bottom:0.5rem;">
        <span style="color:var(--accent-glow);">INFO</span> Acerca de los reportes
    </strong>
    Los PDFs se generan dinámicamente utilizando el motor <strong>ReportLab</strong>, diseñados con estética profesional de alto contraste.
    <ul style="margin-top:0.5rem; margin-bottom:0; padding-left:1.2rem;">
        <li><strong>Reporte Operacional:</strong> Orientación <em>horizontal (landscape)</em>.</li>
        <li><strong>Reporte de Gestión:</strong> Orientación <em>vertical (portrait)</em> formato A4 estándar.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
