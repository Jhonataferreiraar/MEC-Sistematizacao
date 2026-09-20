# Relatório — Laboratório Estatístico Interativo

<!--
  Estrutura da Etapa 7.1 do guia: uma seção por item. Quem seguiu o guia já
  produziu cada peça — o relatório é montagem, não maratona.
  Substitua cada "TODO B" pelo texto da equipe. Apague estes comentários no final.
-->

**Equipe:** TODO B · **Componentes:** TODO B (nome completo e matrícula de todos)

## 1. Dataset e justificativa

- **Nome:** TODO B
- **Fonte original:** TODO B (link)
- **Tamanho:** TODO B linhas × TODO B colunas
- **Variáveis numéricas usadas:** TODO B
- **Variáveis categóricas usadas:** TODO B
- **Por que escolhemos:** TODO B (que perguntas reais a equipe tinha sobre esses dados?)

## 2. Decisões de tratamento dos dados

<!-- Tratamento de dados é conteúdo, não bastidor. -->

- Valores ausentes: TODO B (quantos, em quais colunas, o que fizemos e por quê)
- Texto onde deveria haver número: TODO B (colunas convertidas com `pd.to_numeric(errors="coerce")`)
- Outras decisões: TODO B (linhas removidas, categorias agrupadas, unidades convertidas...)

## 3. Fórmulas do núcleo (minhastats.py)

<!-- Escreva as fórmulas em notação matemática, com as SUAS palavras. -->

| Função | Fórmula | Observação |
|--------|---------|------------|
| média | média = (1/n) · Σ xᵢ | TODO B: caso vazio |
| variância amostral | s² = Σ(xᵢ − média)² / (n − 1) | TODO B: por que n − 1? (correção de Bessel) |
| variância populacional | σ² = Σ(xᵢ − média)² / n | |
| desvio padrão | s = √s² | |
| mediana | TODO B | TODO B |
| moda | TODO B | TODO B |
| amplitude | TODO B | |
| percentil | TODO B | convenção: posição p·(n−1)/100 com interpolação linear |
| coeficiente de variação | TODO B | TODO B: média zero |
| covariância | TODO B | |
| correlação de Pearson | TODO B | TODO B: variável constante |
| regressão (b₀, b₁, R²) | TODO B | |

## 4. Tabela de validação

<!-- Rode `pytest -v` e preencha. A tolerância está no topo de test_minhastats.py. -->

| Função | Referência | Diferença observada | Tolerância | Passou? |
|--------|------------|---------------------|------------|---------|
| media | np.mean | TODO B | 1e-9 (relativa) | TODO B |
| variancia (amostral) | np.var(ddof=1) | TODO B | 1e-9 | TODO B |
| variancia (populacional) | np.var(ddof=0) | TODO B | 1e-9 | TODO B |
| mediana | np.median | TODO B | 1e-9 | TODO B |
| percentil | np.percentile | TODO B | 1e-6 | TODO B |
| covariancia | np.cov(ddof=1) | TODO B | 1e-9 | TODO B |
| correlacao | np.corrcoef | TODO B | 1e-9 | TODO B |
| regressao_linear | scipy.stats.linregress | TODO B | 1e-9 | TODO B |

Saída do `pytest -v`: TODO B (cole um print ou o texto)

## 5. Os módulos (um print + um parágrafo por módulo)

### Módulo 2 — Descritiva interativa
TODO B: print + parágrafo (que variável, o que a interpretação automática disse, outliers encontrados)

### Módulo 3 — Simulação (LGN e TCL)
TODO B: print + parágrafo (o que aconteceu com n = 2, 10 e 30 sobre a variável escolhida)

### Módulo 4 — Distribuições teóricas
TODO B: print + parágrafo (a Normal ajustou bem ou mal? por quê? qual distribuição descreveria melhor?)

### Módulo 5 — Correlação e regressão
TODO B: print + parágrafo (equação, R², interpretação de b₁, exemplo de causalidade duvidosa)

## 6. As três descobertas

<!-- Afirmação em uma frase + evidência (número/gráfico da aplicação) + limite honesto. -->

### Descoberta 1 — TODO B (título)
- **Afirmação:** TODO B
- **Evidência:** TODO B
- **Limite honesto:** TODO B

### Descoberta 2 — TODO B (título)
- **Afirmação:** TODO B
- **Evidência:** TODO B
- **Limite honesto:** TODO B

### Descoberta 3 — TODO B (título)
- **Afirmação:** TODO B
- **Evidência:** TODO B
- **Limite honesto:** TODO B

## 7. Divisão do trabalho

| Componente | O que fez | Commits (aprox.) |
|------------|-----------|------------------|
| TODO B | TODO B | TODO B |
