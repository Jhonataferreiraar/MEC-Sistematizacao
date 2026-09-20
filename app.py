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
NOME_EQUIPE = "MEC-Sistematizacao"
CAMINHO_DATASET = "dados/dataset.csv"
SEPARADOR_CSV = ","
SEPARADOR_DECIMAL = "."
COLUNAS_PARA_CONVERTER_EM_NUMERO = []

# ---- TODO 14: sobre o dataset (aparece no Módulo 0) --------------------------
NOME_DATASET = "Video Game Sales"
FONTE_DATASET = (
    "https://www.kaggle.com/datasets/gregorut/videogamesales"
)
POR_QUE_ESCOLHEMOS = (
    "Escolhemos o dataset Video Game Sales porque ele permite investigar "
    "como as vendas de jogos variam entre gêneros e plataformas. Também "
    "podemos analisar a relação entre as vendas em diferentes regiões e "
    "identificar jogos com vendas muito acima do padrão."
)
DECISAO_SOBRE_NULOS = (
    "O dataset possui 271 valores ausentes em Year e 58 em Publisher. "
    "Mantivemos os registros e usamos apenas os valores válidos da variável "
    "analisada. Em análises com duas variáveis, removemos somente os pares "
    "que possuem algum valor ausente."
)

# ---- TODO 15: leitura do Teorema Central do Limite (Módulo 3) ----------------
TEXTO_LEITURA_TCL = (
    "Quando o tamanho das amostras aumenta, o histograma das médias "
    "amostrais fica mais concentrado e mais parecido com uma distribuição "
    "Normal. A média das médias se aproxima da média dos dados, enquanto "
    "o desvio das médias diminui aproximadamente na proporção de 1 sobre "
    "a raiz quadrada do tamanho da amostra."
)

# ---- TODO 16: discussão do ajuste das distribuições (Módulo 4) ---------------
TEXTO_DISCUSSAO_DISTRIBUICAO = (
    "A variável Global_Sales apresenta forte assimetria à direita, pois "
    "a maioria dos jogos possui vendas relativamente baixas e poucos jogos "
    "possuem vendas muito altas. Por isso, a distribuição Normal tende a "
    "não representar bem a cauda direita. A distribuição Exponencial é "
    "uma candidata mais coerente para representar a concentração de valores "
    "baixos, embora também possa não representar perfeitamente os grandes "
    "sucessos."
)

# ---- TODO 17: exemplo de causalidade duvidosa (Módulo 5) --------------------
EXEMPLO_CAUSALIDADE_DUVIDOSA = (
    "NA_Sales e EU_Sales podem apresentar associação positiva, mas isso não "
    "significa que as vendas na América do Norte causem as vendas na Europa. "
    "A popularidade do jogo, o investimento em marketing, a plataforma e "
    "o gênero podem influenciar as duas variáveis."
)

# ---- TODO 18, 19 e 20: AS TRÊS DESCOBERTAS (Módulo 6) -----------------------
# Cada descoberta tem um "tipo" que diz ao app qual gráfico gerar:
#   "contraste"  -> uma CATEGÓRICA particionando uma NUMÉRICA (boxplots por grupo)
#   "correlacao" -> duas NUMÉRICAS (dispersão + r + reta)
#   "outliers"   -> uma NUMÉRICA (quem são os pontos fora da curva)
# Troque os nomes das colunas pelos do SEU dataset (exatamente como no CSV).
DESCOBERTAS = [
    {
        "titulo": "Diferenças de vendas entre gêneros",
        "tipo": "contraste",
        "categorica": "Genre",
        "numerica": "Global_Sales",
        "afirmacao": (
            "As vendas globais apresentam diferenças entre os gêneros. "
            "A tabela e o boxplot mostram qual gênero possui a maior mediana."
        ),
        "limite": (
            "A comparação mostra associação entre gênero e vendas neste "
            "dataset, mas não prova que o gênero cause maiores vendas."
        ),
    },
    {
        "titulo": "Associação entre vendas norte-americanas e europeias",
        "tipo": "correlacao",
        "x": "NA_Sales",
        "y": "EU_Sales",
        "afirmacao": (
            "As vendas na América do Norte e na Europa apresentam associação "
            "positiva, observada pelo gráfico de dispersão e pelo valor de r."
        ),
        "limite": (
            "A correlação não implica causalidade e pode ser influenciada "
            "pela popularidade, plataforma, gênero ou período de lançamento."
        ),
    },
    {
        "titulo": "Jogos com vendas globais fora do padrão",
        "tipo": "outliers",
        "numerica": "Global_Sales",
        "afirmacao": (
            "A regra do IQR identifica jogos com vendas globais muito acima "
            "do padrão observado no restante do dataset."
        ),
        "limite": (
            "Um outlier é um valor estatisticamente distante, mas isso não "
            "significa que o registro seja um erro ou que represente todos "
            "os jogos."
        ),
    },
]

