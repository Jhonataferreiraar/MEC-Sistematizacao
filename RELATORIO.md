# Relatório — Laboratório Estatístico Interativo

**Equipe:** MEC-Sistematizacao
**Componente:** Jhonata Ferreira de Araujo — 72650246
**Repositório:** https://github.com/Jhonataferreiraar/MEC-Sistematizacao
**Fonte do dataset:** https://www.kaggle.com/datasets/gregorut/videogamesales
**Vídeo:** https://youtu.be/zXUieqC58bc

## Resumo executivo

Este projeto desenvolveu um Laboratório Estatístico Interativo utilizando o dataset Video Game Sales, disponibilizado publicamente no Kaggle. O conjunto possui 16.598 registros e informações sobre vendas de jogos em diferentes regiões, além de variáveis como gênero, plataforma e publicadora.

A aplicação apresenta estatística descritiva, simulações da Lei dos Grandes Números e do Teorema Central do Limite, comparação com distribuições teóricas, correlação, regressão linear e descobertas sobre os dados. O núcleo estatístico foi implementado no arquivo minhastats.py e validado por testes comparativos com NumPy e SciPy.

As três principais descobertas foram: a existência de diferenças nas vendas globais entre gêneros; a associação positiva entre vendas na América do Norte e na Europa; e a existência de jogos com vendas globais muito acima do padrão identificado pela regra do IQR. Essas descobertas mostram associações presentes nos dados, mas não permitem afirmar relações de causa e efeito.

## 1. Dataset e justificativa

- **Nome:** Video Game Sales
- **Fonte original:** https://www.kaggle.com/datasets/gregorut/videogamesales
- **Tamanho:** 16.598 linhas × 11 colunas
- **Variáveis numéricas usadas:** `Rank`, `Year`, `NA_Sales`, `EU_Sales`, `JP_Sales`, `Other_Sales`, `Global_Sales`
- **Variáveis categóricas usadas:** `Name`, `Platform`, `Genre`, `Publisher`

O dataset atende aos requisitos mínimos da atividade, pois possui mais de 1.000 registros, sete variáveis numéricas e quatro variáveis categóricas. Ele foi escolhido porque permite analisar as vendas de jogos em diferentes regiões, comparar gêneros e plataformas, investigar relações entre mercados e identificar jogos com vendas muito acima do padrão.

## 2. Decisões de tratamento dos dados

- **Valores ausentes:** Existem 271 valores ausentes em `Year` e 58 em `Publisher`. A análise mantém o dataset e utiliza somente os valores válidos da variável selecionada. Em análises com duas variáveis, são removidos somente os pares que possuem algum valor ausente.
- **Texto onde deveria haver número:** Nenhuma coluna numérica precisou ser convertida, pois as colunas numéricas foram reconhecidas corretamente.
- **Outras decisões:** Para as comparações categóricas, foram priorizadas as colunas `Genre` e `Platform`, pois `Name` possui muitos valores distintos e não formaria grupos úteis para a comparação.
- **Regra de ouro:** O Pandas é utilizado para carregar e organizar os dados. Depois da conversão para listas, as medidas estatísticas exibidas são calculadas pelas funções próprias de `minhastats.py`.

## 3. Fórmulas do núcleo (`minhastats.py`)

| Função | Fórmula | Observação |
|--------|---------|------------|
| média | x̄ = (x₁ + x₂ + ... + xₙ) / n | Lista vazia gera erro |
| variância amostral | s² = Σ(xᵢ − x̄)² / (n − 1) | Usa n − 1 no denominador |
| variância populacional | σ² = Σ(xᵢ − μ)² / n | Usa n no denominador |
| desvio padrão amostral | s = √s² | Raiz quadrada da variância amostral |
| mediana | Dados ordenados; valor central ou média dos dois valores centrais | Lista vazia gera erro |
| moda | Valor ou valores com maior frequência | Pode haver mais de uma moda |
| amplitude | máximo − mínimo | Lista vazia gera erro |
| percentil | posição = p(n − 1) / 100 com interpolação linear | p deve estar entre 0 e 100 |
| quartis | Q1 = P25, Q2 = P50 e Q3 = P75 | Reutiliza o cálculo de percentil |
| coeficiente de variação | CV = (s / x̄) × 100% | Média zero gera erro |
| covariância | Σ[(xᵢ − x̄)(yᵢ − ȳ)] / (n − 1) | X e Y devem ter o mesmo tamanho |
| correlação de Pearson | r = cov(X,Y) / (sₓ · sᵧ) | Variável constante gera erro |
| regra de Sturges | k = ⌈1 + 3,322 log₁₀(n)⌉ | Estima o número de classes do histograma |
| outliers pelo IQR | limite inferior = Q1 − 1,5 × IQR; limite superior = Q3 + 1,5 × IQR | Valores fora dos limites são identificados |
| regressão linear | ŷ = b₀ + b₁x e R² = 1 − SQres/SQtot | X ou Y constante gera erro |

