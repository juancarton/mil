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
        st.success("Acceso concedido. ¡Bienvenido!")
    elif password != "":
        st.error("Contraseña incorrecta. Inténtelo nuevamente.")
    st.stop()

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

# Filtrar por tienda y categoría
def filtrar_tienda(df, tienda, categorias):
    return df[(df["CLUB"] == tienda) & (df["Categoria"].isin(categorias))]

t1_df = filtrar_tienda(ventas_df, tienda1, cat_select)
t2_df = filtrar_tienda(ventas_df, tienda2, cat_select)

# Agrupar y sumar datos relevantes
def resumir(df):
    return df[["Venta MTD", "Venta YTD", "Trans YTD"]].sum()

resumen1 = resumir(t1_df)
resumen2 = resumir(t2_df)

# Mostrar tablas resumen
st.subheader("Resumen Comparativo")
comparativa = pd.DataFrame({
    tienda1: resumen1,
    tienda2: resumen2,
    "Diferencia": resumen1 - resumen2
})
st.dataframe(comparativa.style.format("{:.2f}"), use_container_width=True)

# Gráfica comparativa
st.subheader("Gráfica Comparativa")
fig = go.Figure(data=[
    go.Bar(name=tienda1, x=comparativa.index, y=comparativa[tienda1]),
    go.Bar(name=tienda2, x=comparativa.index, y=comparativa[tienda2])
])
fig.update_layout(barmode='group', title="Comparación entre Tiendas", xaxis_title="Métricas", yaxis_title="Valores")
st.plotly_chart(fig, use_container_width=True)

st.caption("App desarrollada con Streamlit y Plotly. Optimizada para dispositivos móviles.")
