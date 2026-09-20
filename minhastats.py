"""
==============================================================================
 minhastats.py — O NÚCLEO ESTATÍSTICO DA EQUIPE
 (Etapa 2 do guia — Critério 1 do barema — 25% da nota)
==============================================================================

COMO USAR ESTE ARQUIVO (leia com calma, é simples)

  1. Leia a Etapa 2 do guia antes de começar.
  2. Aperte Ctrl+F e procure por "TODO". Cada TODO é UMA função para vocês
     escreverem. Faça na ordem: TODO 1, depois TODO 2, e assim por diante.
  3. Dentro de cada função há PASSOS escritos em comentários (linhas com #).
     Traduza cada passo em UMA linha de código, logo abaixo do comentário.
  4. Quando terminar a função, APAGUE a linha que começa com
     "raise NotImplementedError". Ela só existe para avisar que falta fazer.
  5. Abra o terminal e rode:   pytest -v
     Se o teste da sua função aparecer em verde (PASSED), ela está certa.
  6. Faça um commit ("implementa mediana + teste passando") e vá para o
     próximo TODO.

REGRA DE OURO (vale 25% da nota — não quebre)

  Neste arquivo é PROIBIDO importar numpy, pandas, statistics ou scipy.
  Só pode Python puro: sum, len, sorted, min, max, abs, round, laços for,
  if/else, listas e dicionários. O módulo `math` é permitido apenas para
  log10, ceil, sqrt, exp, pi e factorial.

  Dica: rode  python verificar_regra_de_ouro.py  para conferir.

DICA DE OURO PARA INICIANTES
  As funções abaixo se COMPÕEM como peças de LEGO: a variância usa a média,
  o desvio usa a variância, os quartis usam o percentil, os outliers usam
  os quartis, a correlação usa a covariância e o desvio. Reutilize!
"""

import math


# =============================================================================
# PARTE A — FUNÇÕES JÁ PRONTAS (exemplos do guia — leia e entenda o padrão)
# =============================================================================

def media(dados):
    """Média aritmética: soma de todos os valores dividida pela contagem.

    média = (1/n) · Σ xi
    """
    if len(dados) == 0:
        raise ValueError("média de sequência vazia é indefinida")
    return sum(dados) / len(dados)


def variancia(dados, amostral=True):
    """Variância. amostral=True divide por n-1 (correção de Bessel); False, por n.

    s²  = Σ(xi − média)² / (n − 1)   (amostral)
    σ²  = Σ(xi − média)² / n         (populacional)
    """
    n = len(dados)
    if n == 0:
        raise ValueError("variância de sequência vazia é indefinida")
    if n < 2 and amostral:
        raise ValueError("variância amostral exige n >= 2")
    m = media(dados)
    soma_quad = sum((x - m) ** 2 for x in dados)
    return soma_quad / (n - 1 if amostral else n)


def desvio_padrao(dados, amostral=True):
    """Desvio padrão = raiz quadrada da variância."""
    return variancia(dados, amostral) ** 0.5


def contar_frequencias(dados):
    """Conta quantas vezes cada valor aparece. Devolve um dicionário {valor: contagem}.

    Exemplo: contar_frequencias([1, 2, 2, 3]) -> {1: 1, 2: 2, 3: 1}
    Use esta função dentro da moda (TODO 2) e para variáveis categóricas.
    """
    contagens = {}
    for x in dados:
        if x in contagens:
            contagens[x] = contagens[x] + 1
        else:
            contagens[x] = 1
    return contagens


def tabela_frequencias(dados, k):
    """Tabela de frequências com k classes de mesma largura.

    Devolve uma lista de dicionários, um por classe, com as chaves:
    classe, limite_inferior, limite_superior, frequencia, freq_relativa,
    freq_acumulada.
    """
    if len(dados) == 0:
        raise ValueError("tabela de frequências de sequência vazia é indefinida")
    if k < 1:
        raise ValueError("número de classes deve ser >= 1")
    n = len(dados)
    minimo, maximo = min(dados), max(dados)

    if maximo == minimo:  # todos os valores iguais: uma classe só
        return [{
            "classe": f"[{minimo:.2f}, {maximo:.2f}]",
            "limite_inferior": minimo, "limite_superior": maximo,
            "frequencia": n, "freq_relativa": 1.0, "freq_acumulada": n,
        }]

    largura = (maximo - minimo) / k
    contagens = [0] * k
    for x in dados:
        indice = int((x - minimo) / largura)
        indice = min(indice, k - 1)  # o valor máximo cai na última classe
        contagens[indice] += 1

    linhas = []
    acumulada = 0
    for i in range(k):
        li = minimo + i * largura
        ls = li + largura
        acumulada += contagens[i]
        fecha = "]" if i == k - 1 else ")"
        linhas.append({
            "classe": f"[{li:.2f}, {ls:.2f}{fecha}",
            "limite_inferior": li, "limite_superior": ls,
            "frequencia": contagens[i],
            "freq_relativa": contagens[i] / n,
            "freq_acumulada": acumulada,
        })
    return linhas


