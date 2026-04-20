"""
pages/1_Dashboard.py - Panel principal con KPIs y visualizaciones
"""
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

# Importar configuración global
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ui_utils import render_global_ui

# Aplicar UI global (reemplaza Sidebar default y CSS)
render_global_ui(page_title="Dashboard - Sistema de Gestión")

API_URL = st.session_state.get("API_URL", "http://localhost:8000")

# ─────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────

@st.cache_data(ttl=30)
def fetch_dashboard_stats():
    try:
        r = requests.get(f"{API_URL}/stats/dashboard", timeout=8)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=30)
def fetch_categorias_stats():
    try:
        r = requests.get(f"{API_URL}/stats/categorias", timeout=8)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=30)
def fetch_bajo_stock():
    try:
        r = requests.get(f"{API_URL}/stats/bajo-stock", timeout=8)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

PALETA = [
    "#CAFA04", "#00E5FF", "#FF2E63", "#7D5FFF",
    "#00F5D4", "#FEE440", "#F15BB5", "#9B5DE5",
    "#38B000", "#FF9900"
]

# ─────────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────────

st.markdown("""
<div class="page-header">
    <h1 style="margin:0; text-transform:uppercase; background: linear-gradient(90deg, #FFF, #8E939C); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📊 Dashboard Analítico</h1>
    <p style="margin:0.3rem 0 0; color:#8E939C; font-size:0.95rem;">
        Indicadores clave y visualizaciones en tiempo real
    </p>
</div>
""", unsafe_allow_html=True)

if st.button("🔄 Actualizar datos"):
    st.cache_data.clear()
    st.rerun()

# ─────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────

stats, err_stats = fetch_dashboard_stats()

if err_stats:
    st.error(f"⚠ No se pudo conectar al backend: {err_stats}")
    st.info("Asegúrate de que FastAPI está corriendo en " + API_URL)
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "📦 Productos",
        stats.get("total_productos", 0),
        help="Total de productos únicos en el sistema"
    )
with col2:
    valor = stats.get("valor_total_inventario", 0)
    st.metric(
        "💰 Valor Inventario",
        f"S/ {valor:,.0f}",
        help="Suma de stock_actual × precio_compra"
    )
with col3:
    bajo = stats.get("productos_bajo_stock", 0)
    delta_color = "inverse" if bajo > 0 else "normal"
    st.metric(
        "⚠ Bajo Stock",
        bajo,
        delta=f"Requieren reorden" if bajo > 0 else "Todo OK",
        delta_color=delta_color,
        help="Productos con stock_actual < stock_minimo"
    )
with col4:
    st.metric(
        "🏷 Categorías",
        stats.get("total_categorias", 0),
        help="Número de categorías activas"
    )
with col5:
    margen = stats.get("margen_promedio_pct", 0)
    st.metric(
        "📈 Margen Prom.",
        f"{margen:.1f}%",
        help="Margen promedio: (precio_venta - precio_compra) / precio_compra"
    )

