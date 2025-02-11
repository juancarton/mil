#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Definir la contraseña directamente en el código
PASSWORD = "Ileana"  # 🔐 Cambia esto por la contraseña que desees

# Inicializar sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ----------------------- LOGIN -----------------------
if not st.session_state.authenticated:
    st.title("🔐 Acceso a Reporte de Ventas")
    password_input = st.text_input("Ingresa la contraseña:", type="password")

    if st.button("Ingresar"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()  # Recargar la página para ocultar el campo de contraseña
        else:
            st.error("❌ Contraseña incorrecta")

# ---------------------- INTERFAZ PRINCIPAL ----------------------
if st.session_state.authenticated:
    st.title("📊 Análisis de Ventas - Tiendas")

    # Botón para cerrar sesión
    if st.button("Cerrar sesión 🔒"):
        st.session_state.authenticated = False
        st.experimental_rerun()

    # Cargar archivo Excel
    file_path = "ventas_tiendas_actualizado.xlsx"  # Asegúrate de que el archivo esté en la misma carpeta
    df = pd.read_excel(file_path)

    # Convertir la columna de fecha a formato datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"])

    # ----------------------- FILTRO POR FECHA -----------------------
    st.subheader("📅 Comparación de Ventas por Fecha")
    fecha_seleccionada = st.date_input("Selecciona una fecha", df["Fecha"].min())

    df_fecha = df[df["Fecha"] == pd.to_datetime(fecha_seleccionada)]

    if not df_fecha.empty:
        ventas_tienda = df_fecha.groupby("Tienda")["Venta ($)"].sum().reset_index()
        st.dataframe(ventas_tienda)

        # Gráfico
        fig, ax = plt.subplots()
        ax.bar(ventas_tienda["Tienda"], ventas_tienda["Venta ($)"], color=["blue", "green"])
        ax.set_ylabel("Venta Total ($)")
        ax.set_title(f"Ventas por Tienda - {fecha_seleccionada.strftime('%d-%m-%Y')}")
        st.pyplot(fig)
    else:
        st.warning("⚠ No hay datos de ventas para esta fecha.")

    # -------------------- FILTRO POR DÍA DE LA SEMANA --------------------
    st.subheader("📆 Comparación de Ventas por Día de la Semana")
    mes_seleccionado = st.selectbox("Selecciona un mes", df["Fecha"].dt.strftime("%B").unique())
    dia_seleccionado = st.selectbox("Selecciona un día de la semana", df["Día de la Semana"].unique())

    df_dia = df[(df["Fecha"].dt.strftime("%B") == mes_seleccionado) & (df["Día de la Semana"] == dia_seleccionado)]
    
    if not df_dia.empty:
        ventas_dia = df_dia.groupby("Tienda")["Venta ($)"].sum().reset_index()
        st.dataframe(ventas_dia)

        # Gráfico
        fig, ax = plt.subplots()
        ax.bar(ventas_dia["Tienda"], ventas_dia["Venta ($)"], color=["orange", "purple"])
        ax.set_ylabel("Venta Total ($)")
        ax.set_title(f"Ventas por Tienda - {dia_seleccionado} de {mes_seleccionado}")
        st.pyplot(fig)
    else:
        st.warning("⚠ No hay datos para este día en el mes seleccionado.")

    # -------------------- FILTRO POR CATEGORÍA --------------------
    st.subheader("🏷️ Ventas por Categoría")
    categoria_seleccionada = st.selectbox("Selecciona una categoría", df["Categoría"].unique())

    df_categoria = df[df["Categoría"] == categoria_seleccionada]

    if not df_categoria.empty:
        ventas_categoria = df_categoria.groupby(["Tienda", "Fecha"])["Venta ($)"].sum().reset_index()
        st.dataframe(ventas_categoria)

        # Gráfico
        fig, ax = plt.subplots()
        for tienda in ventas_categoria["Tienda"].unique():
            data_tienda = ventas_categoria[ventas_categoria["Tienda"] == tienda]
            ax.plot(data_tienda["Fecha"], data_tienda["Venta ($)"], label=tienda)
        
        ax.set_ylabel("Venta Total ($)")
        ax.set_title(f"Ventas en Categoría: {categoria_seleccionada}")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("⚠ No hay datos para esta categoría.")

    # -------------------- FILTRO POR PRODUCTO --------------------
    st.subheader("🔍 Ventas por Producto")
    producto_seleccionado = st.selectbox("Selecciona un producto", df["Producto"].unique())

    df_producto = df[df["Producto"] == producto_seleccionado]

    if not df_producto.empty:
        ventas_producto = df_producto.groupby(["Tienda", "Fecha"])["Venta ($)"].sum().reset_index()
        st.dataframe(ventas_producto)

        # Gráfico
        fig, ax = plt.subplots()
        for tienda in ventas_producto["Tienda"].unique():
            data_tienda = ventas_producto[ventas_producto["Tienda"] == tienda]
            ax.plot(data_tienda["Fecha"], data_tienda["Venta ($)"], label=tienda)
        
        ax.set_ylabel("Venta Total ($)")
        ax.set_title(f"Ventas del Producto: {producto_seleccionado}")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("⚠ No hay datos para este producto.")

