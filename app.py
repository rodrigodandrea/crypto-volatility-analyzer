import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Título de la Aplicación
st.title('🚀 Crypto Correlation Dashboard')
st.markdown('Analizador de volatilidad para Liquidity Providers (LP)')

# Sidebar para que el usuario elija los activos
st.sidebar.header('Configuración')
crypto_1 = st.sidebar.text_input('Cripto 1', 'BTC-USD')
crypto_2 = st.sidebar.text_input('Cripto 2', 'ETH-USD')
days = st.sidebar.slider('Días de análisis', 30, 365, 90)

# Botón para ejecutar el análisis
if st.button('Correr Análisis'):
    assets = [crypto_1, crypto_2]
    data = yf.download(assets, period=f'{days}d')['Close']
    
    returns = data.pct_change().dropna()
    
    # Mostrar métricas clave
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"Volatilidad {crypto_1}", f"{round(returns[crypto_1].std()*(252**0.5)*100, 2)}%")
    with col2:
        st.metric(f"Volatilidad {crypto_2}", f"{round(returns[crypto_2].std()*(252**0.5)*100, 2)}%")

    # Gráfico de Correlación
    st.subheader('Gráfico de Dispersión y Regresión')
    fig, ax = plt.subplots()
    sns.regplot(x=returns[crypto_1], y=returns[crypto_2], ax=ax)
    st.pyplot(fig)
