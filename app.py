"""
==============================================================================
 app.py — A INTERFACE (Streamlit) do Laboratório Estatístico Interativo
==============================================================================

COMO USAR
  1. Termine PRIMEIRO os TODOs 1 a 12 do minhastats.py (rode `pytest -v`).
  2. Preencha os TODOs 13 a 20 na seção CONFIGURAÇÃO logo abaixo.
     Todos são textos ou nomes de colunas — ninguém precisa mexer no resto.
  3. Rode no terminal:   streamlit run app.py
     O navegador abre sozinho. Ao salvar o arquivo, clique em "Rerun" no app.

O PADRÃO QUE SE REPETE (regra de ouro do guia):
     Pandas CARREGA os dados  ->  .tolist()  ->  MINHASTATS CALCULA  ->  Streamlit MOSTRA
  A linha do .tolist() é a fronteira: dali em diante só as funções de vocês
  tocam os números exibidos. Não calcule média, desvio, percentil ou correlação
  com Pandas/NumPy neste arquivo — o verificar_regra_de_ouro.py acusa.
"""

import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import minhastats as ms  # <- O NÚCLEO DE VOCÊS. Toda conta exibida vem daqui.


# =============================================================================
#                 CONFIGURAÇÃO — PREENCHA OS TODOs 13 a 20
# =============================================================================

# ---- TODO 13: identificação e arquivo de dados ------------------------------
NOME_EQUIPE = "TODO 13: nome da equipe"
CAMINHO_DATASET = "dados/dataset.csv"   # deixe assim se o CSV estiver em dados/
SEPARADOR_CSV = ","                     # use ";" se o CSV brasileiro separar por ponto e vírgula
SEPARADOR_DECIMAL = "."                 # use "," se os números vierem como 3,14

# Colunas que deveriam ser numéricas mas vieram como texto ("N/A", "—", etc.).
# Ex.: ["preco", "nota"]. Elas serão convertidas com pd.to_numeric(errors="coerce").
COLUNAS_PARA_CONVERTER_EM_NUMERO = []

# ---- TODO 14: sobre o dataset (aparece no Módulo 0) --------------------------
NOME_DATASET = "TODO 14: nome do dataset (ex.: Steam Games 2024)"
FONTE_DATASET = "TODO 14: link da fonte ORIGINAL (Kaggle, UCI, dados.gov.br...)"
POR_QUE_ESCOLHEMOS = "TODO 14: 2 ou 3 frases: por que este tema desperta curiosidade na equipe?"
DECISAO_SOBRE_NULOS = (
    "TODO 14: o que fizemos com valores ausentes? (ex.: removemos as linhas com nulos "
    "na variável analisada; a coluna X tinha 'N/A' e foi convertida com to_numeric)."
)

# ---- TODO 15: leitura do Teorema Central do Limite (Módulo 3) ----------------
TEXTO_LEITURA_TCL = (
    "TODO 15: escreva com as palavras da equipe o que acontece com o histograma das "
    "médias quando n cresce, e por que isso explica a Normal aparecer em todo lugar."
)

# ---- TODO 16: discussão do ajuste das distribuições (Módulo 4) ---------------
TEXTO_DISCUSSAO_DISTRIBUICAO = (
    "TODO 16: para a variável que vocês escolheram, a Normal ajusta bem ou mal? Por quê? "
    "(ex.: 'A Normal falha porque a variável tem cauda à direita; a Exponencial descreve melhor.')"
)

# ---- TODO 17: exemplo de causalidade duvidosa (Módulo 5) --------------------
EXEMPLO_CAUSALIDADE_DUVIDOSA = (
    "TODO 17: dê um exemplo DO PRÓPRIO DATASET em que X e Y estão associados "
    "mas um não causa o outro (ex.: 'jogos com mais avaliações têm nota maior, "
    "mas provavelmente é a popularidade que gera as duas coisas')."
)

