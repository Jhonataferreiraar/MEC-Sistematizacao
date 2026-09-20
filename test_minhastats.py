"""
==============================================================================
 test_minhastats.py — OS TESTES QUE PROVAM O NÚCLEO  (Etapa 2.5 do guia)
==============================================================================

Estes testes já estão prontos. Vocês NÃO precisam mexer aqui.
Eles comparam CADA função de vocês com a referência (NumPy / SciPy).

COMO RODAR (no terminal, dentro da pasta do projeto, com o venv ativado):

    pytest -v

O que você vai ver:
  - PASSED  (verde)   -> a função está certa. Comemore e faça um commit.
  - FAILED  (vermelho) -> leia a mensagem. Se disser "NotImplementedError:
                          TODO n", é só porque ainda não fez esse TODO.
                          Se disser "assert False", a conta está errada:
                          compare com a fórmula do guia.

Para rodar só um teste:   pytest -v -k mediana

Sobre a tolerância: números de ponto flutuante somados em ordens diferentes
divergem nas últimas casas — por isso usamos np.isclose com rtol.
Anote as tolerâncias abaixo na tabela de validação do RELATORIO.md.
"""

import collections
import math

import numpy as np
import pytest
from scipy import stats

import minhastats as ms

# --------------------------- dados de referência -----------------------------
RNG = np.random.default_rng(0)
DADOS = RNG.gamma(2, 9, 500).tolist()            # assimétrico à direita
X = RNG.normal(50, 10, 300).tolist()
Y = [2.0 * xi + ruido for xi, ruido in zip(X, RNG.normal(0, 5, 300))]
INTEIROS = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

TOL_EXATA = 1e-9      # média, variância, covariância, correlação, regressão
TOL_PERCENTIL = 1e-6  # percentil: convenções diferentes divergem mais


# =============================== PARTE A =====================================

def test_media():
    assert np.isclose(ms.media(DADOS), np.mean(DADOS), rtol=TOL_EXATA)


def test_media_vazia_levanta_erro():
    with pytest.raises(ValueError):
        ms.media([])


def test_variancia_amostral():
    assert np.isclose(ms.variancia(DADOS, amostral=True),
                      np.var(DADOS, ddof=1), rtol=TOL_EXATA)   # ddof=1 = n-1!


def test_variancia_populacional():
    assert np.isclose(ms.variancia(DADOS, amostral=False),
                      np.var(DADOS, ddof=0), rtol=TOL_EXATA)


def test_desvio_padrao():
    assert np.isclose(ms.desvio_padrao(DADOS), np.std(DADOS, ddof=1), rtol=TOL_EXATA)
    assert np.isclose(ms.desvio_padrao(DADOS, amostral=False),
                      np.std(DADOS, ddof=0), rtol=TOL_EXATA)


def test_contar_frequencias():
    assert ms.contar_frequencias(INTEIROS) == dict(collections.Counter(INTEIROS))


def test_tabela_frequencias_soma_bate():
    tabela = ms.tabela_frequencias(DADOS, 10)
    assert len(tabela) == 10
    assert sum(linha["frequencia"] for linha in tabela) == len(DADOS)
    assert tabela[-1]["freq_acumulada"] == len(DADOS)
    assert np.isclose(sum(linha["freq_relativa"] for linha in tabela), 1.0)


def test_densidades_teoricas():
    assert np.isclose(ms.densidade_normal(1.0, 0.0, 1.0), stats.norm.pdf(1.0, 0, 1))
    assert np.isclose(ms.densidade_exponencial(2.0, 0.5), stats.expon.pdf(2.0, scale=2))
    assert np.isclose(ms.densidade_uniforme(3.0, 1.0, 5.0), stats.uniform.pdf(3.0, 1, 4))
    assert np.isclose(ms.massa_poisson(3, 2.5), stats.poisson.pmf(3, 2.5))


# =============================== PARTE B =====================================

# ---- TODO 1 ----
def test_mediana_n_impar():
    assert np.isclose(ms.mediana(INTEIROS), np.median(INTEIROS))


def test_mediana_n_par():
    assert np.isclose(ms.mediana(DADOS), np.median(DADOS))       # 500 é par
    assert ms.mediana([4, 1, 3, 2]) == 2.5


def test_mediana_vazia_levanta_erro():
    with pytest.raises(ValueError):
        ms.mediana([])


# ---- TODO 2 ----
def test_moda_unica():
    assert list(ms.moda(INTEIROS)) == [5]


def test_moda_multipla_devolve_lista():
    assert sorted(ms.moda([1, 2, 2, 3, 3])) == [2, 3]


def test_moda_categorica():
    assert list(ms.moda(["PC", "Mobile", "PC"])) == ["PC"]