# =============================================================================
#      DAQUI PARA BAIXO NÃO PRECISA MEXER (mas leia — cai na arguição!)
# =============================================================================

st.set_page_config(
    page_title="Laboratório Estatístico Interativo",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)


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


def titulo_modulo(titulo, icone, apoio):
    """Apresenta o título e a finalidade de cada módulo com o mesmo padrão visual."""
    st.header(titulo, icon=icone)
    st.caption(apoio)


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
    titulo_modulo(
        "Módulo 0 — O dataset",
        ":material/database:",
        "Conheça a fonte, o tamanho e a qualidade dos dados usados no laboratório.",
    )
    st.subheader(NOME_DATASET)
    st.markdown(f"**Fonte original:** {FONTE_DATASET}")
    texto_ou_aviso(POR_QUE_ESCOLHEMOS, "A justificativa da escolha")

    n_linhas, n_colunas = df.shape
    num = colunas_numericas(df)
    cat = colunas_categoricas(df)

    with st.container(border=True):
        st.markdown("#### O contrato do guia")
        st.caption("Pelo menos 1.000 registros, 4 variáveis numéricas e 2 categóricas.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Registros", n_linhas, "✅" if n_linhas >= 1000 else "❌ menos de 1000")
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
    titulo_modulo(
        "Módulo 2 — Estatística descritiva",
        ":material/bar_chart:",
        "Explore medidas de posição, dispersão, frequências, gráficos e outliers.",
    )
    tipo = st.segmented_control(
        "Tipo de variável",
        ["Numérica", "Categórica"],
        default="Numérica",
        key="tipo_variavel",
    ) or "Numérica"

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
        ax1.hist(dados, bins=k, color="#0F5AA6", edgecolor="white")
        ax1.axvline(med, color="#F59E0B", linewidth=2, label=f"média = {med:.1f}")
        ax1.axvline(mdn, color="#2E8B57", linewidth=2, linestyle="--", label=f"mediana = {mdn:.1f}")
        ax1.set_title(f"Histograma ({k} classes pela regra de Sturges)")
        ax1.set_xlabel(col)
        ax1.legend()

        ax2.boxplot(dados, widths=0.5)
        ax2.axhline(ls, color="#D94B4B", linestyle=":", label=f"Q3 + 1,5·IQR = {ls:.1f}")
        ax2.axhline(li, color="#D94B4B", linestyle=":", label=f"Q1 − 1,5·IQR = {li:.1f}")
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
                     width="stretch")

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
            ax.bar([c for c, _ in top], [f for _, f in top], color="#0F5AA6")
            ax.set_title(f"Frequências de {col} (15 mais comuns)")
            ax.tick_params(axis="x", rotation=45)
        mostrar(fig)


# =============================================================================
# MÓDULO 3 — SIMULAÇÃO (LGN e TCL)
# =============================================================================