# ---- TODO 18, 19 e 20: AS TRÊS DESCOBERTAS (Módulo 6) -----------------------
# Cada descoberta tem um "tipo" que diz ao app qual gráfico gerar:
#   "contraste"  -> uma CATEGÓRICA particionando uma NUMÉRICA (boxplots por grupo)
#   "correlacao" -> duas NUMÉRICAS (dispersão + r + reta)
#   "outliers"   -> uma NUMÉRICA (quem são os pontos fora da curva)
# Troque os nomes das colunas pelos do SEU dataset (exatamente como no CSV).
DESCOBERTAS = [
    {   # TODO 18
        "titulo": "TODO 18: título curto da descoberta 1",
        "tipo": "contraste",
        "categorica": "TODO: nome da coluna categórica",
        "numerica": "TODO: nome da coluna numérica",
        "afirmacao": "TODO 18: uma frase que surpreende, compara ou conecta.",
        "limite": "TODO 18: o limite honesto (ex.: 'associação, não causa; amostra só cobre 2023').",
    },
    {   # TODO 19
        "titulo": "TODO 19: título curto da descoberta 2",
        "tipo": "correlacao",
        "x": "TODO: nome da coluna numérica X",
        "y": "TODO: nome da coluna numérica Y",
        "afirmacao": "TODO 19: correlação forte onde não se esperava, ou ausente onde todos jurariam existir.",
        "limite": "TODO 19: o limite honesto.",
    },
    {   # TODO 20
        "titulo": "TODO 20: título curto da descoberta 3",
        "tipo": "outliers",
        "numerica": "TODO: nome da coluna numérica",
        "afirmacao": "TODO 20: quem são os outliers e o que têm em comum?",
        "limite": "TODO 20: o limite honesto.",
    },
]

# =============================================================================
#      DAQUI PARA BAIXO NÃO PRECISA MEXER (mas leia — cai na arguição!)
# =============================================================================

st.set_page_config(page_title="Laboratório Estatístico Interativo", layout="wide")


# ------------------------------- utilidades ----------------------------------

@st.cache_data
def carregar_dados(caminho, sep, decimal, colunas_converter):
    """Pandas carrega e limpa. Estatística, NUNCA aqui."""
    df = pd.read_csv(caminho, sep=sep, decimal=decimal)
    for coluna in colunas_converter:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df


def colunas_numericas(df):
    return list(df.select_dtypes("number").columns)


def colunas_categoricas(df):
    return [c for c in df.columns if c not in colunas_numericas(df)]


def lista_limpa(df, coluna):
    """A FRONTEIRA da regra de ouro: sai um DataFrame, entra uma lista pura."""
    return df[coluna].dropna().tolist()


def nova_figura(largura=10, altura=4, colunas=1):
    fig, eixos = plt.subplots(1, colunas, figsize=(largura, altura))
    return fig, eixos


def mostrar(fig):
    st.pyplot(fig)
    plt.close(fig)


def rodar_modulo(funcao, df):
    """Executa um módulo e traduz erros em mensagens amigáveis para iniciantes."""
    try:
        funcao(df)
    except NotImplementedError as erro:
        st.error(f"⚠️ Falta implementar uma função do núcleo: **{erro}**")
        st.info("Abra o arquivo minhastats.py, procure o TODO indicado, implemente e rode `pytest -v`. "
                "Depois volte aqui e clique em Rerun.")
    except ValueError as erro:
        st.warning(f"Não foi possível calcular: {erro}")


def eh_todo(texto):
    return isinstance(texto, str) and texto.strip().upper().startswith("TODO")


def texto_ou_aviso(texto, rotulo):
    if eh_todo(texto):
        st.warning(f"✏️ {rotulo} ainda não foi preenchido em app.py: {texto}")
    else:
        st.info(texto)


# =============================================================================
# MÓDULO 0 — O DATASET
# =============================================================================