# ---- TODO 3 ----
def test_amplitude():
    assert np.isclose(ms.amplitude(DADOS), np.ptp(DADOS))


def test_amplitude_n_igual_a_1():
    assert ms.amplitude([7.5]) == 0


# ---- TODO 4 ----
@pytest.mark.parametrize("p", [0, 10, 25, 50, 75, 90, 100])
def test_percentil(p):
    assert np.isclose(ms.percentil(DADOS, p), np.percentile(DADOS, p), rtol=TOL_PERCENTIL)


def test_percentil_exemplo_do_enunciado():
    assert ms.percentil([10, 20, 30, 40], 50) == 25.0


def test_percentil_p_invalido():
    with pytest.raises(ValueError):
        ms.percentil(DADOS, 150)


# ---- TODO 5 ----
def test_quartis():
    q1, q2, q3 = ms.quartis(DADOS)
    assert np.isclose(q1, np.percentile(DADOS, 25), rtol=TOL_PERCENTIL)
    assert np.isclose(q2, np.percentile(DADOS, 50), rtol=TOL_PERCENTIL)
    assert np.isclose(q3, np.percentile(DADOS, 75), rtol=TOL_PERCENTIL)


# ---- TODO 6 ----
def test_coeficiente_variacao():
    esperado = np.std(DADOS, ddof=1) / np.mean(DADOS)
    assert np.isclose(ms.coeficiente_variacao(DADOS, em_percentual=False), esperado, rtol=TOL_EXATA)
    assert np.isclose(ms.coeficiente_variacao(DADOS), esperado * 100, rtol=TOL_EXATA)


def test_coeficiente_variacao_media_zero():
    with pytest.raises(ValueError):
        ms.coeficiente_variacao([-1, 0, 1])


# ---- TODO 7 ----
def test_covariancia_amostral():
    assert np.isclose(ms.covariancia(X, Y), np.cov(X, Y, ddof=1)[0, 1], rtol=TOL_EXATA)


def test_covariancia_populacional():
    assert np.isclose(ms.covariancia(X, Y, amostral=False),
                      np.cov(X, Y, ddof=0)[0, 1], rtol=TOL_EXATA)


def test_covariancia_tamanhos_diferentes():
    with pytest.raises(ValueError):
        ms.covariancia([1, 2, 3], [1, 2])


# ---- TODO 8 ----
def test_correlacao():
    assert np.isclose(ms.correlacao(X, Y), np.corrcoef(X, Y)[0, 1], rtol=TOL_EXATA)


def test_correlacao_variavel_constante():
    with pytest.raises(ValueError):
        ms.correlacao([1, 2, 3], [5, 5, 5])


# ---- TODO 9 ----
def test_sturges():
    assert ms.numero_classes_sturges(500) == math.ceil(1 + 3.322 * math.log10(500))
    assert ms.numero_classes_sturges(1000) == 11


# ---- TODO 10 ----
def test_outliers_iqr():
    q1, q3 = np.percentile(DADOS, [25, 75])
    iqr = q3 - q1
    li_esp, ls_esp = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    esperados = sorted(x for x in DADOS if x < li_esp or x > ls_esp)

    li, ls, outliers = ms.outliers_iqr(DADOS)
    assert np.isclose(li, li_esp, rtol=TOL_PERCENTIL)
    assert np.isclose(ls, ls_esp, rtol=TOL_PERCENTIL)
    assert sorted(outliers) == esperados


# ---- TODO 11 ----
def test_interpretacao_assimetria_direita():
    exponencial = np.random.default_rng(1).exponential(10, 2000).tolist()
    assert "direita" in ms.interpretar_assimetria(exponencial).lower()


def test_interpretacao_assimetria_esquerda():
    espelhada = (-np.random.default_rng(1).exponential(10, 2000)).tolist()
    assert "esquerda" in ms.interpretar_assimetria(espelhada).lower()


def test_interpretacao_simetrica():
    normal = np.random.default_rng(2).normal(50, 10, 2000).tolist()
    assert "simétrica" in ms.interpretar_assimetria(normal).lower()


# ---- TODO 12 ----
def test_regressao_linear():
    ref = stats.linregress(X, Y)
    b0, b1, r2 = ms.regressao_linear(X, Y)
    assert np.isclose(b0, ref.intercept, rtol=TOL_EXATA)
    assert np.isclose(b1, ref.slope, rtol=TOL_EXATA)
    assert np.isclose(r2, ref.rvalue ** 2, rtol=TOL_EXATA)


def test_regressao_x_constante():
    with pytest.raises(ValueError):
        ms.regressao_linear([2, 2, 2], [1, 2, 3])