# --- Densidades teóricas (Módulo 4). Fórmulas de livro; usadas para desenhar
#     a curva por cima do histograma. Os PARÂMETROS vêm das SUAS funções. ---

def densidade_normal(x, mu, sigma):
    """f(x) da Normal(mu, sigma)."""
    if sigma <= 0:
        raise ValueError("sigma deve ser > 0")
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)


def densidade_exponencial(x, lam):
    """f(x) da Exponencial com taxa lam (= 1/média). Vale 0 para x < 0."""
    if lam <= 0:
        raise ValueError("lambda deve ser > 0")
    if x < 0:
        return 0.0
    return lam * math.exp(-lam * x)


def densidade_uniforme(x, a, b):
    """f(x) da Uniforme contínua em [a, b]."""
    if b <= a:
        raise ValueError("b deve ser maior que a")
    if a <= x <= b:
        return 1 / (b - a)
    return 0.0


def massa_poisson(k, lam):
    """P(X = k) da Poisson(lam), para k inteiro >= 0."""
    if lam <= 0:
        raise ValueError("lambda deve ser > 0")
    if k < 0:
        return 0.0
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


# =============================================================================
# PARTE B — OS TODOs (o trabalho de vocês). Faça na ordem.
# =============================================================================

# -----------------------------------------------------------------------------
# TODO 1 — MEDIANA
# -----------------------------------------------------------------------------
def mediana(dados):
    """Mediana: valor central dos dados ordenados."""
    if len(dados) == 0:
        raise ValueError("mediana de sequência vazia é indefinida")

    ordenados = sorted(dados)
    n = len(ordenados)
    meio = n // 2

    if n % 2 == 1:
        return ordenados[meio]

    return (ordenados[meio - 1] + ordenados[meio]) / 2


# -----------------------------------------------------------------------------
# TODO 2 — MODA
# -----------------------------------------------------------------------------
def moda(dados):
    """Devolve uma lista com a(s) moda(s)."""
    if len(dados) == 0:
        raise ValueError("moda de sequência vazia é indefinida")

    contagens = contar_frequencias(dados)
    maior_frequencia = max(contagens.values())

    return [
        valor
        for valor, frequencia in contagens.items()
        if frequencia == maior_frequencia
    ]


# -----------------------------------------------------------------------------
# TODO 3 — AMPLITUDE
# -----------------------------------------------------------------------------
def amplitude(dados):
    """Amplitude = maior valor - menor valor."""
    if len(dados) == 0:
        raise ValueError("amplitude de sequência vazia é indefinida")

    return max(dados) - min(dados)


# -----------------------------------------------------------------------------
# TODO 4 — PERCENTIL
# -----------------------------------------------------------------------------
def percentil(dados, p):
    """Percentil usando interpolação linear."""
    if len(dados) == 0:
        raise ValueError("percentil de sequência vazia é indefinido")

    if p < 0 or p > 100:
        raise ValueError("p deve estar entre 0 e 100")

    ordenados = sorted(dados)
    n = len(ordenados)

    posicao = p * (n - 1) / 100
    baixo = int(posicao)
    alto = min(baixo + 1, n - 1)
    fracao = posicao - baixo

    return ordenados[baixo] + fracao * (
        ordenados[alto] - ordenados[baixo]
    )


# -----------------------------------------------------------------------------
# TODO 5 — QUARTIS  (reutiliza o percentil — LEGO!)
# -----------------------------------------------------------------------------
def quartis(dados):
    """Devolve Q1, Q2 e Q3."""
    q1 = percentil(dados, 25)
    q2 = percentil(dados, 50)
    q3 = percentil(dados, 75)

    return q1, q2, q3


# -----------------------------------------------------------------------------
# TODO 6 — COEFICIENTE DE VARIAÇÃO
# -----------------------------------------------------------------------------
def coeficiente_variacao(dados, em_percentual=True):
    """Calcula o coeficiente de variação."""
    m = media(dados)

    if m == 0:
        raise ValueError(
            "coeficiente de variação indefinido: média é zero"
        )

    cv = desvio_padrao(dados) / m

    if em_percentual:
        return cv * 100

    return cv