def modulo_0_dataset(df):
    st.header("Módulo 0 — O dataset")
    st.subheader(NOME_DATASET)
    st.markdown(f"**Fonte original:** {FONTE_DATASET}")
    texto_ou_aviso(POR_QUE_ESCOLHEMOS, "A justificativa da escolha")

    n_linhas, n_colunas = df.shape
    num = colunas_numericas(df)
    cat = colunas_categoricas(df)

    st.markdown("### O contrato do guia (≥ 1.000 registros, ≥ 4 numéricas, ≥ 2 categóricas)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Registros (linhas)", n_linhas, "✅" if n_linhas >= 1000 else "❌ menos de 1000")
    c2.metric("Variáveis numéricas", len(num), "✅" if len(num) >= 4 else "❌ menos de 4")
    c3.metric("Variáveis categóricas", len(cat), "✅" if len(cat) >= 2 else "❌ menos de 2")

    st.markdown("### Tipos e valores ausentes por coluna")
    nulos = df.isna().sum()
    info = pd.DataFrame({
        "coluna": df.columns,
        "tipo": [str(t) for t in df.dtypes],
        "nulos": [int(nulos[c]) for c in df.columns],
        "% nulos": [round(100 * int(nulos[c]) / n_linhas, 1) for c in df.columns],
        "valores distintos": [int(df[c].nunique()) for c in df.columns],
    })
    st.dataframe(info)

    st.markdown("### Decisão sobre valores ausentes")
    texto_ou_aviso(DECISAO_SOBRE_NULOS, "A decisão sobre nulos")

    st.markdown("### Primeiras linhas")
    st.dataframe(df.head(10))


# =============================================================================
# MÓDULO 2 — DESCRITIVA INTERATIVA
# =============================================================================

def modulo_2_descritiva(df):
    st.header("Módulo 2 — Estatística descritiva")
    tipo = st.radio("Tipo de variável:", ["Numérica", "Categórica"], horizontal=True)

    if tipo == "Numérica":
        col = st.selectbox("Escolha a variável numérica:", colunas_numericas(df))
        dados = lista_limpa(df, col)          # <- fronteira da regra de ouro
        if len(dados) < 2:
            st.warning("Variável com menos de 2 valores válidos.")
            return

        # ---- medidas: TODAS vindas de minhastats ----
        med, mdn, dp = ms.media(dados), ms.mediana(dados), ms.desvio_padrao(dados)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Média", f"{med:.2f}")
        c2.metric("Mediana", f"{mdn:.2f}")
        c3.metric("Desvio padrão (amostral)", f"{dp:.2f}")
        c4.metric("Variância (amostral)", f"{ms.variancia(dados):.2f}")

        q1, q2, q3 = ms.quartis(dados)
        modas = ms.moda(dados)
        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Mínimo / Máximo", f"{min(dados):.2f} / {max(dados):.2f}")
        c6.metric("Amplitude", f"{ms.amplitude(dados):.2f}")
        c7.metric("Q1 / Q3", f"{q1:.2f} / {q3:.2f}")
        c8.metric("Coef. de variação", f"{ms.coeficiente_variacao(dados):.1f} %")
        st.caption(f"Moda(s): {modas[:5]}{' ...' if len(modas) > 5 else ''}  ·  n = {len(dados)}")

        # ---- interpretação automática ----
        st.info("📖 " + ms.interpretar_assimetria(dados))

        # ---- gráficos ----
        k = ms.numero_classes_sturges(len(dados))
        li, ls, outliers = ms.outliers_iqr(dados)

        fig, (ax1, ax2) = nova_figura(12, 4, colunas=2)
        ax1.hist(dados, bins=k, color="#7b3fd8", edgecolor="white")
        ax1.axvline(med, color="orange", linewidth=2, label=f"média = {med:.1f}")
        ax1.axvline(mdn, color="green", linewidth=2, linestyle="--", label=f"mediana = {mdn:.1f}")
        ax1.set_title(f"Histograma ({k} classes pela regra de Sturges)")
        ax1.set_xlabel(col)
        ax1.legend()

        ax2.boxplot(dados, widths=0.5)
        ax2.axhline(ls, color="red", linestyle=":", label=f"Q3 + 1,5·IQR = {ls:.1f}")
        ax2.axhline(li, color="red", linestyle=":", label=f"Q1 − 1,5·IQR = {li:.1f}")
        ax2.set_title(f"Boxplot — {len(outliers)} outlier(s) pela regra do IQR")
        ax2.set_ylabel(col)
        ax2.set_xticks([])
        ax2.legend(fontsize=8)
        mostrar(fig)

        # ---- tabela de frequências ----
        st.markdown(f"### Tabela de frequências — {k} classes (Sturges: k = 1 + 3,322·log10({len(dados)}))")
        tabela = pd.DataFrame(ms.tabela_frequencias(dados, k))
        tabela["freq_relativa"] = (tabela["freq_relativa"] * 100).round(2)
        tabela = tabela.rename(columns={"freq_relativa": "freq. relativa (%)"})
        st.dataframe(tabela[["classe", "frequencia", "freq. relativa (%)", "freq_acumulada"]],
                     use_container_width=True)

        if outliers:
            st.markdown(f"**Outliers ({len(outliers)}):** valores fora de [{li:.2f}, {ls:.2f}]")
            st.write(sorted(outliers)[:30], "..." if len(outliers) > 30 else "")

    else:
        col = st.selectbox("Escolha a variável categórica:", colunas_categoricas(df))
        valores = [str(v) for v in lista_limpa(df, col)]
        if not valores:
            st.warning("Variável sem valores válidos.")
            return
        contagens = ms.contar_frequencias(valores)
        n = len(valores)
        ordenado = sorted(contagens.items(), key=lambda par: par[1], reverse=True)

        st.metric("Moda (categoria mais frequente)", ", ".join(ms.moda(valores)[:3]))
        tabela = pd.DataFrame({
            "categoria": [c for c, _ in ordenado],
            "frequência": [f for _, f in ordenado],
            "freq. relativa (%)": [round(100 * f / n, 2) for _, f in ordenado],
        })
        st.dataframe(tabela)

        top = ordenado[:15]
        fig, ax = nova_figura(10, 4)
        if len(ordenado) <= 6:
            ax.pie([f for _, f in top], labels=[c for c, _ in top], autopct="%1.1f%%")
            ax.set_title(f"Distribuição de {col}")
        else:
            ax.bar([c for c, _ in top], [f for _, f in top], color="#7b3fd8")
            ax.set_title(f"Frequências de {col} (15 mais comuns)")
            ax.tick_params(axis="x", rotation=45)
        mostrar(fig)


