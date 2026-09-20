# COMECE AQUI — passo a passo para quem nunca programou

Este template já tem TUDO montado: interface, testes, gráficos, simulações.
O que falta é o que vale nota e aprendizado: **as funções estatísticas** e
**os textos de interpretação**. Cada coisa que falta está marcada com `TODO`.

> Regra de leitura: faça na ordem. Não pule etapas. Um commit por TODO.

---

## Parte 1 — Preparar o computador (só uma vez, 15 min)

### 1.1 Instalar o Python
Baixe em https://www.python.org/downloads/ (versão 3.10 ou mais nova).
**No Windows, marque a caixa "Add Python to PATH"** na instalação.

### 1.2 Abrir o terminal DENTRO da pasta do projeto
- **VS Code:** abra a pasta do projeto (File → Open Folder) e aperte `Ctrl + '` (crase).
- **Windows sem VS Code:** abra a pasta no Explorador, clique na barra de endereço, digite `cmd` e Enter.

### 1.3 Criar o ambiente virtual e instalar as bibliotecas
Copie e cole uma linha de cada vez:

```bash
python -m venv .venv
```
```bash
.venv\Scripts\activate
```
(no Linux/Mac: `source .venv/bin/activate`)

Você vai ver `(.venv)` no começo da linha. Isso significa que o ambiente está ativo.
**Toda vez que abrir o terminal de novo, repita só este comando de ativar.**

```bash
pip install -r requirements.txt
```

### 1.4 Criar um dataset de teste (temporário)
```bash
python dados/gerar_dataset_exemplo.py
```
Isso cria `dados/dataset.csv` com dados inventados de jogos, só para o app
funcionar hoje. **Vocês vão trocar por um dataset real na Parte 3.**

### 1.5 Conferir que tudo funciona
```bash
pytest -v
```
Vai aparecer muita coisa em vermelho (FAILED). **Isso é esperado**: cada
vermelho é um TODO que vocês ainda não fizeram. Os verdes (PASSED) são as
funções que já vieram prontas.

```bash
streamlit run app.py
```
O navegador abre com a aplicação. Navegue pelos módulos: onde faltar uma
função, o app avisa qual TODO implementar. Para parar o app: `Ctrl + C` no terminal.

---

## Parte 2 — O núcleo: `minhastats.py` (TODOs 1 a 12) — Semana 1 e 2

Abra `minhastats.py`. Cada TODO é uma função com os PASSOS escritos em
comentários. A rotina é sempre a mesma:

1. Leia a explicação da função e a fórmula no guia (Etapa 2).
2. Escreva uma linha de código abaixo de cada `# PASSO`.
3. Apague a linha `raise NotImplementedError(...)`.
4. Rode `pytest -v -k nome_da_funcao` (ex.: `pytest -v -k mediana`).
5. Verde? Commit: `git add . && git commit -m "implementa mediana + teste passando"`.
6. Vermelho? Leia a mensagem de erro (a última linha explica) e compare com a fórmula.

| TODO | Função | Dificuldade | Depende de |
|------|--------|-------------|------------|
| 1 | mediana | ★ | — |
| 2 | moda | ★ | contar_frequencias (pronta) |
| 3 | amplitude | ★ | — |
| 4 | percentil | ★★★ | — (a mais chata: siga os passos à risca) |
| 5 | quartis | ★ | percentil |
| 6 | coeficiente_variacao | ★ | media, desvio_padrao |
| 7 | covariancia | ★★ | media |
| 8 | correlacao | ★★ | covariancia, desvio_padrao |
| 9 | numero_classes_sturges | ★ | — |
| 10 | outliers_iqr | ★★ | quartis |
| 11 | interpretar_assimetria | ★★ | media, mediana, desvio_padrao |
| 12 | regressao_linear | ★★★ | media |

Quando os 12 passarem, rode `python verificar_regra_de_ouro.py`.

---

## Parte 3 — O dataset real (TODO 13 e 14) — Semana 1

1. Escolham um tema que dê curiosidade (jogos, música, transporte, futebol...).
2. Procurem em Kaggle, Hugging Face Datasets, UCI ou dados.gov.br.
3. Baixem o CSV e salvem como `dados/dataset.csv` (substituindo o de exemplo).
4. Rodem `python inspecionar_dataset.py` e respondam ao checklist da Etapa 1 do guia.
5. Preencham os **TODO 13 e 14** no topo de `app.py` (nome, fonte, separadores, nulos).
6. Commit: `git commit -m "adiciona dataset X e configuração do app"`.

---

## Parte 4 — Os textos da interface (TODOs 15 a 20) — Semanas 3 e 4

Tudo no topo de `app.py`. Rode o app, use cada módulo com os SEUS dados, e
escreva o que viram:

- **TODO 15** — o que o TCL mostrou (Módulo 3).
- **TODO 16** — a Normal ajustou bem ou mal? (Módulo 4).
- **TODO 17** — um exemplo do dataset onde correlação não é causa (Módulo 5).
- **TODO 18, 19, 20** — as três descobertas (Módulo 6). O app gera o gráfico
  sozinho: vocês só dizem o tipo e os nomes das colunas.

---

## Parte 5 — Entrega (TODO A e B) — Semana 4

- `README.md` → TODO A (nomes, matrículas, links, prints).
- `RELATORIO.md` → TODO B (uma seção por item; a tabela de validação vem do `pytest -v`).
- Vídeo de 3 a 5 min e PDF final: siga a Etapa 7 do guia.

---

## Erros comuns e como resolver

| Mensagem no terminal | Causa | Solução |
|----------------------|-------|---------|
| `'streamlit' não é reconhecido` / `command not found` | ambiente virtual não ativado | `.venv\Scripts\activate` |
| `ModuleNotFoundError: No module named 'pandas'` | bibliotecas não instaladas nesse ambiente | `pip install -r requirements.txt` |
| `IndentationError` | espaços errados no início da linha | alinhe o código com os comentários `# PASSO` (4 espaços) |
| `NotImplementedError: TODO n` | função ainda não feita | implemente o TODO n |
| `FileNotFoundError: dados/dataset.csv` | CSV não está na pasta `dados/` com esse nome | mova/renomeie o arquivo ou ajuste o TODO 13 |
| `UnicodeDecodeError` ao ler o CSV | arquivo em outra codificação | abra no Excel/LibreOffice e salve como "CSV UTF-8" |
| Números aparecem como texto (`object`) | vírgula decimal ou "N/A" | `SEPARADOR_DECIMAL = ","` e/ou `COLUNAS_PARA_CONVERTER_EM_NUMERO` no TODO 13 |
| Teste diz `assert False` na variância | dividiu por n em vez de n−1 (ou o contrário) | releia a Etapa 2.3 do guia |

## Git em 4 comandos (todo dia de trabalho)

```bash
git pull                                  # pega o que os colegas fizeram
git add .                                 # marca o que você mudou
git commit -m "implementa percentil"      # registra com mensagem descritiva
git push                                  # envia para o GitHub
```