## 4. Tabela de validação

As funções foram comparadas com referências do NumPy e do SciPy. Os testes utilizam tolerância relativa de `1e-9` para as contas principais e `1e-6` para percentis, pois diferentes ordens de operações podem produzir pequenas diferenças nas últimas casas decimais.

| Função | Referência | Diferença observada | Tolerância | Passou? |
|--------|------------|---------------------|------------|---------|
| média | `np.mean` | Dentro da tolerância | `1e-9` relativa | Sim |
| variância amostral | `np.var(ddof=1)` | Dentro da tolerância | `1e-9` | Sim |
| variância populacional | `np.var(ddof=0)` | Dentro da tolerância | `1e-9` | Sim |
| desvio padrão | `np.std` | Dentro da tolerância | `1e-9` | Sim |
| mediana | `np.median` | Dentro da tolerância | `1e-9` | Sim |
| percentil | `np.percentile` | Dentro da tolerância | `1e-6` | Sim |
| covariância | `np.cov(ddof=1)` | Dentro da tolerância | `1e-9` | Sim |
| correlação | `np.corrcoef` | Dentro da tolerância | `1e-9` | Sim |
| regressão linear | `scipy.stats.linregress` | Dentro da tolerância | `1e-9` | Sim |

Além dessas funções, os testes também verificam moda, amplitude, quartis, coeficiente de variação, densidades teóricas, número de classes de Sturges, outliers pelo IQR, interpretações de assimetria e tratamento de entradas inválidas.

Saída do `pytest -v`:

```text
40 passed
```

## 5. Os módulos

### Módulo 0 — Dados reais

O Módulo 0 apresenta a estrutura do dataset utilizado. São 16.598 registros e 11 colunas, sendo sete numéricas e quatro categóricas. Existem 271 valores ausentes em `Year` e 58 em `Publisher`. As variáveis de vendas são adequadas para análises de distribuição, comparação entre grupos e correlação entre regiões.

![Módulo 0 — Dataset](<assets/screenshots/Módulo 0 - Dataset.png>)

### Módulo 2 — Estatística descritiva interativa

![Módulo 2 — Descritiva](<assets/screenshots/Módulo 2 - Descritiva (1).png>)

Foi analisada a variável numérica `Global_Sales`. A média foi 0,54, enquanto a mediana foi 0,17. Essa diferença mostra que a distribuição possui assimetria à direita: a maioria dos jogos apresenta vendas relativamente baixas, enquanto poucos jogos possuem vendas muito altas e puxam a média para cima.

O desvio padrão amostral foi 1,56, a variância amostral foi 2,42, o primeiro quartil foi 0,06 e o terceiro quartil foi 0,47. O coeficiente de variação foi aproximadamente 289,3%, indicando grande dispersão em relação à média. A moda foi 0,02.

![Módulo 2 — Frequências](<assets/screenshots/Módulo 2 - Descritiva (2).png>)

A regra do IQR identificou 1.893 outliers em `Global_Sales`, considerando como valores fora do intervalo aproximado de -0,55 a 1,08. Esses valores não são necessariamente erros; eles representam jogos com vendas muito superiores ao padrão da maior parte do dataset.

![Módulo 2 — Distribuição](<assets/screenshots/Módulo 2 - Descritiva (3).png>)

### Módulo 3 — Simulação: Lei dos Grandes Números e Teorema Central do Limite

![Módulo 3 — Lei dos Grandes Números](<assets/screenshots/Módulo 3 - Simulação (1).png>)

Na simulação da Lei dos Grandes Números, foram realizados 2.000 lançamentos de moeda. A frequência relativa observada foi 0,5070, próxima da probabilidade teórica de 0,5000. Isso mostra que, conforme o número de repetições aumenta, a frequência observada tende a se aproximar da probabilidade esperada.

![Módulo 3 — Teorema Central do Limite](<assets/screenshots/Módulo 3 - Simulação (2).png>)

No Teorema Central do Limite, foi utilizada a variável `Global_Sales`. Para amostras com n = 2, as médias apresentaram maior dispersão e conservaram parte da assimetria dos dados originais. Com n = 10, as médias ficaram mais concentradas. Com n = 30, a distribuição das médias ficou ainda mais concentrada e mais próxima de uma forma normal.

Esse comportamento está de acordo com o TCL: a média das médias se aproxima da média original e o desvio das médias diminui conforme o tamanho da amostra aumenta.

### Módulo 4 — Distribuições teóricas

![Módulo 4 — Distribuição Normal](<assets/screenshots/Módulo 4 - Distribuições (1).png>)

A distribuição Normal foi ajustada à variável `Global_Sales` utilizando média μ = 0,537 e desvio padrão σ = 1,555. O ajuste não foi adequado, porque os dados são fortemente assimétricos à direita. A maior parte dos jogos possui vendas baixas, mas existem poucos jogos com valores extremamente altos.

![Módulo 4 — Distribuição Exponencial](<assets/screenshots/Módulo 4 - Distribuições (2).png>)