# =============================================================================
# MÓDULO 3 — SIMULAÇÃO (LGN e TCL)
# =============================================================================

def modulo_3_simulacao(df):
    st.header("Módulo 3 — Simulação: Lei dos Grandes Números e Teorema Central do Limite")

    # ------------------------ Lei dos Grandes Números ------------------------
    st.subheader("3.1 Lei dos Grandes Números")
    experimento = st.selectbox("Experimento:", ["Moeda honesta (sair cara)", "Dado honesto (sair 6)"])
    p_teorica = 0.5 if experimento.startswith("Moeda") else 1 / 6
    n = st.slider("Número de lançamentos (n):", 10, 20000, 2000, step=10)
    st.button("🎲 Simular de novo")   # qualquer clique re-executa a simulação

    sucessos_acumulados = 0
    frequencias = []
    for i in range(1, n + 1):
        if random.random() < p_teorica:
            sucessos_acumulados += 1
        frequencias.append(sucessos_acumulados / i)

    fig, ax = nova_figura(10, 4)
    ax.plot(range(1, n + 1), frequencias, color="#7b3fd8", linewidth=1)
    ax.axhline(p_teorica, color="red", linestyle="--", label=f"probabilidade teórica = {p_teorica:.3f}")
    ax.set_xscale("log")
    ax.set_xlabel("nº de lançamentos (escala log)")
    ax.set_ylabel("frequência relativa acumulada")
    ax.set_title("A frequência relativa CONVERGE para a probabilidade")
    ax.legend()
    mostrar(fig)
    st.caption(f"Após {n} lançamentos a frequência relativa foi {frequencias[-1]:.4f} "
               f"(teórica: {p_teorica:.4f}). Clique em 'Simular de novo': o início muda, o fim não.")

    # --------------------- Teorema Central do Limite -------------------------
    st.subheader("3.2 Teorema Central do Limite — sobre os SEUS dados")
    col = st.selectbox("Escolha uma variável (quanto mais assimétrica, melhor o show):",
                       colunas_numericas(df), key="tcl_col")
    dados = lista_limpa(df, col)
    if len(dados) < 30:
        st.warning("Variável com poucos valores válidos.")
        return

    c1, c2 = st.columns(2)
    tamanho = c1.slider("Tamanho de cada amostra (n):", 2, min(100, len(dados)), 30)
    repeticoes = c2.slider("Número de amostras sorteadas:", 100, 5000, 1000, step=100)

    medias = [ms.media(random.sample(dados, tamanho)) for _ in range(repeticoes)]

    mu_dados, sigma_dados = ms.media(dados), ms.desvio_padrao(dados)
    mu_medias, sigma_medias = ms.media(medias), ms.desvio_padrao(medias)

    fig, (ax1, ax2) = nova_figura(12, 4, colunas=2)
    ax1.hist(dados, bins=ms.numero_classes_sturges(len(dados)), density=True,
             color="#b39ddb", edgecolor="white")
    ax1.set_title(f"Dados originais: {col}")
    ax1.set_xlabel(col)

    ax2.hist(medias, bins=ms.numero_classes_sturges(len(medias)), density=True,
             color="#7b3fd8", edgecolor="white", label="médias das amostras")
    passo = (max(medias) - min(medias)) / 200 or 1e-9
    xs = [min(medias) + i * passo for i in range(201)]
    ax2.plot(xs, [ms.densidade_normal(x, mu_medias, sigma_medias) for x in xs],
             color="orange", linewidth=2, label="Normal(μ̂, σ̂)")
    ax2.set_title(f"Médias de {repeticoes} amostras com n = {tamanho}")
    ax2.set_xlabel(f"média de {col}")
    ax2.legend()
    mostrar(fig)

    c1, c2, c3 = st.columns(3)
    c1.metric("Média dos dados", f"{mu_dados:.2f}", f"média das médias = {mu_medias:.2f}")
    c2.metric("Desvio dos dados / √n", f"{sigma_dados / tamanho ** 0.5:.2f}",
              f"desvio das médias = {sigma_medias:.2f}")
    c3.metric("Interpretação", ms.interpretar_assimetria(medias).split(":")[0].split(".")[0])
    st.caption("O TCL prevê: média das médias ≈ média dos dados e desvio das médias ≈ desvio/√n.")
    texto_ou_aviso(TEXTO_LEITURA_TCL, "A leitura do TCL (TODO 15)")


