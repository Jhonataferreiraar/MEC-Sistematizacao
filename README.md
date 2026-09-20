# Laboratório Estatístico Interativo

<!-- TODO A: preencha a tabela da equipe (máx. 5 componentes) -->

**Equipe:** TODO A — nome da equipe

| Nome completo | Matrícula | Frente principal |
|---------------|-----------|------------------|
| TODO A        | TODO A    | núcleo estatístico |
| TODO A        | TODO A    | núcleo estatístico |
| TODO A        | TODO A    | interface |
| TODO A        | TODO A    | simulações e distribuições |
| TODO A        | TODO A    | relatório, vídeo e qualidade |

**Dataset:** TODO A — nome do dataset · fonte original: TODO A — link

**Vídeo (3 a 5 min):** TODO A — link (YouTube não listado ou Drive liberado, testado deslogado)

## Como rodar

```bash
# 1. criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / Mac

# 2. instalar as dependências
pip install -r requirements.txt

# 3. rodar os testes do núcleo (todos devem passar)
pytest -v

# 4. rodar a aplicação
streamlit run app.py
```

## Estrutura

```
app.py                     interface (Streamlit) — só exibe o que o núcleo calcula
minhastats.py              NÚCLEO: funções estatísticas da equipe, sem NumPy nas contas
test_minhastats.py         testes pytest comparando com NumPy/SciPy
verificar_regra_de_ouro.py confere que a regra de ouro foi respeitada
inspecionar_dataset.py     inspeção de 5 minutos do dataset (Etapa 1)
dados/dataset.csv          o dataset
RELATORIO.md               relatório final
requirements.txt           dependências
```

## Prints da aplicação

<!-- TODO A: cole aqui um print por módulo (arraste a imagem para a pasta e referencie) -->

- Módulo 2 — Descritiva: TODO A
- Módulo 3 — Simulação: TODO A
- Módulo 4 — Distribuições: TODO A
- Módulo 5 — Regressão: TODO A
- Módulo 6 — Descobertas: TODO A
