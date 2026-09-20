"""
gerar_dataset_exemplo.py — cria um dataset FICTÍCIO para vocês testarem o app
no primeiro dia, antes de escolher o dataset real.

Rode (da pasta do projeto):    python dados/gerar_dataset_exemplo.py

Ele cria dados/dataset.csv com 1.500 jogos inventados:
  numéricas : preco, horas_jogo_mes (assimétrica!), avaliacao, idade_jogador, num_avaliacoes
  categóricas: genero, plataforma, gratuito

ATENÇÃO: este dataset NÃO vale para a entrega. O guia exige um dataset REAL
(Kaggle, Hugging Face, UCI, dados.gov.br). Quando tiverem o real, substituam
o arquivo dados/dataset.csv e apaguem este script (ou deixem — não atrapalha).
"""

import os

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 1500

genero = rng.choice(["Ação", "RPG", "Estratégia", "Esporte", "Indie"], size=N, p=[0.3, 0.2, 0.15, 0.15, 0.2])
plataforma = rng.choice(["PC", "Console", "Mobile"], size=N, p=[0.45, 0.35, 0.20])
gratuito = rng.choice(["Sim", "Não"], size=N, p=[0.3, 0.7])

preco = np.where(gratuito == "Sim", 0.0, rng.lognormal(mean=3.2, sigma=0.6, size=N)).round(2)
horas_jogo_mes = rng.gamma(shape=2, scale=9, size=N).round(1)          # cauda à direita (ótima para o TCL)
idade_jogador = rng.normal(25, 7, size=N).clip(10, 70).round(0)          # aproximadamente simétrica
num_avaliacoes = rng.poisson(lam=horas_jogo_mes * 2 + 5).astype(int)     # contagem, correlacionada com horas
avaliacao = (55 + 0.6 * horas_jogo_mes + rng.normal(0, 9, size=N)).clip(0, 100).round(1)

# alguns valores ausentes de propósito, para vocês treinarem o tratamento
avaliacao[rng.choice(N, 40, replace=False)] = np.nan
idade_jogador[rng.choice(N, 25, replace=False)] = np.nan

df = pd.DataFrame({
    "jogo_id": np.arange(1, N + 1),
    "genero": genero,
    "plataforma": plataforma,
    "gratuito": gratuito,
    "preco": preco,
    "horas_jogo_mes": horas_jogo_mes,
    "avaliacao": avaliacao,
    "idade_jogador": idade_jogador,
    "num_avaliacoes": num_avaliacoes,
})

destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.csv")
df.to_csv(destino, index=False)
print(f"Dataset de exemplo criado em: {destino}")
print(df.shape, "->", "linhas, colunas")
print(df.head())