# =============================================================================
# MÓDULO 4 — DISTRIBUIÇÕES TEÓRICAS SOBRE OS DADOS
# =============================================================================

def modulo_4_distribuicoes(df):
    st.header("Módulo 4 — Sobrepor a teoria aos dados")
    col = st.selectbox("Variável:", colunas_numericas(df), key="dist_col")
    dados = lista_limpa(df, col)
    if len(dados) < 2:
        st.warning("Variável com poucos valores válidos.")
        return

    distribuicao = st.selectbox("Distribuição teórica:",
                                ["Normal", "Exponencial", "Uniforme", "Poisson (só para contagens)"])

    # parâmetros estimados com as SUAS funções
    mu, sigma = ms.media(dados), ms.desvio_padrao(dados)
    minimo, maximo = min(dados), max(dados)
    k = ms.numero_classes_sturges(len(dados))

    fig, ax = nova_figura(10, 4.5)
    ax.hist(dados, bins=k, density=True, color="#b39ddb", edgecolor="white", label="dados (density=True)")
    passo = (maximo - minimo) / 300 or 1e-9
    xs = [minimo + i * passo for i in range(301)]

    if distribuicao == "Normal":
        ax.plot(xs, [ms.densidade_normal(x, mu, sigma) for x in xs], color="red", linewidth=2,
                label=f"Normal(μ = {mu:.2f}, σ = {sigma:.2f})")
        st.markdown(f"**Parâmetros estimados dos dados:** μ = média = {mu:.3f}, σ = desvio = {sigma:.3f}")
    elif distribuicao == "Exponencial":
        if mu <= 0:
            st.warning("A Exponencial exige valores positivos.")
            mostrar(fig)
            return
        lam = 1 / mu
        ax.plot(xs, [ms.densidade_exponencial(x, lam) for x in xs], color="red", linewidth=2,
                label=f"Exponencial(λ = 1/média = {lam:.4f})")
        st.markdown(f"**Parâmetro estimado:** λ = 1/média = {lam:.4f}")
    elif distribuicao == "Uniforme":
        ax.plot(xs, [ms.densidade_uniforme(x, minimo, maximo) for x in xs], color="red", linewidth=2,
                label=f"Uniforme({minimo:.2f}, {maximo:.2f})")
        st.markdown(f"**Parâmetros estimados:** mín = {minimo:.3f}, máx = {maximo:.3f}")
    else:
        if any(x < 0 or x != int(x) for x in dados):
            st.warning("A Poisson só serve para CONTAGENS (inteiros ≥ 0). Escolha outra variável ou distribuição.")
            mostrar(fig)
            return
        if mu <= 0:
            st.warning("λ = média deve ser > 0.")
            mostrar(fig)
            return
        ks = list(range(int(minimo), int(maximo) + 1))
        ax.plot(ks, [ms.massa_poisson(kk, mu) for kk in ks], "o-", color="red", label=f"Poisson(λ = {mu:.2f})")
        st.markdown(f"**Parâmetro estimado:** λ = média = {mu:.3f}")

    ax.set_title(f"{col}: histograma (density=True) + {distribuicao.split(' ')[0]} estimada dos dados")
    ax.set_xlabel(col)
    ax.legend()
    mostrar(fig)

    st.info("📖 Leitura automática dos dados: " + ms.interpretar_assimetria(dados))
    st.markdown("### Discussão da equipe (o ajuste ruim BEM DISCUTIDO vale nota)")
    texto_ou_aviso(TEXTO_DISCUSSAO_DISTRIBUICAO, "A discussão do ajuste (TODO 16)")


