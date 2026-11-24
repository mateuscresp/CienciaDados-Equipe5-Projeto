# Conferência de mapeamento — Issue #4

**Responsável:** Eric · **Revisão:** 23/11/2026

**Fonte de referência:** [Condepe/Fidem, divisão histórica do IBGE](https://www.cf.pe.gov.br/observatorio/mapas/regioes/mesorregioes).

**Resultado:** 0 registros sem mesorregião entre 5.104 linhas; 15 municípios amostrados conferidos e coerentes; variantes de grafia compatíveis; **6 correções no alvo**:

| Cidade | Antes | Depois | Registros |
|---|---|---|---:|
| Afrânio | Sertão | São Francisco | 32 |
| Dormentes | Sertão | São Francisco | 32 |
| Itacuruba | Sertão | São Francisco | 16 |
| Terra Nova | Sertão | São Francisco | 16 |
| Feira Nova | Mata | Agreste | 16 |
| Machados | Mata | Agreste | 16 |

A contagem oficial de postos no CSV é **319 códigos distintos** (documentação anterior: 310). As métricas de KNN e os experimentos devem ser recalculados após alteração dos rótulos.

Veja o notebook `notebooks/05_Limpeza.ipynb` para os testes reproduzíveis.
