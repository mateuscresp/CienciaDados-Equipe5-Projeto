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

## Resultados registrados

Execução do Randell no Colab (15/11): melhor F1 macro **0,726**, acurácia 0,748, 3.337 instâncias (limite de ≤ 6 ausentes, KNNImputer, StandardScaler, k = 3, peso por distância, Manhattan). São Francisco é a pior classe (F1 0,587).

- Os 5 melhores diferem em menos de 0,01 de F1; o desvio entre folds é de 0,01 a 0,03. Não dá para defender uma "melhor configuração" única, e sim um grupo equivalente (k de 3 a 7, Manhattan, peso por distância).
- Outra execução, com versão diferente do scikit-learn, deu F1 0,722. Os folds mudam um pouco entre versões, então é preciso reportar média e desvio.
- Principal confusão: São Francisco classificado como Sertão (regiões vizinhas, clima semiárido).

## Conferência do alvo — issue #4 (23/11/2026, Eric)

- Fonte oficial: Condepe/Fidem, **Mesorregiões** (lista dos 185 municípios na divisão histórica do IBGE): https://www.cf.pe.gov.br/observatorio/mapas/regioes/mesorregioes ; IBGE, *Divisão Regional do Brasil em Mesorregiões e Microrregiões Geográficas*, páginas 52–55.
- **Mapeamento conferido, 6 ajustes:** `Afrânio`, `Dormentes`, `Itacuruba`, `Terra Nova` de Sertão → São Francisco Pernambucano; `Feira Nova`, `Machados` de Mata → Agreste Pernambucano.
- Total 5.104 registros; **0 sem mesorregião**; variantes de grafia consistentes; 15 nomes amostrados (seed 42) conferidos com a fonte oficial em `notebooks/05_Limpeza.ipynb`.
- CSV apresenta **319 códigos de posto únicos**; a anotação anterior de 310 postos deve ser revista.
- **Atenção:** os resultados de modelagem e a distribuição das classes documentados em 15/11 são **anteriores à correção**; refazer métricas/experimentos com os rótulos revisados.

## Pendências

- [ ] Confirmar com a APAC o que "-" significa. Indício: não existe nenhum 0 no dataset (mínimo 0,1 mm) e os "-" se concentram nos meses secos de cada região (set: 76% no Sertão × 19% no Agreste). Provável "chuva zero" nas linhas parciais e "posto sem dados" nas 100% vazias. Testar imputar zero (issue #5).
- [ ] Testar outros limites de ausentes (4, 8, 10)
- [ ] Balanceamento para o São Francisco (Aula 8)
- [ ] Seleção de features (Aula 7)
- [ ] Confirmar data de entrega e formato da apresentação com a professora
