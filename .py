import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
import kagglehub
from kagglehub import KaggleDatasetAdapter
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV


df = kagglehub.load_dataset(
   KaggleDatasetAdapter.PANDAS,
   "renatosn/sao-paulo-housing-prices",
   "data.csv"
)


df_clean = df[df['area'] > 0].copy()


x = df_clean[['district', 'area', 'bedrooms', 'garage', 'type']]
y = df_clean['total']


x_train, x_test, y_train, y_test = train_test_split(
   x, y, test_size=0.2, random_state=42
)


numericas = ['area', 'bedrooms', 'garage']
categoricas = ['district', 'type']


pre_processor = ColumnTransformer(
   transformers=[('num', StandardScaler(), numericas),
   ('cat', OneHotEncoder(handle_unknown = 'ignore'), categoricas,),]
)


x_train_scaled = pre_processor.fit_transform(x_train)
x_test_scaled = pre_processor.transform(x_test)


knn_base = KNeighborsRegressor(n_neighbors=5)
knn_base.fit(x_train_scaled, y_train)


y_predict_base = knn_base.predict(x_test_scaled)
rmse_base = np.sqrt(mean_squared_error(y_test, y_predict_base))
r2_base = r2_score(y_test, y_predict_base)


para_grid = {
   'n_neighbors' : [3, 5, 7, 9],
   'weights' : ['uniform', 'distance'],
   'metric' : ['euclidean', 'manhattan'],
}


grid = GridSearchCV(
   KNeighborsRegressor(),
   para_grid,
   cv=5,
   scoring='neg_root_mean_squared_error',
)
grid.fit(x_train_scaled, y_train)


print(f"Melhores parâmetros: {grid.best_params_}")
print(f"Erro Médio (RMSE): R$ {rmse_base:,.2f}")
print(f"Coeficiente R²: {r2_base:.4f}")
print(f"Formato original de X_train: {x_train.shape}")
print(f"Formato de X_train após transformação: {x_train_scaled.shape}")
print(f"Linhas restantes após a limpeza: {len(df_clean)}")
print("\nVariáveis de Entrada (X):")
print(x.head(2))
print("\nVariável Alvo (y):")
print(y.head(2))
print(df.head())
# --- INSPEÇÃO DOS DADOS ---
print("\n=== 1. TIPOS DE DADOS E VALORES AUSENTES ===")
print(df.info())
print("\n=== 2. RESUMO ESTATÍSTICO ===")
print(df.describe())
print("\n=== 3. CONTAGEM DE NULOS ===")
print(df.isnull().sum())



import pandas as pd


# 1. Carrega o arquivo CSV com os ajustes típicos do Excel em português
df = pd.read_csv(
   'Dataset.Pluviometria.csv',
   sep=';',              # Se o seu CSV usar vírgula, troque por sep=','
   decimal=',',          # Se os decimais usarem ponto (ex: 71.9), troque por decimal='.'
   na_values='-',        # Trata os traços '-' como dados ausentes (NaN)
   encoding='utf-8-sig'  # Mantém os acentos e caracteres especiais
)


# 2. Transforma as colunas dos meses em linhas (Unpivot / Melt)a
df_dataset = pd.melt(
   df,
   id_vars=['Código', 'Posto', 'Ano'],   # Colunas fixas
   var_name='Mês',                        # Coluna para os meses
   value_name='Chuva_mm'                  # Coluna para os valores
)


# 3. Visualiza o resultado
print("--- PRÉVIA DO DATASET (CSV) ---")
print(df_dataset.head(10))


# 4. Salva o dataset final tratado
df_dataset.to_csv('dataset_pluviometrico_limpo.csv', index=False, encoding='utf-8-sig')
print("\nDataset em CSV tratado com sucesso!")
