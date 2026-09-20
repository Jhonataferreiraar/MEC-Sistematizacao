"""
verificar_regra_de_ouro.py — confere se a equipe não quebrou a regra de ouro.

Rode:   python verificar_regra_de_ouro.py

Regra de ouro (Critério 1, 25% da nota):
  - minhastats.py NÃO pode importar numpy, pandas, statistics ou scipy.
  - app.py NÃO pode calcular medidas estatísticas com Pandas/NumPy
    (df.mean(), np.percentile(), .describe() ...). Toda medida exibida
    vem de minhastats.

Este script só procura padrões de texto — não substitui a leitura do guia.
"""

import re
import sys

PROIBIDO_NO_NUCLEO = [
    r"^\s*import\s+numpy", r"^\s*from\s+numpy", r"^\s*import\s+pandas", r"^\s*from\s+pandas",
    r"^\s*import\s+statistics", r"^\s*from\s+statistics", r"^\s*import\s+scipy", r"^\s*from\s+scipy",
]
SUSPEITO_NO_APP = [
    r"\.mean\(", r"\.median\(", r"\.std\(", r"\.var\(", r"\.corr\(", r"\.quantile\(",
    r"\.describe\(", r"\.mode\(", r"\.cov\(", r"\.skew\(",
    r"np\.mean", r"np\.median", r"np\.std", r"np\.var", r"np\.percentile", r"np\.average",
    r"np\.corrcoef", r"np\.polyfit", r"np\.cov", r"statistics\.", r"scipy\.stats", r"stats\.linregress",
]


def verificar(arquivo, padroes, mensagem):
    problemas = []
    try:
        with open(arquivo, encoding="utf-8") as f:
            for numero, linha in enumerate(f, start=1):
                sem_comentario = linha.split("#")[0]
                if any(re.search(padrao, sem_comentario) for padrao in padroes):
                    problemas.append(f"  {arquivo}:{numero}: {linha.strip()}")
    except FileNotFoundError:
        print(f"(aviso) {arquivo} não encontrado — pulei.")
        return True
    if problemas:
        print(f"[ERRO] {mensagem}")
        print("\n".join(problemas))
        return False
    print(f"[OK] {arquivo}")
    return True


ok_nucleo = verificar("minhastats.py", PROIBIDO_NO_NUCLEO,
                      "minhastats.py importa biblioteca proibida (numpy/pandas/statistics/scipy):")
ok_app = verificar("app.py", SUSPEITO_NO_APP,
                   "app.py parece calcular estatística com Pandas/NumPy em vez de minhastats:")

if ok_nucleo and ok_app:
    print("\nRegra de ouro respeitada.")
    sys.exit(0)
print("\nCorrija os pontos acima antes de entregar.")
sys.exit(1)