# =============================================================================
# MÓDULO 5 — CORRELAÇÃO E REGRESSÃO
# =============================================================================

def modulo_5_regressao(df):
    st.header("Módulo 5 — Correlação e regressão linear")
    numericas = colunas_numericas(df)
    c1, c2 = st.columns(2)
    col_x = c1.selectbox("Variável explicativa X:", numericas, index=0)
    col_y = c2.selectbox("Variável resposta Y:", numericas, index=min(1, len(numericas) - 1))
    if col_x == col_y:
        st.warning("Escolha duas variáveis diferentes.")
        return

    pares = df[[col_x, col_y]].dropna()          # Pandas só limpa
    x, y = pares[col_x].tolist(), pares[col_y].tolist()   # fronteira da regra de ouro
    if len(x) < 3:
        st.warning("Poucos pares válidos.")
        return

    r = ms.correlacao(x, y)
    b0, b1, r2 = ms.regressao_linear(x, y)

    c1, c2, c3 = st.columns(3)
    c1.metric("Correlação de Pearson (r)", f"{r:.4f}")
    c2.metric("R² (variação de Y explicada por X)", f"{r2:.4f}")
    c3.metric("Equação da reta", f"ŷ = {b0:.3f} + {b1:.3f}·x")

    fig, ax = nova_figura(10, 5)
    ax.scatter(x, y, s=12, alpha=0.5, color="#7b3fd8", label="dados")
    xmin, xmax = min(x), max(x)
    ax.plot([xmin, xmax], [b0 + b1 * xmin, b0 + b1 * xmax], color="orange", linewidth=2.5,
            label=f"ŷ = {b0:.2f} + {b1:.2f}·x   (R² = {r2:.3f})")
    ax.set_xlabel(col_x)
    ax.set_ylabel(col_y)
    ax.set_title("Mínimos quadrados: a reta que minimiza a soma dos resíduos²")
    ax.legend()
    mostrar(fig)

    # ---- interpretação obrigatória (estrutura do guia) ----
    direcao = "a mais" if b1 >= 0 else "a menos"
    forca = ("forte" if abs(r) >= 0.7 else "moderada" if abs(r) >= 0.4 else "fraca" if abs(r) >= 0.2 else "praticamente nula")
    st.info(
        f"📖 **Interpretação:** cada unidade a mais de **{col_x}** está *associada*, em média, a "
        f"**{abs(b1):.3f} unidades {direcao}** de **{col_y}**. A correlação é {forca} "
        f"(r = {r:.2f}) e a reta explica {100 * r2:.1f}% da variação de {col_y}."
    )
    st.error("⚠️ **Correlação NÃO implica causalidade.** Associação estatística não diz quem causa quem "
             "— pode haver uma terceira variável por trás das duas.")
    texto_ou_aviso(EXEMPLO_CAUSALIDADE_DUVIDOSA, "O exemplo de causalidade duvidosa (TODO 17)")

    # ---- predição limitada ao intervalo observado ----
    st.markdown("### Predição")
    st.caption(f"A reta só foi validada dentro de [{xmin:.2f}, {xmax:.2f}]. Fora disso é extrapolação — chute vestido de matemática.")
    x_novo = st.number_input(f"Valor de {col_x}:", value=float(ms.media(x)), step=(xmax - xmin) / 100 or 1.0)
    y_prev = b0 + b1 * x_novo
    if x_novo < xmin or x_novo > xmax:
        st.warning(f"⚠️ {x_novo:.2f} está FORA do intervalo observado [{xmin:.2f}, {xmax:.2f}]. "
                   f"A previsão ŷ = {y_prev:.3f} é uma extrapolação e não é confiável.")
    else:
        st.success(f"Para {col_x} = {x_novo:.2f}, a reta prevê {col_y} ≈ **{y_prev:.3f}**")


