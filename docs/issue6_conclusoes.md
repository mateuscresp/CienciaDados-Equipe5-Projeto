# Issue #6 — Conclusões para relatório e slides

**Origem:** `results/experimentos_knn.csv` (360 linhas) e EDA do CSV da APAC. **Atenção:** o CSV de experimentos foi gerado antes das seis correções de rótulos da Issue #4; esses resultados precisam ser recalculados para representar o modelo atualizado.

## Parágrafo para o relatório

Na análise histórica de 360 configurações do classificador KNN sobre dados de precipitação mensal da APAC, o maior F1 macro foi 0,7224, com desvio de 0,0436 entre folds, utilizando 3.337 instâncias, imputação por mediana, StandardScaler, cinco vizinhos, ponderação por distância e métrica Manhattan. Os cinco melhores experimentos variaram apenas 0,00374 ponto no F1 macro, abaixo do menor desvio entre folds entre esses modelos (0,0401), o que não permite afirmar a superioridade robusta de uma única configuração. A EDA identificou desequilíbrio na distribuição entre as cinco mesorregiões e diferentes perfis de precipitação sazonal, reforçando o uso de F1 macro e a avaliação de todos os meses. A comparação entre usar ou não o limite de seis meses ausentes é descritiva, pois envolve populações diferentes (3.337 e 5.104 instâncias). As métricas históricas devem ser reexecutadas com os rótulos corrigidos na Issue #4 antes de serem tratadas como resultados finais.

## Pitch (4 tópicos)

1. Base APAC: 5.104 registros de posto × ano, 12 atributos mensais e cinco mesorregiões; classes desbalanceadas.
2. EDA: distribuição por classe, sazonalidade por mês e por região, correlações entre meses; não excluir extremos só porque aparecem no boxplot.
3. Grade histórica de 360 configurações: melhor F1 macro 0,7224 ± 0,0436 (desvio entre folds); top 5 separados por somente 0,00374.
4. Decisão: reportar média e desvio, priorizar F1 macro, evitar afirmar um único vencedor e reexecutar os experimentos com a correção do alvo antes dos slides finais.

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
