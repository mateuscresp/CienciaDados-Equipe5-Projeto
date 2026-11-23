# Decisões do projeto

Registro de cada escolha de método, com data e motivo. Quem decidir algo novo acrescenta uma linha aqui.

## Base de trabalho

- **EDA (Mateus, ~14/10):** `notebooks/01_EDA_Checkpoint.ipynb`, feita 14/10. É a origem do dicionário município → mesorregião (`src/meso_map.py`), da extração da cidade a partir do nome do posto, da conversão do formato largo para o longo e dos gráficos de sazonalidade, ausências e boxplots.
- **Código do modelo (Randell, 15/11):** `src/data.py` e `src/experimentos.py` reaproveitam essas funções (carga, extração de cidade, mapeamento) e acrescentam o pipeline de modelagem, a validação por posto e a grade de 360 experimentos.
- **Dataset:** APAC, 5.104 registros (310 postos, 2010–2025).

## Decisões tomadas

| Data | Decisão | Motivo |
|---|---|---|
| 15/11 | **Formato largo** para o modelo: 1 linha = posto × ano, com os 12 totais mensais como atributos | Cumpre o requisito de ≥ 10 atributos (12) e ≥ 1000 instâncias (5.104). O formato longo (mês, chuva, ano) tem só 3 atributos e fica só para a EDA |
| 15/11 | **Alvo:** mesorregião (5 classes), derivada do município do posto (`src/meso_map.py`) | Todas as 5.104 linhas receberam mesorregião |
| 15/11 | **A mesorregião não entra como atributo.** Só a chuva mensal | Nos slides do Sprint 1 ela aparece como entrada e como saída; como entrada seria vazamento do alvo |
| 15/11 | **Ano fora dos atributos** | Não agrega à previsão de chuva por região |
| 15/11 | **"-" tratado como ausente (NaN)** | Hipótese de trabalho, a confirmar (ver pendências) |
| 15/11 | **Limite de ausentes por linha:** testar sem limite e com no máximo 6 meses vazios | 1.562 linhas (31%) têm os 12 meses vazios; imputar essas linhas só inventaria dado |
| 15/11 | **Imputação dentro do Pipeline** (mediana ou KNNImputer), junto com normalização e KNN | Evita vazamento: nada é ajustado fora do treino |
| 15/11 | **Validação:** StratifiedGroupKFold com 5 folds, agrupando por posto (`Código`), seed 42 | O mesmo posto aparece em vários anos; sem agrupar, o KNN reconhece o posto no teste e infla a acurácia |
| 15/11 | **Métrica principal: F1 macro** (também acurácia e acurácia balanceada) | Classes desbalanceadas (Sertão ~32%, São Francisco ~8%) |
| 15/11 | **Grade de 360 experimentos:** 2 limites de ausentes × 2 imputadores × 3 scalers × 5 valores de k × 2 pesos × 3 distâncias | Passa dos 150 exigidos |
| 23/11 | **Issue #5 — Comparação de imputadores:** mediana, KNNImputer (5 vizinhos) e preenchimento por zero | Avaliar como diferentes tratamentos de `-` afetam o desempenho do KNN, sem assumir que `-` significa necessariamente chuva zero |
| 23/11 | **Limites adicionais:** máximo de 4, 8 e 10 meses ausentes, além de 6 e sem limite | Investigar o efeito da quantidade de dados faltantes sobre o desempenho e a quantidade de instâncias aproveitadas |
| 23/11 | **Melhor resultado exploratório:** zero, máximo de 4 meses ausentes, 3.086 instâncias | Maior F1-macro médio observado (0,7476), mantendo imputação e normalização dentro do Pipeline |
| 23/11 | **Indicador de ausência:** testar quantidade de meses faltantes como atributo adicional | Verificar se o padrão de ausência contém informação útil; não houve melhoria no F1-macro da melhor configuração |
| 23/11 | **Sensibilidade do agrupamento:** comparar validação por `Código` e por `Posto` | Nove nomes aparecem com códigos distintos; F1-macro de 0,7476 por código e 0,7380 por nome. A diferença não comprova ausência de vazamento |

