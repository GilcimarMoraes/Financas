# Importação das bibliotecas necessárias
import pandas as pd
import wget
from zipfile import ZipFile
import os

# Armazena o diretório atual
diretorio_atual = os.getcwd()

# Muda para o diretório onde serão armazenados os arquivos baixados
os.chdir(f'{diretorio_atual}/dados_cvm')

# URL onde os arquivos ZIP estão localizados
url = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'

# Lista dos arquivos ZIP a serem baixados, de 2013 a 2023
dados_cvm = []
anos = range(2013, 2024)

for ano in anos:
    dados_cvm.append(f'itr_cia_aberta_{ano}.zip')

# Baixa os arquivos ZIP
for i in dados_cvm:
    wget.download(url + i)

# Extrai os arquivos ZIP baixados
for i in dados_cvm:
    ZipFile(i, 'r').extractall('ITR')

# Lista dos nomes dos arquivos CSV a serem unificados
nomes = ['BPA_con', 'BPA_ind', 'BPP_con', 'BPP_ind', 'DFC_MD_con', 'DFC_MD_ind', 'DFC_MI_con', 'DFC_MI_ind', 'DMPL_con', 'DMPL_ind', 'DRE_con', 'DRE_ind', 'DVA_con', 'DVA_ind']

# Itera sobre cada nome de arquivo para unificar os dados
for nome in nomes:
    arquivo = pd.DataFrame()
    # Itera sobre cada ano para ler os dados de cada arquivo CSV e unificá-los
    for ano in anos:
        # Caminho do arquivo CSV para o ano e nome especificados
        caminho = 'ITR\itr_cia_aberta_{}_{}.csv'.format(nome, ano)
        # Lê o arquivo CSV e adiciona ao DataFrame 'arquivo'
        arquivo = pd.concat([arquivo, pd.read_csv(caminho, sep=';', decimal=',', encoding='ISO-8859-1')])
    
    # Salva o DataFrame unificado como um novo arquivo CSV
    arquivo.to_csv(f'Dados_unificados/itr_cia_aberta_{nome}_2013-2023.csv', index=False)


