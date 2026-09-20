"""
inspecionar_dataset.py — a "inspeção de 5 minutos que economiza uma semana"
(Código 1.1 do guia, Etapa 1).

Rode:   python inspecionar_dataset.py

Responda às perguntas dos comentários. Se o dataset falhar em DOIS itens,
troquem de dataset AGORA — é barato hoje, caro na semana 3.
"""

import pandas as pd

CAMINHO = "dados/dataset.csv"   # TODO (opcional): mude se o CSV tiver outro nome
SEPARADOR = ","                 # use ";" para CSV brasileiro separado por ponto e vírgula
DECIMAL = "."                   # use "," se os números vierem como 3,14

df = pd.read_csv(CAMINHO, sep=SEPARADOR, decimal=DECIMAL)

print("\n=== 1. TAMANHO (linhas, colunas) -> linhas >= 1000? ===")
print(df.shape)

print("\n=== 2. TIPOS -> >= 4 numéricas e >= 2 categóricas? ===")
print(df.dtypes)
print(f"\nnuméricas: {len(df.select_dtypes('number').columns)} | "
      f"não numéricas: {len(df.columns) - len(df.select_dtypes('number').columns)}")

print("\n=== 3. FRAÇÃO DE NULOS POR COLUNA -> < 20%? ===")
print(df.isna().mean().round(3))

print("\n=== 4. RESUMO -> há variação real ou coluna constante? ===")
print(df.describe())

print("\n=== 5. VALORES DISTINTOS -> categórica com 900 níveis não é categórica útil ===")
print(df.nunique())

print("\nDica: colunas numéricas que apareceram como 'object' têm texto no meio "
      "('N/A', '—', vírgula decimal). Liste-as em COLUNAS_PARA_CONVERTER_EM_NUMERO no app.py.")