def modulo_3_simulacao(df):
    titulo_modulo(
        "Módulo 3 — Simulação",
        ":material/casino:",
        "Veja a Lei dos Grandes Números e o Teorema Central do Limite acontecendo.",
    )

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
    ax.plot(range(1, n + 1), frequencias, color="#0F5AA6", linewidth=1)
    ax.axhline(p_teorica, color="#D94B4B", linestyle="--", label=f"probabilidade teórica = {p_teorica:.3f}")
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
             color="#A8C6E8", edgecolor="white")
    ax1.set_title(f"Dados originais: {col}")
    ax1.set_xlabel(col)

    ax2.hist(medias, bins=ms.numero_classes_sturges(len(medias)), density=True,
             color="#0F5AA6", edgecolor="white", label="médias das amostras")
    passo = (max(medias) - min(medias)) / 200 or 1e-9
    xs = [min(medias) + i * passo for i in range(201)]
    ax2.plot(xs, [ms.densidade_normal(x, mu_medias, sigma_medias) for x in xs],
             color="#F59E0B", linewidth=2, label="Normal(μ̂, σ̂)")
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
    titulo_modulo(
        "Módulo 4 — Distribuições teóricas",
        ":material/timeline:",
        "Compare os dados reais com curvas teóricas e discuta a qualidade do ajuste.",
    )
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
    ax.hist(dados, bins=k, density=True, color="#A8C6E8", edgecolor="white", label="dados (density=True)")
    passo = (maximo - minimo) / 300 or 1e-9
    xs = [minimo + i * passo for i in range(301)]

    if distribuicao == "Normal":
        ax.plot(xs, [ms.densidade_normal(x, mu, sigma) for x in xs], color="#D94B4B", linewidth=2,
                label=f"Normal(μ = {mu:.2f}, σ = {sigma:.2f})")
        st.markdown(f"**Parâmetros estimados dos dados:** μ = média = {mu:.3f}, σ = desvio = {sigma:.3f}")
    elif distribuicao == "Exponencial":
        if mu <= 0:
            st.warning("A Exponencial exige valores positivos.")
            mostrar(fig)
            return
        lam = 1 / mu
        ax.plot(xs, [ms.densidade_exponencial(x, lam) for x in xs], color="#D94B4B", linewidth=2,
                label=f"Exponencial(λ = 1/média = {lam:.4f})")
        st.markdown(f"**Parâmetro estimado:** λ = 1/média = {lam:.4f}")
    elif distribuicao == "Uniforme":
        ax.plot(xs, [ms.densidade_uniforme(x, minimo, maximo) for x in xs], color="#D94B4B", linewidth=2,
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
        ax.plot(ks, [ms.massa_poisson(kk, mu) for kk in ks], "o-", color="#D94B4B", label=f"Poisson(λ = {mu:.2f})")
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
    titulo_modulo(
        "Módulo 5 — Correlação e regressão linear",
        ":material/show_chart:",
        "Investigue relações entre variáveis, ajuste uma reta e faça uma predição.",
    )
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
    ax.scatter(x, y, s=12, alpha=0.5, color="#0F5AA6", label="dados")
    xmin, xmax = min(x), max(x)
    ax.plot([xmin, xmax], [b0 + b1 * xmin, b0 + b1 * xmax], color="#F59E0B", linewidth=2.5,
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
    ax.scatter(x, y, s=10, alpha=0.5, color="#0F5AA6")
    ax.plot([min(x), max(x)], [b0 + b1 * min(x), b0 + b1 * max(x)], color="#F59E0B", linewidth=2)
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
    titulo_modulo(
        "Módulo 6 — As três descobertas",
        ":material/lightbulb:",
        "Afirmação, evidência gerada pela aplicação e limite honesto.",
    )
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
        st.space("small")


# =============================================================================
# NAVEGAÇÃO
# =============================================================================

def main():
    st.title("Laboratório Estatístico Interativo", icon=":material/analytics:")
    st.caption(f"{NOME_EQUIPE}  ·  Medidas calculadas pelo núcleo próprio `minhastats.py`.")

    with st.container(border=True):
        c1, c2 = st.columns([3, 1], vertical_alignment="center")
        with c1:
            st.markdown("#### Dados reais, fórmulas próprias e descobertas")
            st.write(
                "Navegue pelos módulos para entender o dataset, testar simulações "
                "e encontrar padrões nas vendas de jogos."
            )
        with c2:
            st.metric("Registros", "16.598", "Video Game Sales")

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
    with st.sidebar:
        st.markdown("## Laboratório")
        st.caption("MEC-Sistematizacao")
        st.markdown("#### Navegação")
        escolha = st.radio("Escolha um módulo", list(modulos.keys()), label_visibility="collapsed")
        st.space("small")
        st.markdown(
            "**Módulo 1** é o núcleo `minhastats.py`. Ele não tem tela: "
            "é ele que calcula os resultados exibidos aqui."
        )
        st.caption(":material/check_circle: 40 testes validados com pytest")
    rodar_modulo(modulos[escolha], df)


main()
