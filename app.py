import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Comparador de Tiendas", layout="wide")

# Sesiones para autenticación
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso a la App")
    password = st.text_input("Ingrese la contraseña para acceder:", type="password")
    if password == "Ileana":
        st.session_state.autenticado = True
        st.success("Acceso concedido. ¡Bienvenido! Por favor recarga la página si no ves el contenido.")
        st.stop()
    elif password != "":
        st.error("Contraseña incorrecta. Inténtelo nuevamente.")
    st.stop()  # Se detiene aquí solo si aún no está autenticado

# Botón para cerrar sesión
if st.button("🔓 Cerrar sesión"):
    st.session_state.autenticado = False
    st.success("Sesión cerrada. Recarga la página para volver a ingresar.")
    st.stop()

# Cargar datos
ventas_df = pd.read_excel("ventas_tiendas_actualizado.xlsx", sheet_name="Hoja1")
articulos_df = pd.read_excel("articulos.xlsx", sheet_name="Hoja1")

st.title("📊 Comparativa de Ventas y Transacciones entre Tiendas")

# Tiendas disponibles
tiendas = ventas_df["CLUB"].unique()

# Filtros de usuario
col1, col2 = st.columns(2)
with col1:
    tienda1 = st.selectbox("Selecciona la primera tienda:", tiendas, index=0)
with col2:
    tienda2 = st.selectbox("Selecciona la segunda tienda:", tiendas, index=1)

# Categorías disponibles
categorias = ventas_df["Categoria"].unique()
cat_select = st.multiselect("Filtrar por categorías (opcional):", categorias, default=categorias)

# Filtrar por tienda y categoría en ventas
def filtrar_tienda(df, tienda, categorias):
    return df[(df["CLUB"] == tienda) & (df["Categoria"].isin(categorias))]

t1_df = filtrar_tienda(ventas_df, tienda1, cat_select)
t2_df = filtrar_tienda(ventas_df, tienda2, cat_select)

# Agrupar y resumir datos
def resumir(df):
    return df[["Venta MTD", "Venta YTD", "Trans YTD"]].sum()

resumen1 = resumir(t1_df)
resumen2 = resumir(t2_df)

# Panel de visualización
col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.subheader("Resumen Comparativo por Categoría")
    comparativa = pd.DataFrame({
        tienda1: resumen1,
        tienda2: resumen2,
        "Diferencia": resumen1 - resumen2
    })
    st.dataframe(comparativa.style.format("{:.2f}"), use_container_width=True)

    st.subheader("Gráfica Comparativa por Categoría")
    fig = go.Figure(data=[
        go.Bar(name=tienda1, x=comparativa.index, y=comparativa[tienda1]),
        go.Bar(name=tienda2, x=comparativa.index, y=comparativa[tienda2])
    ])
    fig.update_layout(barmode='group', title="Comparación entre Tiendas", xaxis_title="Métricas", yaxis_title="Valores")
    st.plotly_chart(fig, use_container_width=True)

with col_der:
    st.subheader("🔍 Comparativa de Artículos")
    art1_df = articulos_df[(articulos_df["CLUB"] == tienda1) & (articulos_df["CATEGORIA"].isin(cat_select))]
    art2_df = articulos_df[(articulos_df["CLUB"] == tienda2) & (articulos_df["CATEGORIA"].isin(cat_select))]

    merged_art = pd.merge(art1_df, art2_df, on="NUM ARTICULO", suffixes=(f" ({tienda1})", f" ({tienda2})"))

    if not merged_art.empty:
        st.write("Artículos comunes entre ambas tiendas dentro de las categorías seleccionadas:")
        st.dataframe(merged_art[["NUM ARTICULO", f"DESCRIPCION ({tienda1})", f"PVENTA ({tienda1})", f"PVENTA ({tienda2})"]], use_container_width=True)

        fig_art = go.Figure()
        fig_art.add_trace(go.Bar(x=merged_art[f"DESCRIPCION ({tienda1})"], y=merged_art[f"PVENTA ({tienda1})"], name=tienda1))
        fig_art.add_trace(go.Bar(x=merged_art[f"DESCRIPCION ({tienda1})"], y=merged_art[f"PVENTA ({tienda2})"], name=tienda2))
        fig_art.update_layout(title="Comparativa de Precios de Artículos", xaxis_title="Artículo", yaxis_title="Precio de Venta", barmode="group")
        st.plotly_chart(fig_art, use_container_width=True)
    else:
        st.info("No hay artículos comunes entre las tiendas seleccionadas para las categorías elegidas.")

st.caption("App desarrollada con Streamlit y Plotly. Optimizada para dispositivos móviles.")