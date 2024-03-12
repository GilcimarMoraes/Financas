import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf

url = 'https://fundamentus.com.br/resultado.php'
data = {"User-Agent":"Mozzila/5.0"}
response = requests.get(url, headers=data)
soup = BeautifulSoup(response.text,'lxml')
tabela = soup.find_all('table')[0]
df = pd.read_html(str(tabela), decimal = ',', thousands= '.')[0]

df.to_excel('dadosCompletosFundamentus.xlsx', index = False, engine = 'openpyxl')

liquidezMinima = df[df['Liq.2meses'] > 500000]

PatrimonioLiquido = liquidezMinima[liquidezMinima['Patrim. Líq'] > 0]

dataNovo = PatrimonioLiquido[['Papel', 'ROIC', 'EV/EBIT']]

EvOrdenado = dataNovo.sort_values(by = 'EV/EBIT')
EvOrdenado = EvOrdenado.reset_index(drop = True)
EvOrdenado['EvOrdenado'] = EvOrdenado.index

RoicOrdenado = EvOrdenado.sort_values(by = 'ROIC', ascending = False)
RoicOrdenado = RoicOrdenado.reset_index(drop = True)
RoicOrdenado['RoicOrdenado'] = RoicOrdenado.index
dados = RoicOrdenado

dados['magic'] = dados['EvOrdenado'] + dados['RoicOrdenado']
dados.sort_values(by = 'magic')

carteira = dados.sort_values(by = 'magic').head(30)

print(carteira)