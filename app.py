import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Painel de Criptomoedas", layout="wide")

# Título
st.title("📊 Painel de Criptomoedas em Tempo Real")

# Sidebar para seleção de moeda e número de criptomoedas
st.sidebar.header("Configurações")
moeda = st.sidebar.selectbox("Moeda", ["usd", "eur", "brl"])
quantidade = st.sidebar.slider("Número de criptomoedas", min_value=5, max_value=50, value=10)

# Função para obter dados da API
@st.cache_data(ttl=300)
def obter_dados(moeda, quantidade):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": moeda,
        "order": "market_cap_desc",
        "per_page": quantidade,
        "page": 1,
        "sparkline": False
    }
    resposta = requests.get(url, params=params)
    if resposta.status_code == 200:
        dados = resposta.json()
        df = pd.DataFrame(dados)
        df = df[["name", "symbol", "current_price", "market_cap", "price_change_percentage_24h"]]
        df.columns = ["Nome", "Símbolo", f"Preço ({moeda.upper()})", "Capitalização de Mercado", "Variação 24h (%)"]
        return df
    else:
        st.error("Erro ao obter dados da API.")
        return pd.DataFrame()

# Obter dados
df = obter_dados(moeda, quantidade)

# Exibir dados em tabela
if not df.empty:
    st.subheader("📈 Dados das Criptomoedas")
    st.dataframe(df, use_container_width=True)

    # Gráfico de variação percentual
    st.subheader("📉 Variação Percentual nas Últimas 24h")
    fig = px.bar(df, x="Nome", y="Variação 24h (%)", color="Variação 24h (%)",
                 color_continuous_scale=["red", "green"], height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Última atualização
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
