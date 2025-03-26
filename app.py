import streamlit as st
import pandas as pd
import plotly.express as px

# Autenticación
def autenticar():
    password = st.text_input("🔐 Ingresa la contraseña para acceder", type="password")
    if password == "Ileana":
        st.success("✅ Acceso concedido. Bienvenida Ileana.")
        return True
    elif password:
        st.error("❌ Contraseña incorrecta.")
        return False
    return False

# Cargar datos
@st.cache_data
def cargar_datos():
    ventas = pd.read_excel("ventas_tiendas_actualizado.xlsx")
    articulos = pd.read_excel("articulos.xlsx")
    return ventas, articulos

# Solo continúa si la contraseña es correcta
if autenticar():
    st.title("📊 Comparativa de Tiendas")
    st.markdown("Consulta y compara ventas, transacciones y artículos por tienda.")

    ventas_df, articulos_df = cargar_datos()

    # Limpieza básica
    ventas_df["CLUB"] = ventas_df["CLUB"].astype(str)
    articulos_df["CLUB"] = articulos_df["CLUB"].astype(str)

    # Selección de tiendas
    tiendas = ventas_df["CLUB"].unique()
    tienda1 = st.selectbox("Selecciona la primera tienda", tiendas)
    tienda2 = st.selectbox("Selecciona la segunda tienda", tiendas, index=1 if len(tiendas) > 1 else 0)

    # Filtros por categoría y artículo
    categorias = ventas_df["Categoria"].unique()
    categoria_sel = st.multiselect("Filtrar por categoría", categorias, default=categorias[:3])

    ventas_filtradas = ventas_df[
        (ventas_df["CLUB"].isin([tienda1, tienda2])) &
        (ventas_df["Categoria"].isin(categoria_sel))
    ]

    # Agrupar datos por tienda
    resumen = ventas_filtradas.groupby("CLUB")[["Venta MTD", "Venta YTD", "Trans YTD"]].sum().reset_index()

    st.subheader("📈 Comparativa de Ventas y Transacciones")
    st.dataframe(resumen, use_container_width=True)

    # Gráficas modernas con Plotly
    for columna in ["Venta MTD", "Venta YTD", "Trans YTD"]:
        fig = px.bar(resumen, x="CLUB", y=columna, title=f"Comparativa: {columna}", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    # Artículos relacionados
    st.subheader("🧾 Artículos por tienda y categoría")
    categoria_art = st.selectbox("Selecciona categoría para ver artículos", categorias)
    articulos_filtrados = articulos_df[
        (articulos_df["CATEGORIA"] == categoria_art) &
        (articulos_df["CLUB"].isin([tienda1, tienda2]))
    ]

    st.dataframe(articulos_filtrados, use_container_width=True)

    st.markdown("---")
    st.caption("Optimizado para móviles. Publicado en Streamlit Cloud.")
