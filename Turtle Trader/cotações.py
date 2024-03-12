#Bibliotecas
import numpy as np
from pandas_datareader import data as wb
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime, timedelta
import yfinance as yf
yf.pdr_override()

# Definição das datas

end_date = datetime.now()
start_date = end_date - timedelta(days = 90)
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Busca de dados
cotacao_bovespa = wb.get_data_yahoo('PETR4.SA', start = start_date_str, end = end_date_str)

# Cálculo dos Canais de Donchian
cotacao_bovespa['20 Day High'] = cotacao_bovespa['Adj Close'].rolling(window = 20).max()
cotacao_bovespa['10 Day Low'] = cotacao_bovespa['Adj Close'].rolling(window = 10).min()

# Identificação de pontos de entrada e saída
cotacao_bovespa['Long Entry'] = (cotacao_bovespa['Adj Close'] > cotacao_bovespa['20 Day High'].shift(1)).fillna(False)
cotacao_bovespa['Long Exit'] = (cotacao_bovespa['Adj Close'] < cotacao_bovespa['10 Day Low'].shift(1)).fillna(False)

# Assumindo que entramos no trade no dia seguinte ao sinal de entrada e saímos no dia seguinte ao sinal de saída
cotacao_bovespa['Positions Long'] = np.nan
cotacao_bovespa.loc[cotacao_bovespa['Long Entry'],'Positions Long'] = 1
cotacao_bovespa.loc[cotacao_bovespa['Long Exit'],'Positions Long'] = 0
cotacao_bovespa['Positions Long'] = cotacao_bovespa['Positions Long'].fillna(method='ffill')

# Cálculo do ATR para gestão de risco
cotacao_bovespa['True Range'] = np.maximum(cotacao_bovespa['High'] - cotacao_bovespa['Low'], 
                                           np.maximum(abs(cotacao_bovespa['High'] - cotacao_bovespa['Adj Close'].shift(1)), 
                                                      abs(cotacao_bovespa['Low'] - cotacao_bovespa['Adj Close'].shift(1))))
cotacao_bovespa['ATR'] = cotacao_bovespa['True Range'].rolling(window=14).mean()

# Implementação da lógica de decisão para o dia atual
hoje = cotacao_bovespa.iloc[-1]  # Pega a última linha do DataFrame

# Ajusta para comparar com os valores do dia anterior
sinal_compra = hoje['Adj Close'] > cotacao_bovespa['20 Day High'].iloc[-2]  # Compara com o dia anterior
sinal_venda = hoje['Adj Close'] < cotacao_bovespa['10 Day Low'].iloc[-2]  # Compara com o dia anterior

if sinal_compra:
    acao = "Compra"
elif sinal_venda:
    acao = "Venda"
else:
    acao = "Aguardar"

print(f"Ação recomendada para hoje ({hoje.name.date()}): {acao}")

# Salvando as colunas de Donchian em variáveis separadas
donchian_20_day_high = cotacao_bovespa['20 Day High']
donchian_10_day_low = cotacao_bovespa['10 Day Low']

# Ajuste para o DataFrame apenas com as colunas necessárias para o gráfico de velas
cotacao_bovespa_velas = cotacao_bovespa[['Open', 'High', 'Low', 'Close', 'Volume']].copy()

# Criando addplots para os Canais de Donchian usando as variáveis separadas
addplot_20_day_high = mpf.make_addplot(donchian_20_day_high, color='blue', width=1.0)
addplot_10_day_low = mpf.make_addplot(donchian_10_day_low, color='red', width=1.0)

# Criando o gráfico de velas com Canais de Donchian
mpf.plot(cotacao_bovespa_velas, type='candle', style='charles', 
         title='Gráfico de Velas da PETR4.SA com Canais de Donchian', 
         ylabel='Preço (R$)', 
         volume=True, 
         ylabel_lower='Volume',
         figratio=(12,6),
         addplot=[addplot_20_day_high, addplot_10_day_low])
