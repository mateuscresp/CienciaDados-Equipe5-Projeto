# Análise de codificação e balanceamento

Esta análise compara as escolhas do modelo principal com alternativas experimentais. A pipeline principal não foi alterada.

## Métodos usados no modelo principal

O modelo usa os 12 totais mensais de chuva como atributos numéricos. Como são medidas contínuas em milímetros, não precisam de codificação categórica. O ano fica fora dos atributos e o alvo é o nome textual da mesorregião, que o `KNeighborsClassifier` aceita diretamente.

A configuração da base v1 pode ser resumida assim:

```python
pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(
        n_neighbors=5,
        weights="distance",
        metric="manhattan",
    )),
])
```

O modelo não reamostra as classes. Imputação e escala são ajustadas dentro do pipeline em cada fold, e a validação é agrupada por posto para evitar que registros do mesmo posto apareçam simultaneamente no treino e no teste.

## Alternativas avaliadas

| Configuração | Instâncias | F1 macro | Desvio F1 macro | Precisão SF | Recall SF | F1 SF |
|---|---:|---:|---:|---:|---:|---:|
| Sem reamostragem (base v1) | 3.337 | 0,723 | 0,032 | 0,638 | 0,497 | 0,559 |
| RandomOverSampler | 3.337 | 0,682 | 0,028 | 0,456 | 0,718 | 0,558 |
| RandomUnderSampler | 3.337 | 0,658 | 0,025 | 0,438 | 0,700 | 0,539 |
| SMOTE (`k=3`) | 3.337 | 0,685 | 0,030 | 0,480 | 0,703 | 0,571 |
| SMOTE (`k=5`) | 3.337 | 0,694 | 0,034 | 0,481 | 0,712 | 0,574 |
| 12 meses + Ano em One-Hot | 3.337 | **0,769** | 0,032 | 0,715 | 0,579 | **0,640** |

Para representar o ano como categoria, o experimento usa um `ColumnTransformer`:

```python
preprocessamento = ColumnTransformer([
    ("meses", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), MESES),
    ("ano", OneHotEncoder(handle_unknown="ignore"), ["Ano"]),
])
```

O experimento de balanceamento usa `imblearn.pipeline.Pipeline`, na ordem imputação, escala, reamostragem e KNN. Assim, o sampler é ajustado somente no treino de cada fold:

```python
pipe_smote = ImbPipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("balanceamento", SMOTE(k_neighbors=5, random_state=42)),
    ("knn", KNeighborsClassifier(
        n_neighbors=5,
        weights="distance",
        metric="manhattan",
    )),
])
```

## Interpretação

- **Meses sem encoding:** é adequado porque os meses são medidas numéricas. Codificar janeiro a dezembro como 1 a 12 imporia uma distância linear artificial, inclusive entre dezembro e janeiro.
- **Alvo textual:** não precisa de `LabelEncoder` para este classificador; o alvo não participa do cálculo de distância entre atributos.
- **Sem reamostragem:** foi a melhor opção entre os métodos balanceados em F1 macro (0,723 contra 0,694 do SMOTE com `k=5`). Isso favorece a escolha atual quando a prioridade é o desempenho geral equilibrado.
- **Trade-off do São Francisco:** RandomOverSampler elevou o recall de 0,497 para 0,718, mas reduziu a precisão de 0,638 para 0,456 e o F1 macro para 0,682. SMOTE com `k=5` teve F1 da classe ligeiramente maior que a base (0,574 contra 0,559), mas também reduziu o F1 macro.
- **Ano em One-Hot:** obteve os maiores resultados nesta comparação: F1 macro 0,769 e F1 do São Francisco 0,640. O One-Hot adiciona uma dimensão binária para cada ano; com Manhattan, duas amostras de anos diferentes recebem uma distância adicional de 2. Isso pode mudar os vizinhos escolhidos pelo KNN.

## Conclusão

Manter os meses numéricos e não reamostrar é uma escolha defensável para priorizar o F1 macro geral; não é a melhor opção para toda métrica, pois a reamostragem aumenta o recall do São Francisco. Ano em One-Hot é uma alternativa promissora, não uma conclusão definitiva: a validação agrupou por posto, mas não separou os anos cronologicamente, e a seleção foi feita nos mesmos folds usados para avaliar. É necessário testar em anos não vistos antes de adotar essa variável no modelo principal.
