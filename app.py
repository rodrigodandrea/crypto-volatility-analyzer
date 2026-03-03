import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Título de la Aplicación
st.title('🚀 Crypto Correlation Dashboard')
st.markdown('Volatility analyzer designed for Liquidity Providers (LP)')

# Sidebar para que el usuario elija los activos
st.sidebar.header('Analysis Settings')
crypto_1 = st.sidebar.text_input('First Asset (Ticker)', 'BTC-USD')
crypto_2 = st.sidebar.text_input('Second Asset (Ticker)', 'ETH-USD')
days = st.sidebar.slider('Time Horizon (Days)', 30, 365, 90)

# Botón para ejecutar el análisis
if st.button('Run Market Analysis'):
    assets = [crypto_1, crypto_2]
    
   # Data Ingestion
    with st.spinner('Fetching market data...'):
        data = yf.download(assets, period=f'{days}d')['Close']
    
    if data.empty or len(data.columns) < 2:
        st.error("Error: Could not retrieve data for one or both tickers. Please check the symbols.")
    else:
        # Calculate Daily Returns
        returns = data.pct_change().dropna()
        
        # Key Metrics Layout
        st.subheader('Key Risk Metrics')
        col1, col2, col3 = st.columns(3)
        
        # Annualized Volatility Calculation
        vol1 = returns[crypto_1].std() * (252**0.5) * 100
        vol2 = returns[crypto_2].std() * (252**0.5) * 100
        correlation = returns[crypto_1].corr(returns[crypto_2])

        with col1:
            st.metric(f"{crypto_1} Volatility", f"{vol1:.2f}%")
        with col2:
            st.metric(f"{crypto_2} Volatility", f"{vol2:.2f}%")
        with col3:
            st.metric("Correlation", f"{correlation:.2f}")

        # Visualization
        st.divider()
        st.subheader('Returns Correlation & Regression Analysis')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.regplot(x=returns[crypto_1], y=returns[crypto_2], ax=ax, 
                    scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
        
        ax.set_title(f'Daily Returns: {crypto_1} vs {crypto_2}', fontsize=12)
        ax.set_xlabel(f'{crypto_1} Daily Returns')
        ax.set_ylabel(f'{crypto_2} Daily Returns')
        
        st.pyplot(fig)
        
        # Risk Insight (MBA/PhD Touch)
        st.info(f"**Insight:** A correlation of **{correlation:.2f}** suggests that these assets move "
                f"{'strongly' if abs(correlation) > 0.7 else 'moderately'} in the same direction. "
                f"For an LP, higher correlation usually implies lower risk of Impermanent Loss.")
