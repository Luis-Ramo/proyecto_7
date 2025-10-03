import pandas as pd
import plotly.express as px
import streamlit as st

# Cargar dataset
car_df = pd.read_csv("vehicles_us.csv")

# Encabezado principal
st.title("Análisis de Datos de Vehículos")

# ------------- PREPROCESAMIENTO -------------
# Crear columna 'marca' desde la columna 'model'
car_df['marca'] = car_df['model'].str.split().str[0]

# Inicialmente car_df_filtered será igual a car_df
car_df_filtered = car_df.copy()

# ------------- 1. Tabla de datos -------------
if st.checkbox("Tabla de datos"):
    show_small = st.checkbox("Incluir tipos con menos de 1000 anuncios", value=True)

    if not show_small:
        counts = car_df_filtered['type'].value_counts()
        valid_types = counts[counts >= 1000].index
        car_df_filtered = car_df_filtered[car_df_filtered['type'].isin(valid_types)]

    st.dataframe(car_df_filtered)

# ------------- 2. Histograma del kilometraje -------------
if st.checkbox("Histograma del kilometraje"):
    st.write("Histograma del kilometraje de los vehículos")
    fig_hist = px.histogram(
        car_df_filtered,
        x="odometer",
        nbins=50,
        labels={"odometer": "Kilometraje (millas)"},
        title="Histograma del kilometraje"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ------------- 3. Gráfico de dispersión: Precio vs Kilometraje -------------
if st.checkbox("Gráfico de dispersión Precio vs Kilometraje"):
    st.write("Gráfico de dispersión de Precio vs Kilometraje por tipo de vehículo")
    fig_scatter = px.scatter(
        car_df_filtered,
        x="odometer",
        y="price",
        color="type",
        labels={"odometer": "Kilometraje (millas)", "price": "Precio (USD)", "type": "Tipo de vehículo"},
        title="Dispersión: Precio vs Kilometraje por tipo de vehículo"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ------------- 4. Tipos de vehículos por marca -------------
if st.checkbox("Tipos de vehículos por marca"):
    counts = car_df_filtered['marca'].value_counts()
    valid_marcas = counts[counts >= 50].index
    df_marcas = car_df_filtered[car_df_filtered['marca'].isin(valid_marcas)]

    fig_marcas = px.histogram(
        df_marcas,
        x="marca",
        color="type",
        barmode="stack",
        labels={"marca": "Marca del vehículo", "type": "Tipo de vehículo"},
        title="Tipos de vehículos por marca"
    )
    st.plotly_chart(fig_marcas, use_container_width=True)

# ------------- 5. Histograma: Condición vs Año del modelo -------------
if st.checkbox("Distribución de condición por año del modelo"):
    st.write("Histograma que muestra la distribución de la condición de los vehículos por año del modelo")
    df_condition = car_df_filtered.dropna(subset=['model_year', 'condition'])
    fig_condition = px.histogram(
        df_condition,
        x="model_year",
        color="condition",
        barmode="overlay",
        labels={"model_year": "Año del modelo", "condition": "Condición del vehículo"},
        title="Distribución de la condición de vehículos por año del modelo"
    )
    st.plotly_chart(fig_condition, use_container_width=True)

# ------------- 6. Comparar distribución de precios entre marcas -------------
if st.checkbox("Comparar distribución de precios entre marcas"):
    # Usar solo marcas con suficiente cantidad
    counts = car_df_filtered['marca'].value_counts()
    valid_marcas = counts[counts >= 50].index
    marcas = valid_marcas.tolist()

    if len(marcas) >= 2:
        marca1 = st.selectbox("Selecciona la marca 1", marcas, index=0)
        marca2 = st.selectbox("Selecciona la marca 2", marcas, index=1)
        normalize = st.checkbox("Normalizar histograma (%)", value=True)

        subset = car_df_filtered[car_df_filtered['marca'].isin([marca1, marca2])]

        fig_price = px.histogram(
            subset,
            x="price",
            color="marca",
            barmode="overlay",
            histnorm="percent" if normalize else None,
            labels={"price": "Precio (USD)", "marca": "Marca"},
            title=f"Distribución de precios: {marca1} vs {marca2}"
        )
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.warning("No hay suficientes marcas para comparar.")

