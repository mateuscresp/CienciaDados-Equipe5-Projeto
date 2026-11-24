# Issue #6 — Conclusões para relatório e slides

**Origem:** `results/experimentos_knn.csv` (360 linhas) e EDA do CSV da APAC. **Atenção:** o CSV de experimentos foi gerado antes das seis correções de rótulos da Issue #4; esses resultados precisam ser recalculados para representar o modelo atualizado.

## Parágrafo para o relatório

Foram analisados 360 experimentos de classificação utilizando o algoritmo K-Nearest Neighbors (KNN), considerando diferentes configurações de imputação, normalização, métricas de distância, pesos dos vizinhos, número de vizinhos e tratamento de valores ausentes. A melhor configuração registrada apresentou F1 macro de 0,7224, com desvio de 0,0436 entre os folds. Observou-se que a diferença de desempenho entre os cinco melhores experimentos foi de aproximadamente 0,00374, valor inferior à variabilidade observada durante a validação cruzada, indicando que não há evidências suficientes para afirmar a superioridade de uma configuração específica. Além disso, os experimentos com limite de seis meses ausentes apresentaram desempenho superior aos realizados sem esse limite. Entretanto, essa comparação deve ser interpretada com cautela, pois os conjuntos de dados possuem quantidades diferentes de instâncias (3.337 e 5.104, respectivamente). A análise exploratória também contemplou a distribuição das mesorregiões, o comportamento mensal das precipitações e a correlação entre os atributos, contribuindo para a compreensão dos dados e para a interpretação dos resultados do modelo.

## Pitch (5 tópicos)

1. **Análise exploratória:** investigamos a distribuição das cinco mesorregiões pernambucanas, o comportamento mensal das chuvas e as correlações entre os atributos.
2. **Experimentos:** avaliamos 360 configurações do algoritmo KNN, considerando diferentes estratégias de pré-processamento e parâmetros de classificação.
3. **Melhor desempenho:** a melhor configuração registrada alcançou F1 macro de 0,7224, utilizando imputação pela mediana, StandardScaler, distância Manhattan, pesos por distância e cinco vizinhos.
4. **Estabilidade dos resultados:** os cinco melhores experimentos apresentaram diferenças pequenas de desempenho em comparação com a variabilidade entre os folds, não sendo possível afirmar que uma configuração é claramente superior.
5. **Valores ausentes:** limitar a quantidade de meses sem informações apresentou resultados melhores, mas reduziu a base de 5.104 para 3.337 registros, exigindo cautela na interpretação.

## Figuras e interpretações

- `eda_distribuicao_classes.png`: ilustra o desbalanceamento e sustenta a escolha do F1 macro.
- `eda_boxplot_meses.png`: mostra sazonalidade geral, justificando manter todas as colunas de mês como atributos candidatos.
- `eda_boxplot_mesorregioes.png`: mostra diferenças regionais na distribuição da chuva, sem justificar exclusão automática de outliers.
- `eda_boxplot_mes_regiao.png`: detalha os 12 meses em cada mesorregião e evidencia padrões sazonais distintos.
- `eda_correlacao_meses.png`: revela relações entre meses, mas descartar atributos exige avaliação em validação cruzada.
- `experimentos_fator_*.png` (6 figuras): apresentam média e máximo de F1 macro por fator; a barra de erro é a dispersão **entre configurações**, não a variabilidade entre folds.

## Limitação da migração do PR #1

O ZIP de referência não contém o arquivo `main.py` do PR #1. Assim, foi implementado um módulo **equivalente e reproduzível** em `src/eda_graficos.py`, e **não** uma cópia literal do código do PR. Para migração literal, revisar o código do PR #1 com o grupo.

## Execução

Da raiz do projeto: `python src/eda_graficos.py`. Em seguida abrir `notebooks/06_Analise_Experimentos.ipynb` e executar tudo. As 11 figuras geradas ficam em `results/figuras/` (150 dpi). Não altera os dados brutos.
