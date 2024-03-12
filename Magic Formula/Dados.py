# Importação das bibliotecas necessárias
import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf

# URL do site Fundamentus
url = 'https://fundamentus.com.br/resultado.php'

# Configuração do cabeçalho HTTP
data = {"User-Agent":"Mozzila/5.0"}

# Requisição GET para obter o conteúdo HTML da página
response = requests.get(url, headers=data)

# Criação de um objeto BeautifulSoup para analisar o HTML
soup = BeautifulSoup(response.text, 'lxml')

# Extração da tabela de dados da página
tabela = soup.find_all('table')[0]

# Leitura da tabela HTML para um DataFrame do Pandas
df = pd.read_html(str(tabela), decimal=',', thousands='.')[0]

# Salvando o DataFrame como um arquivo Excel
df.to_excel('dadosCompletosFundamentus.xlsx', index=False, engine='openpyxl')

# Filtragem dos dados com liquidez mínima
liquidezMinima = df[df['Liq.2meses'] > 500000]

# Filtragem dos dados com patrimônio líquido positivo
PatrimonioLiquido = liquidezMinima[liquidezMinima['Patrim. Líq'] > 0]

# Seleção de colunas relevantes
dataNovo = PatrimonioLiquido[['Papel', 'ROIC', 'EV/EBIT']]

# Ordenação dos dados por EV/EBIT
EvOrdenado = dataNovo.sort_values(by='EV/EBIT')
EvOrdenado = EvOrdenado.reset_index(drop=True)
EvOrdenado['EvOrdenado'] = EvOrdenado.index

# Ordenação dos dados por ROIC
RoicOrdenado = EvOrdenado.sort_values(by='ROIC', ascending=False)
RoicOrdenado = RoicOrdenado.reset_index(drop=True)
RoicOrdenado['RoicOrdenado'] = RoicOrdenado.index

# DataFrame final com dados ordenados
dados = RoicOrdenado

# Cálculo da métrica "magic"
dados['magic'] = dados['EvOrdenado'] + dados['RoicOrdenado']

# Ordenação dos dados por "magic" e seleção dos primeiros 30
carteira = dados.sort_values(by='magic').head(30)

# Impressão da carteira
print(carteira)
