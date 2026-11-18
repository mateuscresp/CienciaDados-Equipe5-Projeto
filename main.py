import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ==============================================================================
# ETAPA 1: CARREGAMENTO DO DATASET
# ==============================================================================
# Tratamento de decimais com vírgula (,) e valores nulos indicados por hífen (-)
caminho_arquivo = "Dataset APAC.csv"
df = pd.read_csv(caminho_arquivo, decimal=",", na_values="-")

print(f"Dataset carregado com sucesso! Dimensões: {df.shape}")


# ==============================================================================
# ETAPA 2: LIMPEZA, TRATAMENTO DE TEXTO E MESORREGIÕES
# ==============================================================================
# 1. Função para extrair o nome da cidade a partir do Posto Pluviométrico
def extrair_cidade(posto):
    clean = re.sub(r"\(.*?\)", "", str(posto))
    clean = re.sub(r"-\s*PCD", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"-\s*APAC", "", clean, flags=re.IGNORECASE)
    return clean.split("-")[0].strip()


df["Cidade"] = df["Posto"].apply(extrair_cidade)

# 2. Dicionário de mapeamento dos municípios de PE para as 5 Mesorregiões
meso_map = {
    # Metropolitana do Recife
    "Abreu e Lima": "Metropolitana do Recife",
    "Araçoiaba": "Metropolitana do Recife",
    "Cabo": "Metropolitana do Recife",
    "Cabo de Santo Agostinho": "Metropolitana do Recife",
    "Camaragibe": "Metropolitana do Recife",
    "Igarassu": "Metropolitana do Recife",
    "Itamaracá": "Metropolitana do Recife",
    "Ipojuca": "Metropolitana do Recife",
    "Itapissuma": "Metropolitana do Recife",
    "Jaboatão": "Metropolitana do Recife",
    "Jaboatão dos Guararapes": "Metropolitana do Recife",
    "Moreno": "Metropolitana do Recife",
    "Olinda": "Metropolitana do Recife",
    "Paulista": "Metropolitana do Recife",
    "Recife": "Metropolitana do Recife",
    "São Lourenço da Mata": "Metropolitana do Recife",
    # Mata Pernambucana
    "Água Preta": "Mata Pernambucana",
    "Aliança": "Mata Pernambucana",
    "Amaraji": "Mata Pernambucana",
    "Barreiros": "Mata Pernambucana",
    "Belém de Maria": "Mata Pernambucana",
    "Buenos Aires": "Mata Pernambucana",
    "Camutanga": "Mata Pernambucana",
    "Carpina": "Mata Pernambucana",
    "Catende": "Mata Pernambucana",
    "Chã de Alegria": "Mata Pernambucana",
    "Chã Grande": "Mata Pernambucana",
    "Condado": "Mata Pernambucana",
    "Cortês": "Mata Pernambucana",
    "Escada": "Mata Pernambucana",
    "Feira Nova": "Mata Pernambucana",
    "Ferreiros": "Mata Pernambucana",
    "Gameleira": "Mata Pernambucana",
    "Glória do Goitá": "Mata Pernambucana",
    "Goiana": "Mata Pernambucana",
    "Itambé": "Mata Pernambucana",
    "Itaquitinga": "Mata Pernambucana",
    "Jaqueira": "Mata Pernambucana",
    "Joaquim Nabuco": "Mata Pernambucana",
    "Lagoa do Carro": "Mata Pernambucana",
    "Lagoa do Itaenga": "Mata Pernambucana",
    "Lagoa de Itaenga": "Mata Pernambucana",
    "Macaparana": "Mata Pernambucana",
    "Machados": "Mata Pernambucana",
    "Maraial": "Mata Pernambucana",
    "Nazaré da Mata": "Mata Pernambucana",
    "Palmares": "Mata Pernambucana",
    "Paudalho": "Mata Pernambucana",
    "Pombos": "Mata Pernambucana",
    "Primavera": "Mata Pernambucana",
    "Quipapá": "Mata Pernambucana",
    "Ribeirão": "Mata Pernambucana",
    "Rio Formoso": "Mata Pernambucana",
    "São Benedito do Sul": "Mata Pernambucana",
    "São José da Coroa Grande": "Mata Pernambucana",
    "Sirinhaém": "Mata Pernambucana",
    "Tamandaré": "Mata Pernambucana",
    "Timbaúba": "Mata Pernambucana",
    "Tracunhaém": "Mata Pernambucana",
    "Vicência": "Mata Pernambucana",
    "Vitória de Santo Antão": "Mata Pernambucana",
    "Xexéu": "Mata Pernambucana",
    # Agreste Pernambucano
    "Agrestina": "Agreste Pernambucano",
    "Alagoinha": "Agreste Pernambucano",
    "Altinho": "Agreste Pernambucano",
    "Angelim": "Agreste Pernambucano",
    "Águas Belas": "Agreste Pernambucano",
    "Barra de Guabiraba": "Agreste Pernambucano",
    "Belo Jardim": "Agreste Pernambucano",
    "Bezerros": "Agreste Pernambucano",
    "Bom Conselho": "Agreste Pernambucano",
    "Bom Jardim": "Agreste Pernambucano",
    "Bonito": "Agreste Pernambucano",
    "Brejão": "Agreste Pernambucano",
    "Brejo da Madre de Deus": "Agreste Pernambucano",
    "Buíque": "Agreste Pernambucano",
    "Cachoeirinha": "Agreste Pernambucano",
    "Caetés": "Agreste Pernambucano",
    "Calçado": "Agreste Pernambucano",
    "Calçados": "Agreste Pernambucano",
    "Camocim de São Felix": "Agreste Pernambucano",
    "Camocim de São Félix": "Agreste Pernambucano",
    "Canhotinho": "Agreste Pernambucano",
    "Capoeiras": "Agreste Pernambucano",
    "Caruaru": "Agreste Pernambucano",
    "Casinhas": "Agreste Pernambucano",
    "Correntes": "Agreste Pernambucano",
    "Cumaru": "Agreste Pernambucano",
    "Cupira": "Agreste Pernambucano",
    "Frei Miguelinho": "Agreste Pernambucano",
    "Garanhuns": "Agreste Pernambucano",
    "Gravatá": "Agreste Pernambucano",
    "Iati": "Agreste Pernambucano",
    "Ibirajuba": "Agreste Pernambucano",
    "Itaíba": "Agreste Pernambucano",
    "Itaiba": "Agreste Pernambucano",
    "Jataúba": "Agreste Pernambucano",
    "Jatauba": "Agreste Pernambucano",
    "João Alfredo": "Agreste Pernambucano",
    "Jucati": "Agreste Pernambucano",
    "Jupi": "Agreste Pernambucano",
    "Jurema": "Agreste Pernambucano",
    "Lagoa do Ouro": "Agreste Pernambucano",
    "Lagoa dos Gatos": "Agreste Pernambucano",
    "Lajedo": "Agreste Pernambucano",
    "Limoeiro": "Agreste Pernambucano",
    "Orobó": "Agreste Pernambucano",
    "Palmeirina": "Agreste Pernambucano",
    "Panelas": "Agreste Pernambucano",
    "Paranatama": "Agreste Pernambucano",
    "Passira": "Agreste Pernambucano",
    "Pedra": "Agreste Pernambucano",
    "Pesqueira": "Agreste Pernambucano",
    "Poção": "Agreste Pernambucano",
    "Riacho das Almas": "Agreste Pernambucano",
    "Sairé": "Agreste Pernambucano",
    "Salgadinho": "Agreste Pernambucano",
    "Saloá": "Agreste Pernambucano",
    "Sanharó": "Agreste Pernambucano",
    "Santa Cruz do Capibaribe": "Agreste Pernambucano",
    "Santa Maria do Cambucá": "Agreste Pernambucano",
    "Santa Maria do Cambuca": "Agreste Pernambucano",
    "São Bento do Una": "Agreste Pernambucano",
    "São Caetano": "Agreste Pernambucano",
    "São João": "Agreste Pernambucano",
    "São Joaquim do Monte": "Agreste Pernambucano",
    "São Vicente Férrer": "Agreste Pernambucano",
    "São Vicente Ferrer": "Agreste Pernambucano",
    "Surubim": "Agreste Pernambucano",
    "Tacaimbó": "Agreste Pernambucano",
    "Taquaritinga do Norte": "Agreste Pernambucano",
    "Terezinha": "Agreste Pernambucano",
    "Toritama": "Agreste Pernambucano",
    "Tupanatinga": "Agreste Pernambucano",
    "Venturosa": "Agreste Pernambucano",
    "Vertente do Lério": "Agreste Pernambucano",
    "Vertentes": "Agreste Pernambucano",
    # São Francisco Pernambucano
    "Belém de São Francisco": "São Francisco Pernambucano",
    "Cabrobó": "São Francisco Pernambucano",
    "Carnaubeira da Penha": "São Francisco Pernambucano",
    "Floresta": "São Francisco Pernambucano",
    "Jatobá": "São Francisco Pernambucano",
    "Lagoa Grande": "São Francisco Pernambucano",
    "Orocó": "São Francisco Pernambucano",
    "Petrolândia": "São Francisco Pernambucano",
    "Petrolina": "São Francisco Pernambucano",
    "Santa Maria da Boa Vista": "São Francisco Pernambucano",
    "Tacaratu": "São Francisco Pernambucano",
    # Sertão Pernambucano
    "Afogados da Ingazeira": "Sertão Pernambucano",
    "Afrânio": "Sertão Pernambucano",
    "Araripina": "Sertão Pernambucano",
    "Arcoverde": "Sertão Pernambucano",
    "Betânia": "Sertão Pernambucano",
    "Bodocó": "Sertão Pernambucano",
    "Brejinho": "Sertão Pernambucano",
    "Calumbi": "Sertão Pernambucano",
    "Carnaíba": "Sertão Pernambucano",
    "Cedro": "Sertão Pernambucano",
    "Custódia": "Sertão Pernambucano",
    "Dormentes": "Sertão Pernambucano",
    "Exu": "Sertão Pernambucano",
    "Flores": "Sertão Pernambucano",
    "Granito": "Sertão Pernambucano",
    "Ibimirim": "Sertão Pernambucano",
    "Iguaracy": "Sertão Pernambucano",
    "Iguaraci": "Sertão Pernambucano",
    "Inajá": "Sertão Pernambucano",
    "Ingazeira": "Sertão Pernambucano",
    "Ipubi": "Sertão Pernambucano",
    "Itacuruba": "Sertão Pernambucano",
    "Itapetim": "Sertão Pernambucano",
    "Manari": "Sertão Pernambucano",
    "Mirandiba": "Sertão Pernambucano",
    "Moreilândia": "Sertão Pernambucano",
    "Ouricuri": "Sertão Pernambucano",
    "Parnamirim": "Sertão Pernambucano",
    "Quixaba": "Sertão Pernambucano",
    "Salgueiro": "Sertão Pernambucano",
    "Santa Cruz": "Sertão Pernambucano",
    "Santa Filomena": "Sertão Pernambucano",
    "Santa Cruz da Baixa Verde": "Sertão Pernambucano",
    "Santa Cruz da Venerada": "Sertão Pernambucano",
    "Santa Terezinha": "Sertão Pernambucano",
    "São José do Belmonte": "Sertão Pernambucano",
    "São José do Egito": "Sertão Pernambucano",
    "Serra Talhada": "Sertão Pernambucano",
    "Serrita": "Sertão Pernambucano",
    "Sertânia": "Sertão Pernambucano",
    "Solidão": "Sertão Pernambucano",
    "Tabira": "Sertão Pernambucano",
    "Terra Nova": "Sertão Pernambucano",
    "Trindade": "Sertão Pernambucano",
    "Triunfo": "Sertão Pernambucano",
    "Tuparetama": "Sertão Pernambucano",
    "Verdejante": "Sertão Pernambucano",
}

