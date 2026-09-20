# Laboratório Estatístico Interativo

**Equipe:** MEC-Sistematizacao

| Nome completo | Matrícula | Frente principal |
|---|---|---|
| Jhonata Ferreira de Araujo | 72650246 | Desenvolvimento completo |

**Dataset:** Video Game Sales
**Fonte original:** https://www.kaggle.com/datasets/gregorut/videogamesales
**Repositório:** https://github.com/Jhonataferreiraar/MEC-Sistematizacao
**Vídeo:** inserir o link público após a gravação

## Como rodar

Abra o PowerShell na pasta do projeto:

```powershell
# 1. Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 2. Instalar as dependências
python -m pip install -r requirements.txt

# 3. Executar os testes
python -m pytest -v

# 4. Conferir a regra de ouro
python verificar_regra_de_ouro.py

# 5. Rodar a aplicação
python -m streamlit run app.py
```

Se o ambiente virtual ainda não existir:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Sobre o projeto

O laboratório utiliza o dataset Video Game Sales, com 16.598 registros, sete variáveis numéricas e quatro variáveis categóricas. A aplicação permite explorar dados reais por meio de estatística descritiva, simulações, distribuições teóricas, correlação, regressão linear e descobertas estatísticas.

As medidas exibidas pela aplicação são calculadas pelas funções próprias de `minhastats.py`. Pandas é utilizado para carregar e organizar os dados, e NumPy/SciPy aparecem nos testes de validação.

## Estrutura

```text
app.py                     interface da aplicação Streamlit
minhastats.py              núcleo com as funções estatísticas próprias
test_minhastats.py         testes comparativos com NumPy e SciPy
verificar_regra_de_ouro.py verificação da separação entre interface e núcleo
inspecionar_dataset.py      inspeção inicial do dataset
dados/dataset.csv          dataset utilizado
RELATORIO.md               relatório final
requirements.txt           dependências do projeto
assets/screenshots/        evidências da aplicação e dos testes
```

## Prints da aplicação

### Módulo 0 — Dataset

![Módulo 0 — Dataset](<assets/screenshots/Módulo 0 - Dataset.png>)

### Módulo 2 — Estatística descritiva

![Módulo 2 — Descritiva 1](<assets/screenshots/Módulo 2 - Descritiva (1).png>)

![Módulo 2 — Descritiva 2](<assets/screenshots/Módulo 2 - Descritiva (2).png>)

![Módulo 2 — Descritiva 3](<assets/screenshots/Módulo 2 - Descritiva (3).png>)

### Módulo 3 — Simulação

![Módulo 3 — Simulação 1](<assets/screenshots/Módulo 3 - Simulação (1).png>)

![Módulo 3 — Simulação 2](<assets/screenshots/Módulo 3 - Simulação (2).png>)

### Módulo 4 — Distribuições

![Módulo 4 — Distribuições 1](<assets/screenshots/Módulo 4 - Distribuições (1).png>)

![Módulo 4 — Distribuições 2](<assets/screenshots/Módulo 4 - Distribuições (2).png>)

### Módulo 5 — Correlação e regressão

![Módulo 5 — Correlação e regressão 1](<assets/screenshots/Módulo 5 - Correlação e regressão (1).png>)

![Módulo 5 — Correlação e regressão 2](<assets/screenshots/Módulo 5 - Correlação e regressão (2).png>)

### Módulo 6 — Descobertas

![Módulo 6 — Descobertas 1](<assets/screenshots/Módulo 6 - Descobertas (1).png>)

![Módulo 6 — Descobertas 2](<assets/screenshots/Módulo 6 - Descobertas (2).png>)

![Módulo 6 — Descobertas 3](<assets/screenshots/Módulo 6 - Descobertas (3).png>)

![Módulo 6 — Descobertas 4](<assets/screenshots/Módulo 6 - Descobertas (4).png>)

### Testes

![Testes 1](<assets/screenshots/testes 1.png>)

![Testes 2](<assets/screenshots/Testes 2.png>)
