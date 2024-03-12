# Modelo de Backtest da estratégia de investimento Magic Fórmula
#Verificar a eficácia da "fórmula mágica" de investimento de Joel Greenblatt no mercado brasileiro nos últimos anos.

# Importando as bibliotecas necessárias
import pandas as pd
import quantstats as qs
from datetime import date
import yfinance as yf
import matplotlib.pyplot as plt


# Carregando os dados do mercado financeiro
