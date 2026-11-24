# Ciência de Dados – Equipe 5 (CIn/UFPE)

Projeto da disciplina CIN0208 (profa. Juscimara G. Avelino): **classificar a mesorregião de Pernambuco a partir da chuva mensal (dados APAC) com KNN**.

**Equipe:** Mateus Henrique, Gabriel Bueno, Randell Almeida, José Ricardo Torres, Eric Nunes

## Dados
- `data/raw/Dataset APAC - Página1.csv` — 5.104 registros (posto × ano, 2010–2025), 12 colunas de chuva mensal (mm).
- Alvo: `Mesorregiao` (5 classes), derivada do município do posto (`src/meso_map.py`).
- Features: os 12 totais mensais (**12 atributos**). Valores "-" = sem medição (NaN), tratados dentro do Pipeline.

## Estrutura
```
data/raw/        dados brutos (não editar)
docs/            decisões, divisão de temas e issues detalhadas
notebooks/       01_EDA_Checkpoint (EDA)
                 02_Modelagem_KNN (protocolo principal, 360 experimentos)
                 03_Experimentos_Extras (imputar 0, outliers, escalas, seleção, PCA, balanceamento)
src/             data.py, meso_map.py, experimentos.py
results/         experimentos_knn.csv, matriz_confusao, instancias_incorretas.csv, relatorio_melhor.txt
```
## Como rodar
```bash
pip install -r requirements.txt
python src/experimentos.py            # 360 experimentos + matriz de confusão -> results/
```

## Decisões de método
- **Pipeline** (imputação → normalização → KNN): nada é ajustado fora do treino.
- **StratifiedGroupKFold (5) agrupando por posto**: o mesmo posto em anos diferentes não aparece em treino e teste (evita vazamento).
- Classes desbalanceadas (Sertão ~32%, São Francisco ~8%) → métrica principal **F1 macro** + balanced accuracy.
- Grade: 2 imputações × 3 scalers × 5 valores de k × 2 pesos × 3 distâncias × 2 limites de ausentes (sem limite ou ≤ 6 meses vazios) = **360 experimentos**.

## Resultados

Validação por posto (StratifiedGroupKFold, 5 folds, seed 42), com o alvo corrigido na issue #4. Baseline (Dummy): acurácia 0,34 e F1 macro 0,10.

| Modelo | F1 macro | Acurácia | F1 São Francisco |
|---|---|---|---|
| Melhor KNN (mediana, ≤6 meses ausentes, MinMax, k=9, distance, manhattan) | 0,711 | 0,745 | 0,507 |

Os 10 melhores modelos ficam entre 0,705 e 0,711, dentro do desvio entre folds (≈ 0,03).

Extras (notebook 03): imputar "-" como zero dá F1 0,733 (0,748 com até 4 meses vazios; hipótese sem confirmação da APAC); o indicador de ausência piora (0,685); seleção de atributos e PCA não ajudam (0,578 a 0,686 contra 0,705); balanceamento sobe o recall do São Francisco (0,49 → 0,69 a 0,73) e reduz o F1 macro (0,656 a 0,685).

Erros: concentrados entre regiões vizinhas (São Francisco → Sertão: 145; Mata → Agreste: 143).
- `docs/decisoes.md` — decisões de método, resultados registrados e pendências.
- Tarefas: aba **Issues** do repositório (cada uma com responsável e prazo).

## Como contribuir
1. Pegar uma issue e trabalhar em branch própria: `git checkout -b nome/tarefa`.
2. `git pull` antes de começar; commits pequenos e Pull Request para `main`, revisado por outra pessoa.
3. Notebooks: rodar "Restart & run all" antes de commitar.
4. Seed fixa em 42 em tudo que for aleatório; não editar `data/raw/`.
5. Resultados novos em `results/` com nome claro; decisões em `docs/decisoes.md`.
6. Sem Git instalado: dá para rodar tudo no Colab (`!git clone <url>`, `!pip install -r requirements.txt`, `!python src/experimentos.py`).