# =============================================================================
# MÓDULO 6 — AS TRÊS DESCOBERTAS
# =============================================================================

def evidencia_contraste(df, desc):
    cat, num = desc["categorica"], desc["numerica"]
    sub = df[[cat, num]].dropna()
    grupos = ms.contar_frequencias([str(v) for v in sub[cat]])
    maiores = [g for g, _ in sorted(grupos.items(), key=lambda par: par[1], reverse=True)[:10]]

    linhas, caixas = [], []
    for grupo in maiores:
        valores = sub[sub[cat].astype(str) == grupo][num].tolist()   # fronteira
        if len(valores) < 2:
            continue
        linhas.append({cat: grupo, "n": len(valores), "média": round(ms.media(valores), 3),
                       "mediana": round(ms.mediana(valores), 3), "desvio": round(ms.desvio_padrao(valores), 3)})
        caixas.append((grupo, valores))
    st.dataframe(pd.DataFrame(linhas))

    fig, ax = nova_figura(10, 4.5)
    ax.boxplot([v for _, v in caixas])
    ax.set_xticks(range(1, len(caixas) + 1))
    ax.set_xticklabels([g for g, _ in caixas])
    ax.set_ylabel(num)
    ax.set_title(f"{num} por {cat} (até 10 grupos mais frequentes)")
    ax.tick_params(axis="x", rotation=30)
    mostrar(fig)


def evidencia_correlacao(df, desc):
    cx, cy = desc["x"], desc["y"]
    pares = df[[cx, cy]].dropna()
    x, y = pares[cx].tolist(), pares[cy].tolist()
    r = ms.correlacao(x, y)
    b0, b1, r2 = ms.regressao_linear(x, y)
    c1, c2 = st.columns(2)
    c1.metric("r de Pearson", f"{r:.4f}")
    c2.metric("R²", f"{r2:.4f}")
    fig, ax = nova_figura(10, 4.5)
    ax.scatter(x, y, s=10, alpha=0.5, color="#7b3fd8")
    ax.plot([min(x), max(x)], [b0 + b1 * min(x), b0 + b1 * max(x)], color="orange", linewidth=2)
    ax.set_xlabel(cx)
    ax.set_ylabel(cy)
    mostrar(fig)