## Resultados registrados

Execução do Randell no Colab (15/11): melhor F1 macro **0,726**, acurácia 0,748, 3.337 instâncias (limite de ≤ 6 ausentes, KNNImputer, StandardScaler, k = 3, peso por distância, Manhattan). São Francisco é a pior classe (F1 0,587).

- Os 5 melhores diferem em menos de 0,01 de F1; o desvio entre folds é de 0,01 a 0,03. Não dá para defender uma "melhor configuração" única, e sim um grupo equivalente (k de 3 a 7, Manhattan, peso por distância).
- Outra execução, com versão diferente do scikit-learn, deu F1 0,722. Os folds mudam um pouco entre versões, então é preciso reportar média e desvio.
- Principal confusão: São Francisco classificado como Sertão (regiões vizinhas, clima semiárido).

 ### Issue #5 — Tratamento de valores ausentes (23/11)

**Responsável:** Ricardo  
**Notebook:** `notebooks/05_Ausentes.ipynb`

Foram analisados os valores `-` presentes nos totais mensais de precipitação. Das 5.104 linhas, 1.562 apresentam todos os 12 meses ausentes e 3.542 possuem pelo menos uma observação mensal.

Foram comparadas três estratégias de imputação (mediana, KNNImputer e zero) e cinco critérios de inclusão de registros (máximo de 4, 6, 8 e 10 meses ausentes, além de ausência de limite). Os experimentos utilizaram KNN com 3 vizinhos, distância Manhattan, pesos pela distância, StandardScaler e StratifiedGroupKFold com 5 folds agrupados por código do posto.

| Limite de ausentes | Instâncias | F1-macro mediana | F1-macro KNNImputer | F1-macro zero |
|---|---:|---:|---:|---:|
| 4 | 3.086 | 0,7151 | 0,7288 | **0,7476** |
| 6 | 3.337 | 0,7100 | 0,7259 | **0,7369** |
| 8 | 3.428 | 0,6880 | 0,6739 | **0,6988** |
| 10 | 3.488 | 0,6885 | 0,6951 | **0,7193** |
| Sem limite | 3.542 | 0,6846 | 0,6823 | **0,6996** |

A imputação por zero obteve o maior F1-macro em todos os limites avaliados. A melhor configuração exploratória apresentou F1-macro de **0,7476 ± 0,0224**, utilizando 3.086 instâncias e no máximo quatro meses ausentes.

A inclusão da quantidade de meses ausentes como atributo adicional não melhorou o F1-macro dessa configuração (0,7206 com indicador, contra 0,7476 sem indicador).

**Análise de sensibilidade:** ao substituir o agrupamento por código pelo agrupamento por nome do posto, o F1-macro passou de 0,7476 para 0,7380. O resultado sugere relativa estabilidade global, mas não comprova ausência de vazamento.

**Recomendação:** considerar a imputação por zero com limite de quatro meses ausentes como configuração candidata para experimentos posteriores, preservando a configuração original com KNNImputer e limite de seis meses como referência comparativa.

**Limitações:** não foi confirmado o significado de `-` junto à APAC. Portanto, o preenchimento por zero é uma estratégia experimental, não uma interpretação comprovada dos dados. Além disso, a comparação entre limites utiliza subconjuntos diferentes, e a escolha da melhor configuração foi realizada sobre os mesmos folds utilizados para avaliar seu desempenho, sem validação independente.

## Pendências

- [ ] Confirmar com a APAC o significado de `-`. A comparação experimental foi concluída, mas não há evidência suficiente para afirmar que representa chuva zero.
- [x] Testar imputação por zero e outros limites de ausentes (4, 6, 8, 10 e sem limite). Resultados documentados em `notebooks/05_Ausentes.ipynb`.
- [ ] Balanceamento para o São Francisco (Aula 8)
- [ ] Seleção de features (Aula 7)
- [ ] Confirmar data de entrega e formato da apresentação com a professora