if stats.get("producto_mas_valioso"):
    st.markdown(f"""
    <div style="background:rgba(202,250,4,0.05); border:1px solid rgba(202,250,4,0.2); border-radius:12px;
                padding:1rem; margin:1rem 0; font-size:1rem; color:#FFF; display:flex; gap:0.5rem; align-items:center;">
        <span style="font-size:1.5rem; text-shadow:0 0 10px rgba(202,250,4,0.5);">🏆</span> 
        <div>
            <strong style="color:var(--accent-glow); text-transform:uppercase; font-family:'Syne',sans-serif; letter-spacing:0.05em;">Producto Star:</strong> 
            {stats['producto_mas_valioso']}
            &nbsp;<span style="color:#8E939C;">|</span>&nbsp; 
            <span style="color:#00E5FF; font-weight:700;">S/ {float(stats.get('valor_producto_top', 0)):,.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────

cat_data, err_cat = fetch_categorias_stats()

if cat_data:
    df_cat = pd.DataFrame(cat_data)

    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        st.markdown("#### 📊 Top 10 Categorías por Cantidad de Productos")
        top10 = df_cat.nlargest(10, "total_productos").sort_values("total_productos")

        fig_bar = go.Figure(go.Bar(
            x=top10["total_productos"],
            y=top10["categoria"],
            orientation="h",
            marker=dict(
                color=top10["total_productos"],
                colorscale=[[0, "rgba(0,229,255,0.2)"], [1, "#00E5FF"]],
                showscale=False
            ),
            text=top10["total_productos"],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Productos: %{x}<extra></extra>"
        ))
        fig_bar.update_layout(
            height=350,
            margin=dict(l=10, r=30, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Outfit", size=12, color="#FFFFFF"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", gridwidth=1),
            yaxis=dict(gridcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_g2:
        st.markdown("#### 🥧 Distribución por Valor de Inventario")

        fig_pie = go.Figure(go.Pie(
            labels=df_cat["categoria"],
            values=df_cat["valor_inventario"],
            hole=0.45,
            marker=dict(colors=PALETA[:len(df_cat)], line=dict(color="#0a0b10", width=2)),
            textinfo="percent+label",
            textfont=dict(size=12, color="#FFF"),
            hovertemplate="<b>%{label}</b><br>S/ %{value:,.2f}<br>%{percent}<extra></extra>"
        ))
        fig_pie.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Outfit", size=12, color="#FFFFFF"),
            showlegend=False,
            annotations=[dict(
                text="Valor<br>Inv.",
                x=0.5, y=0.5,
                font=dict(family="Syne", size=14, color="#CAFA04", weight="bold"),
                showarrow=False
            )]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Gráfico de valor de inventario por categoría
    st.markdown("#### 💵 Valor de Inventario por Categoría")
    df_sorted = df_cat.sort_values("valor_inventario", ascending=False)
    fig_val = px.bar(
        df_sorted, x="categoria", y="valor_inventario",
        color="valor_inventario",
        color_continuous_scale=["rgba(202,250,4,0.1)", "#CAFA04"],
        labels={"categoria": "Categoría", "valor_inventario": "Valor (S/)"},
        text_auto=".2s"
    )
    fig_val.update_traces(textfont_size=11, textfont_color="#FFF", textangle=0, textposition="outside")
    fig_val.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        font=dict(family="Outfit", color="#FFF"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(title=None)
    )
    st.plotly_chart(fig_val, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# TABLA DE BAJO STOCK
# ─────────────────────────────────────────────────

st.markdown("#### 🚨 Productos que Necesitan Reorden")

bajo_stock_data, err_bs = fetch_bajo_stock()

if err_bs:
    st.error(f"Error al cargar datos de bajo stock: {err_bs}")
elif not bajo_stock_data:
    st.markdown("""
    <div class="alert-success">
        ✅ <strong>¡Excelente!</strong> Todos los productos tienen niveles de stock adecuados.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-danger">
        ⚠ Se encontraron <strong>{len(bajo_stock_data)}</strong> productos
        con stock por debajo del mínimo establecido.
    </div>
    """, unsafe_allow_html=True)

    df_bs = pd.DataFrame(bajo_stock_data)
    df_bs = df_bs.rename(columns={
        "sku": "SKU",
        "nombre": "Producto",
        "categoria": "Categoría",
        "stock_actual": "Stock Actual",
        "stock_minimo": "Stock Mínimo",
        "deficit": "Déficit",
        "proveedor": "Proveedor"
    })
    df_bs = df_bs.drop(columns=["id"], errors="ignore")
    df_bs = df_bs.sort_values("Déficit", ascending=False)

    st.dataframe(
        df_bs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Déficit": st.column_config.NumberColumn(
                "Déficit", format="%d ⚠",
                help="Unidades que faltan para llegar al stock mínimo"
            ),
            "Stock Actual": st.column_config.NumberColumn("Stock Actual", format="%d"),
            "Stock Mínimo": st.column_config.NumberColumn("Stock Mínimo", format="%d"),
        }
    )
