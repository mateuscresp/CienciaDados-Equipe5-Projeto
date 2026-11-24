"""Gráficos reproduzíveis da EDA e dos experimentos APAC/KNN (Issue #6).
Execute da raiz: python src/eda_graficos.py
Não modifica data/raw. Resultados de experimentos são uma fotografia do CSV fornecido.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from data import carregar, MESES

FIG = ROOT / 'results' / 'figuras'
FIG.mkdir(parents=True, exist_ok=True)


def salvar(nome):
    plt.tight_layout()
    plt.savefig(FIG / nome, dpi=150, bbox_inches='tight')
    plt.close()


def graficos(df, exp):
    sns.set_theme(style='whitegrid')
    ordem = df['Mesorregiao'].value_counts().index
    cont = df['Mesorregiao'].value_counts().reindex(ordem)
    fig, ax = plt.subplots(figsize=(10,5))
    b = ax.barh(cont.index[::-1], (100*cont/len(df)).values[::-1])
    ax.bar_label(b,fmt='%.1f%%',padding=3)
    ax.set_xlim(0, max((100*cont/len(df)).values)*1.2)
    ax.set_xlabel('Percentual de registros (%)'); ax.set_title('Distribuição das mesorregiões — base rotulada atual')
    salvar('eda_distribuicao_classes.png')

    longo=df.melt(id_vars=['Mesorregiao'],value_vars=MESES,var_name='Mes',value_name='Chuva_mm').dropna(subset=['Chuva_mm'])
    fig,ax=plt.subplots(figsize=(14,5));sns.boxplot(data=longo,x='Mes',y='Chuva_mm',order=MESES,showfliers=False,ax=ax)
    ax.tick_params(axis='x',rotation=50);ax.set_title('Precipitação por mês (sem pontos extremos na visualização)');ax.set_ylabel('Precipitação (mm)')
    salvar('eda_boxplot_meses.png')

    fig,ax=plt.subplots(figsize=(12,6));sns.boxplot(data=longo,x='Mesorregiao',y='Chuva_mm',order=ordem,showfliers=False,ax=ax)
    ax.tick_params(axis='x',rotation=20);ax.set_title('Precipitação mensal por mesorregião (todos os meses)');ax.set_ylabel('Precipitação (mm)')
    salvar('eda_boxplot_mesorregioes.png')

    # Foco em todos os meses, preservando mesorregiões para não esconder a sazonalidade regional.
    fig,ax=plt.subplots(figsize=(17,7));sns.boxplot(data=longo,x='Mes',y='Chuva_mm',hue='Mesorregiao',order=MESES,showfliers=False,ax=ax)
    ax.tick_params(axis='x',rotation=45);ax.legend(loc='upper right',fontsize=8,title='Mesorregião');ax.set_title('Precipitação por mês × mesorregião');ax.set_ylabel('Precipitação (mm)')
    salvar('eda_boxplot_mes_regiao.png')

    corr=df[MESES].corr()
    fig,ax=plt.subplots(figsize=(10,8));sns.heatmap(corr,annot=True,fmt='.2f',cmap='coolwarm',center=0,vmin=-1,vmax=1,ax=ax)
    ax.set_title('Correlação de Pearson entre meses (pares disponíveis)')
    salvar('eda_correlacao_meses.png')

    fatores=[('max_ausentes','Limite de meses ausentes'),('imputador','Imputação'),('scaler','Normalização'),('metrica','Distância'),('pesos','Pesos'),('k','Número de vizinhos (k)')]
    for c,ttl in fatores:
        x=exp.copy()
        x[c]=x[c].fillna('Sem limite').astype(str)
        a=x.groupby(c)['f1_macro'].agg(['mean','max','std','count']).sort_values('mean',ascending=False)
        fig,ax=plt.subplots(figsize=(max(8,1.2*len(a)),5))
        bars=ax.bar(a.index,a['mean'],yerr=a['std'],capsize=5,alpha=.85,label='Média das configurações ± desvio entre configurações')
        ax.scatter(range(len(a)),a['max'],marker='D',color='black',label='Máximo observado',zorder=4)
        ax.set_ylabel('F1 macro');ax.set_xlabel(c);ax.set_title(f'F1 macro por fator: {ttl}')
        ax.legend(fontsize=8);ax.tick_params(axis='x',rotation=20)
        # média do fator agrega hiperparâmetros distintos; barras de erro são desvio entre configurações, NÃO folds.
        salvar(f'experimentos_fator_{c}.png')
    return cont, longo, corr


def main():
    csvs=sorted((ROOT/'data/raw').glob('*.csv'))
    if len(csvs)!=1: raise RuntimeError(f'Esperado 1 CSV bruto, encontrados {len(csvs)}')
    df=carregar(str(csvs[0]));exp=pd.read_csv(ROOT/'results/experimentos_knn.csv')
    graficos(df,exp)
    print(f'Gráficos salvos em: {FIG}')
if __name__=='__main__':main()