A distribuição Exponencial apresentou uma forma mais coerente com a concentração de valores baixos. O parâmetro estimado foi λ = 1,8607. Mesmo assim, ela também não representa perfeitamente todos os sucessos muito grandes. Portanto, a Exponencial é uma candidata melhor que a Normal para descrever a concentração inicial dos dados, mas possui limitações na cauda.

### Módulo 5 — Correlação e regressão linear

![Módulo 5 — Correlação e regressão](<assets/screenshots/Módulo 5 - Correlação e regressão (1).png>)

Foram escolhidas `NA_Sales` como variável X e `EU_Sales` como variável Y. A correlação de Pearson foi r = 0,7677, indicando uma associação linear positiva e relativamente forte entre as duas variáveis.

A reta de regressão foi:

```text
ŷ = 0,021 + 0,475x
```

O coeficiente angular b₁ = 0,475 indica que, para cada unidade adicional associada a `NA_Sales`, o modelo estima um aumento médio de aproximadamente 0,475 unidade em `EU_Sales`. O coeficiente R² foi 0,5894, indicando que aproximadamente 58,94% da variação linear observada em `EU_Sales` é explicada pelo modelo utilizando `NA_Sales`.

![Módulo 5 — Predição e causalidade](<assets/screenshots/Módulo 5 - Correlação e regressão (2).png>)

A correlação não prova causalidade. As duas regiões podem apresentar vendas associadas porque fatores como popularidade do jogo, plataforma, gênero, marketing e período de lançamento influenciam os dois mercados. Portanto, não é correto afirmar que as vendas na América do Norte causam as vendas na Europa.

### Módulo 6 — Relatório de descobertas

O Módulo 6 reúne as três descobertas estatísticas produzidas a partir dos números e gráficos da aplicação.

## 6. As três descobertas

### Descoberta 1 — Diferenças de vendas entre gêneros

- **Afirmação:** Os gêneros de jogos apresentam diferenças nas vendas globais, especialmente quando observamos as medianas e as distribuições por meio do boxplot.
- **Evidência:** Entre os grupos exibidos, `Platform` apresentou mediana de aproximadamente 0,28 e média de 0,938, com 886 registros. O boxplot também mostrou grande quantidade de valores extremos em vários gêneros.
- **Limite honesto:** A comparação mostra associação entre gênero e vendas neste dataset, mas não prova que o gênero cause maiores vendas. Outros fatores, como plataforma, publicadora, época de lançamento e popularidade, também podem influenciar os resultados.

![Descoberta 1 — Vendas por gênero](<assets/screenshots/Módulo 6 - Descobertas (1).png>)

### Descoberta 2 — Associação entre vendas norte-americanas e europeias

- **Afirmação:** As vendas na América do Norte e na Europa possuem associação positiva.
- **Evidência:** A correlação de Pearson foi r = 0,7677 e o coeficiente R² foi 0,5894. O gráfico de dispersão também mostra uma tendência crescente.
- **Limite honesto:** Correlação não implica causalidade. A associação pode ser explicada por popularidade, plataforma, gênero, marketing ou período de lançamento.

![Descoberta 2 — Correlação entre regiões](<assets/screenshots/Módulo 6 - Descobertas (3).png>)

### Descoberta 3 — Jogos com vendas globais fora do padrão

- **Afirmação:** Existem jogos com vendas globais muito acima do padrão observado no restante do dataset.
- **Evidência:** A regra do IQR identificou 1.893 outliers em `Global_Sales`, considerando valores fora do intervalo aproximado de -0,55 a 1,08. O jogo Wii Sports aparece com 82,74 milhões de vendas globais.
- **Limite honesto:** Um outlier é um valor estatisticamente distante, mas isso não significa que o registro seja um erro. Esses jogos podem ser sucessos reais e não representam o comportamento típico de todos os jogos.

![Descoberta 3 — Outliers](<assets/screenshots/Módulo 6 - Descobertas (4).png>)

## 7. Limitações da análise

As conclusões são válidas para os registros presentes neste dataset e não devem ser generalizadas automaticamente para todos os jogos ou para todos os períodos. A presença de valores extremos influencia fortemente a média, o desvio padrão e alguns ajustes de distribuição. Além disso, a correlação e a regressão mostram associação linear, mas não comprovam causalidade. Os valores ausentes também fazem com que o número de observações possa variar conforme a variável analisada.

## 8. Divisão do trabalho

| Componente | O que fez | Commits |
|------------|-----------|---------|
| Jhonata Ferreira de Araujo — 72650246 | Desenvolvimento completo do núcleo estatístico, testes, dataset, aplicação Streamlit, relatório, README e evidências | Commits registrados no histórico do Git |

## 9. Links para entrega

- **Dataset original:** https://www.kaggle.com/datasets/gregorut/videogamesales
- **Repositório:** https://github.com/Jhonataferreiraar/MEC-Sistematizacao
- **Vídeo:** https://youtu.be/zXUieqC58bc
