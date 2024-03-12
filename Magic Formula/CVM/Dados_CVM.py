import pandas as pd
import wget
from zipfile import ZipFile
import os
diretorio_atual = os.getcwd()
os.chdir(f'{diretorio_atual}/dados_cvm')


url = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'
dados_cvm = []
anos = range(2013, 2024)

for ano in anos:
    dados_cvm.append(f'itr_cia_aberta_{ano}.zip')

dados_cvm
for i in dados_cvm:
    wget.download(url + i)
for i in dados_cvm:
    ZipFile(i,  'r').extractall('ITR')
nomes = ['BPA_con', 'BPA_ind', 'BPP_con', 'BPP_ind', 'DFC_MD_con', 'DFC_MD_ind', 'DFC_MI_con', 'DFC_MI_ind', 'DMPL_con', 'DMPL_ind', 'DRE_con', 'DRE_ind', 'DVA_con', 'DVA_ind']
for nome in nomes:
    arquivo = pd.DataFrame()
    for ano in anos:
        caminho = 'ITR\itr_cia_aberta_{}_{}.csv'.format(nome, ano)
        arquivo = pd.concat([arquivo, pd.read_csv(caminho, sep=';', decimal=',', encoding='ISO-8859-1')])
    
    arquivo.to_csv(f'Dados_unificados/itr_cia_aberta_{nome}_2013-2,-2023', index = False)