df["Mesorregiao"] = df["Cidade"].map(meso_map)

# 3. Garantir a conversão numérica dos 12 meses
months = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]

for m in months:
    df[m] = df[m].astype(str).str.strip().str.replace(",", ".")
    df[m] = pd.to_numeric(df[m], errors="coerce")


# ==============================================================================
# ETAPA 3: UNPIVOT / REESTRUTURAÇÃO PARA FORMATO LONGO (TIDY DATA)
# ==============================================================================
df_long = df.melt(
    id_vars=["Código", "Posto", "Cidade", "Mesorregiao", "Ano"],
    value_vars=months,
    var_name="Mes",
    value_name="Pluviometria",
)

# Mapeamento do mês para número (1 a 12)
month_map = {m: i + 1 for i, m in enumerate(months)}
df_long["Mes_Num"] = df_long["Mes"].map(month_map)

print(
    f"Dataset reestruturado para formato Long! Total de {len(df_long)} registros."
)


# ==============================================================================
# ETAPA 4: ANÁLISE DE DADOS AUSENTES (DATA QUALITY)
# ==============================================================================
df_long["Ausente"] = df_long["Pluviometria"].isna()

missing_df = (
    df_long.groupby(["Mesorregiao", "Mes", "Mes_Num"])["Ausente"]
    .mean()
    .reset_index()
)
missing_df["Porcentagem_Ausente"] = missing_df["Ausente"] * 100
missing_df = missing_df.sort_values(by=["Mesorregiao", "Mes_Num"])


