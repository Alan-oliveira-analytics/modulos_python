import pandas as pd
import numpy as np

def calculo_de_iv_variavel_numerica(tabela_original, variavel_analise, variavel_binaria, formato_bins, formato_label=None):
    #criando o dataframe apenas com as variáveis de correlação
    new_df = tabela_original[[variavel_analise, variavel_binaria]].copy()

    #criando a faixa de valores 
    new_df['faixa_valores'] = pd.cut(new_df[variavel_analise], bins=formato_bins, labels=formato_label)
    
    #soma  de inadimplentes
    calculos_soma_inadimplentes = new_df.groupby(new_df['faixa_valores'], observed=False).sum()
    
    #criação da tabela IV
    tabela_iv = pd.DataFrame({'Eventos': calculos_soma_inadimplentes[variavel_binaria]})
    tabela_iv['nao_eventos'] = new_df['faixa_valores'].value_counts() - tabela_iv['Eventos']
    tabela_iv['total_geral'] = tabela_iv['nao_eventos'] + tabela_iv['Eventos']
    tabela_iv['taxa_evento'] = (tabela_iv['Eventos'] / tabela_iv['Eventos'].sum()) * 100
    tabela_iv['taxa_nao_evento'] = (tabela_iv['nao_eventos'] / tabela_iv['nao_eventos'].sum()) * 100
    tabela_iv['probabilidade_de_ocorrencia'] = (tabela_iv['Eventos'] / tabela_iv['total_geral']) * 100
    tabela_iv['woe'] =tabela_iv['taxa_evento'] / tabela_iv['taxa_nao_evento']
    tabela_iv['iv'] = (tabela_iv['taxa_evento'] - tabela_iv['taxa_nao_evento']) * (np.log(tabela_iv['woe']) / 100)

    return tabela_iv



def calculo_de_iv_variavel_qualitativa(tabela_original, variavel_analise, variavel_binaria):
    #criando o dataframe apenas com as variáveis de correlação
    new_df = tabela_original[[variavel_analise, variavel_binaria]].copy()
    
    #soma  de inadimplentes
    calculos_soma_inadimplentes = new_df.groupby(new_df[variavel_analise], observed=False).sum()
    calculos_soma_nao_inadimplentes = new_df.groupby(new_df[variavel_analise], observed=False).count()
    #criação da tabela IV
    tabela_iv = pd.DataFrame({'Eventos': calculos_soma_inadimplentes[variavel_binaria]})
    tabela_iv['nao_eventos'] = calculos_soma_nao_inadimplentes - calculos_soma_inadimplentes
    tabela_iv['total_geral'] = tabela_iv['nao_eventos'] + tabela_iv['Eventos']
    tabela_iv['taxa_evento'] = (tabela_iv['Eventos'] / tabela_iv['Eventos'].sum()) * 100
    tabela_iv['taxa_nao_evento'] = (tabela_iv['nao_eventos'] / tabela_iv['nao_eventos'].sum()) * 100
    tabela_iv['probabilidade_de_ocorrencia'] = (tabela_iv['Eventos'] / tabela_iv['total_geral']) * 100
    tabela_iv['woe'] =tabela_iv['taxa_evento'] / tabela_iv['taxa_nao_evento']
    tabela_iv['iv'] = (tabela_iv['taxa_evento'] - tabela_iv['taxa_nao_evento']) * (np.log(tabela_iv['woe']) / 100)

    return tabela_iv


def tabela_freq_var_numerica(df, variavel_df, numero_elementos = 2):
    freq_absoluta = df[variavel_df].value_counts().sort_index()
    freq_relativa = (df[variavel_df].value_counts(normalize=True) * 100).sort_index()
    freq_acumulada = np.cumsum(df[variavel_df].value_counts(normalize=True).sort_index() * 100)

    if numero_elementos == 2:
        tabela_frequencia = pd.DataFrame({'Frequência absoluta': freq_absoluta, 'Frequência relativa': {freq_relativa}})
        return tabela_frequencia
    
    tabela_frequencia = pd.DataFrame({'Frequência absoluta': freq_absoluta, 'Frequência relativa': freq_relativa, 'Frequência acumulada': freq_acumulada})
    return tabela_frequencia


def tabela_freq_var_str(df, variavel_df, numero_elementos = 2):
    freq_absoluta = df[variavel_df].value_counts()
    freq_relativa = (df[variavel_df].value_counts(normalize=True) * 100)
    freq_acumulada = np.cumsum(df[variavel_df].value_counts(normalize=True) * 100)

    if numero_elementos == 2:
        tabela_frequencia = pd.DataFrame({'Frequência absoluta': freq_absoluta, 'Frequência relativa': freq_relativa})
        return tabela_frequencia
    
    tabela_frequencia = pd.DataFrame({'Frequência absoluta': freq_absoluta, 'Frequência relativa': freq_relativa, 'Frequência acumulada': freq_acumulada})
    return tabela_frequencia


def tabela_frequencia_bilateral(df, coluna_variavel, coluna_numerica, numero_elementos=2):
    # Soma total de gastos por variavel
    gastos_totais = df.groupby(coluna_variavel)[coluna_numerica].sum().sort_values(ascending=False).reset_index()

    # Cálculo das frequências relativas
    percentual_relativo = (gastos_totais[coluna_numerica] / gastos_totais[coluna_numerica].sum()) * 100

    # Cálculo da frequência acumulada
    percentual_acumulado = percentual_relativo.cumsum()

    # formatações
    gastos_totais['Gasto total (R$)'] = gastos_totais[coluna_numerica].apply(lambda x: f"R${x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    gastos_totais['Percentual sobre o total (%)'] = percentual_relativo.apply(lambda x: f"{x:.2f}%")

    if numero_elementos != 2:
        gastos_totais['Percentual acumulado (%)'] = percentual_acumulado.apply(lambda x: f"{x:.2f}%")

    gastos_totais = gastos_totais.drop(columns=[coluna_numerica])
    
    return gastos_totais
