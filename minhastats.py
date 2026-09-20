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
    """Mediana: o valor do meio da lista ORDENADA.

    Regra do guia: ordene; n ímpar -> elemento central;
                   n par   -> média dos dois centrais.
    Armadilha: esquecer de ordenar.

    Exemplos:  mediana([3, 1, 2])    -> 2
               mediana([4, 1, 3, 2]) -> 2.5
    """
    # PASSO 1: se len(dados) == 0, levante ValueError("mediana de sequência vazia é indefinida")

    # PASSO 2: crie uma lista ordenada:  ordenados = sorted(dados)

    # PASSO 3: guarde o tamanho:  n = len(ordenados)

    # PASSO 4: descubra o índice do meio:  meio = n // 2   (divisão inteira)

    # PASSO 5: se n for ímpar (n % 2 == 1), devolva ordenados[meio]

    # PASSO 6: se n for par, devolva (ordenados[meio - 1] + ordenados[meio]) / 2

    raise NotImplementedError("TODO 1: implemente mediana() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 2 — MODA
# -----------------------------------------------------------------------------
def moda(dados):
    """Moda: o(s) valor(es) que mais se repete(m). Devolve SEMPRE uma LISTA,
    porque pode haver empate (várias modas).

    Exemplos:  moda([1, 2, 2, 3])    -> [2]
               moda([1, 2, 2, 3, 3]) -> [2, 3]
    """
    # PASSO 1: se len(dados) == 0, levante ValueError("moda de sequência vazia é indefinida")

    # PASSO 2: conte as frequências usando a função pronta:
    #          contagens = contar_frequencias(dados)

    # PASSO 3: descubra a maior contagem:  maior = max(contagens.values())

    # PASSO 4: monte a lista dos valores cuja contagem é igual à maior:
    #          modas = [valor for valor, cont in contagens.items() if cont == maior]

    # PASSO 5: devolva a lista (pode ordenar com sorted(modas) se os valores forem números)

    raise NotImplementedError("TODO 2: implemente moda() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 3 — AMPLITUDE
# -----------------------------------------------------------------------------
def amplitude(dados):
    """Amplitude = máximo − mínimo.

    Armadilha do guia: "trivial — mas teste com n = 1" (a resposta deve ser 0).
    """
    # PASSO 1: se len(dados) == 0, levante ValueError("amplitude de sequência vazia é indefinida")

    # PASSO 2: devolva max(dados) - min(dados)

    raise NotImplementedError("TODO 3: implemente amplitude() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 4 — PERCENTIL
# -----------------------------------------------------------------------------
def percentil(dados, p):
    """Percentil p (de 0 a 100) com interpolação linear — a MESMA convenção do
    np.percentile, para o teste bater.

    Regra do guia: posição = p·(n−1)/100 no vetor ordenado; se a posição for
    fracionária (ex.: 3.25), interpole entre os vizinhos (índices 3 e 4).

    Exemplo:  percentil([10, 20, 30, 40], 50) -> 25.0
              (posição = 50·3/100 = 1.5 -> entre 20 e 30 -> 25)
    """
    # PASSO 1: se len(dados) == 0, levante ValueError("percentil de sequência vazia é indefinido")

    # PASSO 2: se p < 0 ou p > 100, levante ValueError("p deve estar entre 0 e 100")

    # PASSO 3: ordenados = sorted(dados)   e   n = len(ordenados)

    # PASSO 4: posicao = p * (n - 1) / 100

    # PASSO 5: parte inteira da posição:   baixo = int(posicao)

    # PASSO 6: o vizinho de cima, sem estourar a lista:   alto = min(baixo + 1, n - 1)

    # PASSO 7: a parte fracionária:   fracao = posicao - baixo

    # PASSO 8: devolva ordenados[baixo] + fracao * (ordenados[alto] - ordenados[baixo])

    raise NotImplementedError("TODO 4: implemente percentil() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 5 — QUARTIS  (reutiliza o percentil — LEGO!)
# -----------------------------------------------------------------------------
def quartis(dados):
    """Devolve a tupla (Q1, Q2, Q3) = percentis 25, 50 e 75.

    Exemplo:  quartis([1, 2, 3, 4, 5]) -> (2.0, 3.0, 4.0)
    """
    # PASSO 1: q1 = percentil(dados, 25)
    # PASSO 2: q2 = percentil(dados, 50)
    # PASSO 3: q3 = percentil(dados, 75)
    # PASSO 4: devolva (q1, q2, q3)

    raise NotImplementedError("TODO 5: implemente quartis() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 6 — COEFICIENTE DE VARIAÇÃO
# -----------------------------------------------------------------------------
def coeficiente_variacao(dados, em_percentual=True):
    """CV = desvio padrão (amostral) / média. Se em_percentual=True, multiplique por 100.

    Armadilha do guia: média zero -> divisão por zero. Trate com ValueError.
    """
    # PASSO 1: m = media(dados)

    # PASSO 2: se m == 0, levante ValueError("coeficiente de variação indefinido: média é zero")

    # PASSO 3: cv = desvio_padrao(dados) / m

    # PASSO 4: se em_percentual for True, devolva cv * 100; senão devolva cv

    raise NotImplementedError("TODO 6: implemente coeficiente_variacao() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 7 — COVARIÂNCIA
# -----------------------------------------------------------------------------
def covariancia(x, y, amostral=True):
    """Covariância entre duas listas de MESMO tamanho.

    cov = Σ (xi − média_x)(yi − média_y) / (n − 1)      (amostral)
    cov = Σ (xi − média_x)(yi − média_y) / n            (populacional)

    Armadilha do guia: vetores de tamanhos diferentes — valide ANTES.
    Dica: zip(x, y) percorre as duas listas ao mesmo tempo:
          for xi, yi in zip(x, y): ...
    """
    # PASSO 1: se len(x) != len(y), levante ValueError("x e y devem ter o mesmo tamanho")

    # PASSO 2: n = len(x); se n == 0 levante ValueError; se n < 2 e amostral, levante ValueError

    # PASSO 3: mx = media(x)   e   my = media(y)

    # PASSO 4: soma = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))

    # PASSO 5: devolva soma / (n - 1) se amostral, senão soma / n

    raise NotImplementedError("TODO 7: implemente covariancia() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 8 — CORRELAÇÃO DE PEARSON
# -----------------------------------------------------------------------------
def correlacao(x, y):
    """r de Pearson = cov(x, y) / (s_x · s_y). Fica sempre entre −1 e 1.

    Armadilha do guia: variável constante tem desvio zero -> divisão por zero.
    """
    # PASSO 1: sx = desvio_padrao(x)   e   sy = desvio_padrao(y)
    #          (a covariancia já valida os tamanhos, mas calcule-a depois dos desvios)

    # PASSO 2: se sx == 0 ou sy == 0, levante ValueError("correlação indefinida: variável constante")

    # PASSO 3: devolva covariancia(x, y) / (sx * sy)

    raise NotImplementedError("TODO 8: implemente correlacao() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 9 — REGRA DE STURGES  (Módulo 2: nº de classes do histograma)
# -----------------------------------------------------------------------------
def numero_classes_sturges(n):
    """k = 1 + 3,322 · log10(n), arredondado PARA CIMA (math.ceil).

    Exemplo: n = 1000 -> 1 + 3.322·3 = 10.966 -> 11 classes.
    """
    # PASSO 1: se n <= 0, levante ValueError("n deve ser positivo")

    # PASSO 2: devolva math.ceil(1 + 3.322 * math.log10(n))

    raise NotImplementedError("TODO 9: implemente numero_classes_sturges() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 10 — OUTLIERS PELA REGRA DO IQR  (reutiliza quartis — LEGO!)
# -----------------------------------------------------------------------------
def outliers_iqr(dados):
    """Regra do IQR: outlier é todo valor fora de [Q1 − 1,5·IQR, Q3 + 1,5·IQR].

    Devolve a tupla (limite_inferior, limite_superior, lista_de_outliers).
    """
    # PASSO 1: q1, q2, q3 = quartis(dados)

    # PASSO 2: iqr = q3 - q1

    # PASSO 3: limite_inferior = q1 - 1.5 * iqr

    # PASSO 4: limite_superior = q3 + 1.5 * iqr

    # PASSO 5: outliers = [x for x in dados if x < limite_inferior or x > limite_superior]

    # PASSO 6: devolva (limite_inferior, limite_superior, outliers)

    raise NotImplementedError("TODO 10: implemente outliers_iqr() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 11 — INTERPRETAÇÃO TEXTUAL AUTOMÁTICA  (o que separa app de calculadora)
# -----------------------------------------------------------------------------

# O guia sugere "mais de meio desvio" (0.5). Na prática |média − mediana| quase
# nunca passa de metade do desvio, então 0.2 já detecta assimetrias visíveis
# no histograma. A equipe pode ajustar — e deve JUSTIFICAR a escolha no relatório.
FOLGA_ASSIMETRIA = 0.2


def interpretar_assimetria(dados):
    """Devolve uma FRASE (string) lendo a relação média × mediana.

    Regra do guia:
      - média > mediana com folga  -> "Assimetria à direita: valores altos puxam a média."
      - mediana > média com folga  -> "Assimetria à esquerda: valores baixos puxam a média."
      - caso contrário             -> "Distribuição aproximadamente simétrica."
    onde "com folga" significa: a diferença é maior que FOLGA_ASSIMETRIA · desvio.

    IMPORTANTE para o teste passar: a frase deve conter a palavra
    "direita", "esquerda" ou "simétrica", conforme o caso.
    """
    # PASSO 1: m = media(dados);  md = mediana(dados);  s = desvio_padrao(dados)

    # PASSO 2: se s == 0, devolva "Todos os valores são iguais: não há dispersão."

    # PASSO 3: folga = FOLGA_ASSIMETRIA * s

    # PASSO 4: se m - md > folga, devolva a frase da assimetria à DIREITA
    #          (dica: inclua os números, ex.: f"... (média = {m:.2f} > mediana = {md:.2f})")

    # PASSO 5: se md - m > folga, devolva a frase da assimetria à ESQUERDA

    # PASSO 6: senão, devolva a frase "aproximadamente simétrica"

    raise NotImplementedError("TODO 11: implemente interpretar_assimetria() em minhastats.py")


# -----------------------------------------------------------------------------
# TODO 12 — REGRESSÃO LINEAR SIMPLES (mínimos quadrados)
# -----------------------------------------------------------------------------
def regressao_linear(x, y):
    """Ajusta a reta  y_prev = b0 + b1·x  e devolve a tupla (b0, b1, r2).

    b1 = Σ(x − média_x)(y − média_y) / Σ(x − média_x)²      (= cov(x,y)/var(x))
    b0 = média_y − b1 · média_x
    R² = 1 − Σ(y − y_prev)² / Σ(y − média_y)²

    O guia mostra esta função completa na Etapa 5. Entenda cada linha antes
    de escrever — na arguição, este é um trecho favorito do professor.
    """
    # PASSO 1: se len(x) != len(y) ou len(x) < 2, levante ValueError

    # PASSO 2: mx = media(x)   e   my = media(y)

    # PASSO 3: numerador   = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))

    # PASSO 4: denominador = sum((xi - mx) ** 2 for xi in x)
    #          se denominador == 0, levante ValueError("x é constante: reta indefinida")

    # PASSO 5: b1 = numerador / denominador

    # PASSO 6: b0 = my - b1 * mx

    # PASSO 7: previstos = [b0 + b1 * xi for xi in x]

    # PASSO 8: sq_res = sum((yi - yp) ** 2 for yi, yp in zip(y, previstos))

    # PASSO 9: sq_tot = sum((yi - my) ** 2 for yi in y)
    #          se sq_tot == 0, levante ValueError("y é constante: R² indefinido")

    # PASSO 10: devolva (b0, b1, 1 - sq_res / sq_tot)

    raise NotImplementedError("TODO 12: implemente regressao_linear() em minhastats.py")


# =============================================================================
# FIM. Se todos os testes passaram:  git add . && git commit -m "núcleo completo"
# =============================================================================
