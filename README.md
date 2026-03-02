# IDS com Machine Learning (UNSW-NB15)

Projeto de TCC: Sistema de Detecção de Intrusão em Redes usando ML com dataset UNSW-NB15.

## Estrutura
- `data/raw`: arquivos parquet originais (não versionados)
- `data/processed`: dados prontos para treino/teste
- `artifacts`: modelos e pipelines
- `reports`: métricas e figuras
- `src`: código fonte
- `scripts`: scripts de execução

## Rodar (exemplo)
1. Coloque os parquets em `data/raw/`
2. Execute:
   - `python scripts/01_preprocess.py`
   - `python scripts/02_train.py`
   - `python scripts/03_evaluate.py`
