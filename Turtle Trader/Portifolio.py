# Bibliotecas
import numpy as np
import pandas as pd
from pandas_datareader import data as wb
from datetime import datetime, timedelta
import yfinance as yf
yf.pdr_override()

# Definição das datas
end_date = datetime.now()
start_date = end_date - timedelta(days=365)  # Um período mais longo pode ser necessário para cálculos de longo prazo
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Lista de tickers
tickers = ['PETR4.SA', 'WEGE3.SA', 'BBDC4.SA', 'BBAS3.SA']

# Dicionário para armazenar os sinais
sinais = {}

# Busca de dados e cálculo dos sinais para cada ticker
for t in tickers:
    dados = wb.get_data_yahoo(t, start=start_date_str, end=end_date_str)
    
    # Cálculo dos Canais de Donchian
    dados['20 Day High'] = dados['Adj Close'].rolling(window=20).max()
    dados['10 Day Low'] = dados['Adj Close'].rolling(window=10).min()
    
    # Identificação de pontos de entrada e saída para o último dia
    ultimo_dia = dados.iloc[-1]
    sinal_compra = ultimo_dia['Adj Close'] > dados['20 Day High'].iloc[-2]  # Compara com o dia anterior
    sinal_venda = ultimo_dia['Adj Close'] < dados['10 Day Low'].iloc[-2]  # Compara com o dia anterior
    
    # Atribuição do sinal
    if sinal_compra:
        sinais[t] = 'Compra'
    elif sinal_venda:
        sinais[t] = 'Venda'
    else:
        sinais[t] = 'Aguardar'

# Exibir os sinais para cada ação
for ticker, sinal in sinais.items():
    print(f"{ticker}: {sinal}")