# ==============================================================================
# ETAPA 5: VISUALIZAÇÃO E GRÁFICOS
# ==============================================================================
sns.set_theme(style="whitegrid")

# --- 5.1. Sazonalidade da Pluviometria por Mesorregião ---
plt.figure(figsize=(12, 5))
sns.lineplot(
    data=df_long.sort_values("Mes_Num"),
    x="Mes",
    y="Pluviometria",
    hue="Mesorregiao",
    marker="o",
    errorbar=None,
    linewidth=2.5,
    sort=False,
)
plt.title(
    "Sazonalidade da Pluviometria por Mesorregião em Pernambuco",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Mês", fontsize=11)
plt.ylabel("Precipitação Média (mm)", fontsize=11)
plt.xticks(rotation=45)
plt.legend(
    title="Mesorregião", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True
)
plt.tight_layout()
plt.show()

# --- 5.2. Volume Médio Mensal de Chuva por Mesorregião ---
plt.figure(figsize=(10, 4.5))
avg_meso = (
    df_long.groupby("Mesorregiao")["Pluviometria"]
    .mean()
    .reset_index()
    .sort_values(by="Pluviometria", ascending=False)
)

ax = sns.barplot(
    data=avg_meso,
    x="Pluviometria",
    y="Mesorregiao",
    hue="Mesorregiao",
    palette="Blues_r",
    legend=False,
)
ax.bar_label(ax.containers[0], fmt="%.1f mm", padding=5, fontsize=10)

plt.title(
    "Volume Médio Mensal de Chuva por Mesorregião (mm)",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Chuva Média (mm)", fontsize=11)
plt.ylabel("")
plt.xlim(0, avg_meso["Pluviometria"].max() * 1.15)
plt.tight_layout()
plt.show()

# --- 5.3. Heatmap Pluviométrico (Mesorregião vs Mês) ---
plt.figure(figsize=(12, 5))
pivot_meso = (
    df_long.groupby(["Mesorregiao", "Mes_Num"])["Pluviometria"]
    .mean()
    .unstack()
)
pivot_meso.columns = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]
pivot_meso = pivot_meso.loc[avg_meso["Mesorregiao"]]

sns.heatmap(
    pivot_meso,
    cmap="YlGnBu",
    annot=True,
    fmt=".1f",
    linewidths=0.5,
    cbar_kws={"label": "Precipitação (mm)"},
)
plt.title(
    "Heatmap Pluviométrico (mm): Mesorregião vs Mês",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Mês", fontsize=11)
plt.ylabel("")
plt.tight_layout()
plt.show()

# --- 5.4. Distribuição Individual (Stripplot) por Mesorregião ---
df_valid = df_long.dropna(subset=["Pluviometria"]).copy()

plt.figure(figsize=(15, 7))
sns.stripplot(
    data=df_valid,
    x="Mes",
    y="Pluviometria",
    hue="Mesorregiao",
    order=months,
    dodge=True,
    jitter=0.2,
    size=3.5,
    alpha=0.6,
)
plt.title(
    "Distribuição Individual das Medições Pluviométricas por Mês e Mesorregião",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Mês", fontsize=11)
plt.ylabel("Precipitação (mm)", fontsize=11)
plt.xticks(rotation=45)
plt.legend(
    title="Mesorregião", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True
)
plt.tight_layout()
plt.show()

# --- 5.5. Heatmap da Taxa de Ausência de Dados (%) ---
pivot_missing = missing_df.pivot(
    index="Mesorregiao", columns="Mes_Num", values="Porcentagem_Ausente"
)
pivot_missing.columns = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]

plt.figure(figsize=(12, 5))
sns.heatmap(
    pivot_missing,
    cmap="Reds",
    annot=True,
    fmt=".1f",
    cbar_kws={"label": "% Dados Ausentes"},
    linewidths=0.5,
)
plt.title(
    "Porcentagem de Ausência de Dados Pluviométricos por Mês e Mesorregião",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Mês", fontsize=11)
plt.ylabel("")
plt.tight_layout()
plt.show()

# --- 5.6. Comparação Pluviométrica: Julho vs Dezembro ---
df_jul_dez = (
    df_long[df_long["Mes"].isin(["Julho", "Dezembro"])]
    .dropna(subset=["Pluviometria"])
    .copy()
)

plt.figure(figsize=(8, 6))
sns.boxplot(
    data=df_jul_dez,
    x="Mes",
    y="Pluviometria",
    hue="Mes",
    order=["Julho", "Dezembro"],
    palette={"Julho": "#3498db", "Dezembro": "#e74c3c"},
    legend=False,
    showmeans=True,
    meanprops={
        "marker": "o",
        "markerfacecolor": "white",
        "markeredgecolor": "black",
        "markersize": "8",
    },
)
plt.title(
    "Comparação Pluviométrica: Julho vs Dezembro em PE",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Mês", fontsize=12)
plt.ylabel("Precipitação (mm)", fontsize=12)
plt.tight_layout()
plt.show()