import pandas as pd
from zipfile import ZipFile
import os
import requests

diretorio_atual = os.getcwd()

os.chdir(f'{diretorio_atual}')

diretorio_atual

anos = range(2013, 2023)

url = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/'

dados_dfp = []

for ano in anos:
    dados_dfp.append(f'dfp_cia_aberta_{ano}.zip')

for arquivo in dados_dfp:
    download = requests.get(url + arquivo)

    open(arquivo, 'wb').write(download.content)

    with ZipFile(arquivo, 'r') as zip_ref:
        zip_ref.extractall()

lista_demosntracoes_2013_2023 = []

for i in os.listdir(diretorio_atual):
    if 'CIA_ABERTA' in i:
        arquivo_zip = ZipFile(i)

        for planilha in arquivo_zip.namelist():
            if 'CIA_ABERTA' in planilha:
                demonstracao = pd.read_csv(arquivo_zip.open(planilha), sep = ';', encoding= 'ISO-8859-1', dtype = {'ORDEM_EXERC': 'category'})

                demonstracao['ANO'] = int(i.split('_')[1].split('.')[0])

                lista_demosntracoes_2013_2023.append(demonstracao)

base_dados = pd.concat(lista_demosntracoes_2013_2023)

base_dados.head(5)

base_dados[['con_ind', 'tipo_dem']] = base_dados['GRUPO_DFP'].str.split('-', expand = True)
base_dados['con_ind'] = base_dados['con_ind'].str.strip()
base_dados['tipo_dem'] = base_dados['tipo_dem'].str.strip()
base_dados = base_dados[base_dados['ORDEM_EXERC'] != 'PENÚLTIMO']

# Adicionar colunas para calcular os indicadores ROIC e EV/EBIT

# ROIC = (Lucro Operacional + Lucro Financeiro + Lucro Extraordinário) / (Patrimônio Líquido + Dívida Líquida)

base_dados['Lucro Operacional'] = base_dados['RESULTADO_OPERACIONAL']
base_dados['Lucro Financeiro'] = base_dados['RESULTADO_FINANCEIRO']
base_dados['Lucro Extraordinário'] = base_dados['RESULTADO_EXTRAORDINARIO']

base_dados['Patrimônio Líquido'] = base_dados['PATRIMONIO_LIQUIDO']
base_dados['Dívida Líquida'] = base_dados['DIVIDA_LIQUIDA']

base_dados['ROIC'] = (base_dados['Lucro Operacional'] + base_dados['Lucro Financeiro'] + base_dados['Lucro Extraordinário']) / (base_dados['Patrimônio Líquido'] + base_dados['Dívida Líquida'])

# EV/EBIT = Valor de Mercado / EBIT

base_dados['Valor de Mercado'] = base_dados['MERCADO_TOTAL']
base_dados['EBIT'] = base_dados['RESULTADO_OPERACIONAL']

base_dados['EV/EBIT'] = base_dados['Valor de Mercado'] / base_dados['EBIT']

base_dados = base_dados.drop(['Lucro Operacional', 'Lucro Financeiro', 'Lucro Extraordinário', 'Patrimônio Líquido', 'Dívida Líquida', 'Valor de Mercado'], axis=1)

base_dados.head(5)