def evidencia_outliers(df, desc):
    num = desc["numerica"]
    dados = lista_limpa(df, num)
    li, ls, outliers = ms.outliers_iqr(dados)
    st.metric(f"Outliers em {num} (regra do IQR)", len(outliers), f"fora de [{li:.2f}, {ls:.2f}]")
    mascara = (df[num] < li) | (df[num] > ls)
    st.markdown("**Quem são eles (até 20 linhas):**")
    st.dataframe(df[mascara].head(20))


def modulo_6_descobertas(df):
    st.header("Módulo 6 — As três descobertas")
    st.caption("Cada descoberta: afirmação em uma frase + evidência gerada pela aplicação + limite honesto.")
    geradores = {"contraste": evidencia_contraste, "correlacao": evidencia_correlacao, "outliers": evidencia_outliers}

    for i, desc in enumerate(DESCOBERTAS, start=1):
        st.markdown(f"## Descoberta {i}: {desc.get('titulo', '')}")
        if eh_todo(desc.get("titulo", "TODO")):
            st.warning(f"✏️ Descoberta {i} ainda não foi preenchida (TODO {17 + i} em app.py).")
            continue
        st.markdown(f"**Afirmação:** {desc.get('afirmacao', '')}")
        colunas_usadas = [desc.get(chave) for chave in ("categorica", "numerica", "x", "y") if desc.get(chave)]
        faltando = [c for c in colunas_usadas if c not in df.columns]
        if faltando:
            st.error(f"Coluna(s) não encontrada(s) no dataset: {faltando}. Confira o nome exato no CSV.")
            continue
        try:
            geradores[desc["tipo"]](df, desc)
        except (NotImplementedError, ValueError) as erro:
            st.error(f"Não foi possível gerar a evidência: {erro}")
        st.markdown(f"**Limite honesto:** {desc.get('limite', '')}")
        st.divider()


# =============================================================================
# NAVEGAÇÃO
# =============================================================================

def main():
    st.title("📊 Laboratório Estatístico Interativo")
    st.caption(f"Equipe: {NOME_EQUIPE}  ·  Toda medida exibida é calculada por minhastats.py (núcleo próprio).")

    try:
        df = carregar_dados(CAMINHO_DATASET, SEPARADOR_CSV, SEPARADOR_DECIMAL,
                            tuple(COLUNAS_PARA_CONVERTER_EM_NUMERO))
    except FileNotFoundError:
        st.error(f"Não encontrei o arquivo **{CAMINHO_DATASET}**.")
        st.info("Coloque o CSV do dataset na pasta `dados/` com o nome `dataset.csv`, "
                "ou ajuste CAMINHO_DATASET no TODO 13 de app.py. Para testar o app antes de "
                "escolher um dataset real, rode:  python dados/gerar_dataset_exemplo.py")
        st.stop()

    modulos = {
        "Módulo 0 — Dataset": modulo_0_dataset,
        "Módulo 2 — Descritiva": modulo_2_descritiva,
        "Módulo 3 — Simulação (LGN e TCL)": modulo_3_simulacao,
        "Módulo 4 — Distribuições": modulo_4_distribuicoes,
        "Módulo 5 — Correlação e regressão": modulo_5_regressao,
        "Módulo 6 — Descobertas": modulo_6_descobertas,
    }
    escolha = st.sidebar.radio("Navegue pelos módulos:", list(modulos.keys()))
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Módulo 1** é o núcleo `minhastats.py` — ele não tem tela, "
                        "mas é ele que calcula tudo o que você vê aqui. Prova: `pytest -v`.")
    rodar_modulo(modulos[escolha], df)


main()