# -----------------------------------------------------------------------------
# TODO 7 — COVARIÂNCIA
# -----------------------------------------------------------------------------
def covariancia(x, y, amostral=True):
    """Calcula a covariância entre duas listas."""
    if len(x) != len(y):
        raise ValueError("x e y devem ter o mesmo tamanho")

    n = len(x)

    if n == 0:
        raise ValueError("covariância de sequência vazia é indefinida")

    if n < 2 and amostral:
        raise ValueError("covariância amostral exige n >= 2")

    mx = media(x)
    my = media(y)

    soma = sum(
        (xi - mx) * (yi - my)
        for xi, yi in zip(x, y)
    )

    divisor = n - 1 if amostral else n

    return soma / divisor


# -----------------------------------------------------------------------------
# TODO 8 — CORRELAÇÃO DE PEARSON
# -----------------------------------------------------------------------------
def correlacao(x, y):
    """Calcula a correlação de Pearson."""
    if len(x) != len(y):
        raise ValueError("x e y devem ter o mesmo tamanho")

    if len(x) < 2:
        raise ValueError("correlação exige pelo menos dois valores")

    sx = desvio_padrao(x)
    sy = desvio_padrao(y)

    if sx == 0 or sy == 0:
        raise ValueError("correlação indefinida: variável constante")

    return covariancia(x, y) / (sx * sy)


# -----------------------------------------------------------------------------
# TODO 9 — REGRA DE STURGES  (Módulo 2: nº de classes do histograma)
# -----------------------------------------------------------------------------
def numero_classes_sturges(n):
    """Calcula o número de classes pela regra de Sturges."""
    if n <= 0:
        raise ValueError("n deve ser positivo")

    return math.ceil(1 + 3.322 * math.log10(n))


# -----------------------------------------------------------------------------
# TODO 10 — OUTLIERS PELA REGRA DO IQR  (reutiliza quartis — LEGO!)
# -----------------------------------------------------------------------------
def outliers_iqr(dados):
    """Identifica outliers pela regra do IQR."""
    q1, q2, q3 = quartis(dados)

    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    outliers = [
        x
        for x in dados
        if x < limite_inferior or x > limite_superior
    ]

    return limite_inferior, limite_superior, outliers


# -----------------------------------------------------------------------------
# TODO 11 — INTERPRETAÇÃO TEXTUAL AUTOMÁTICA  (o que separa app de calculadora)
# -----------------------------------------------------------------------------

# O guia sugere "mais de meio desvio" (0.5). Na prática |média − mediana| quase
# nunca passa de metade do desvio, então 0.2 já detecta assimetrias visíveis
# no histograma. A equipe pode ajustar — e deve JUSTIFICAR a escolha no relatório.
FOLGA_ASSIMETRIA = 0.2


def interpretar_assimetria(dados):
    """Interpreta a assimetria comparando média e mediana."""
    m = media(dados)
    md = mediana(dados)
    s = desvio_padrao(dados)

    if s == 0:
        return "Todos os valores são iguais: não há dispersão."

    folga = FOLGA_ASSIMETRIA * s

    if m - md > folga:
        return (
            f"Assimetria à direita: valores altos puxam a média "
            f"(média = {m:.2f} > mediana = {md:.2f})."
        )

    if md - m > folga:
        return (
            f"Assimetria à esquerda: valores baixos puxam a média "
            f"(mediana = {md:.2f} > média = {m:.2f})."
        )

    return (
        f"Distribuição aproximadamente simétrica "
        f"(média = {m:.2f}, mediana = {md:.2f})."
    )


# -----------------------------------------------------------------------------
# TODO 12 — REGRESSÃO LINEAR SIMPLES (mínimos quadrados)
# -----------------------------------------------------------------------------
def regressao_linear(x, y):
    """Calcula regressão linear simples."""
    if len(x) != len(y) or len(x) < 2:
        raise ValueError(
            "x e y devem ter o mesmo tamanho e pelo menos dois valores"
        )

    mx = media(x)
    my = media(y)

    numerador = sum(
        (xi - mx) * (yi - my)
        for xi, yi in zip(x, y)
    )

    denominador = sum(
        (xi - mx) ** 2
        for xi in x
    )

    if denominador == 0:
        raise ValueError("x é constante: reta indefinida")

    b1 = numerador / denominador
    b0 = my - b1 * mx

    previstos = [
        b0 + b1 * xi
        for xi in x
    ]

    sq_res = sum(
        (yi - yp) ** 2
        for yi, yp in zip(y, previstos)
    )

    sq_tot = sum(
        (yi - my) ** 2
        for yi in y
    )

    if sq_tot == 0:
        raise ValueError("y é constante: R² indefinido")

    r2 = 1 - sq_res / sq_tot

    return b0, b1, r2


# =============================================================================
# FIM. Se todos os testes passaram:  git add . && git commit -m "núcleo completo"
# =============================================================================
