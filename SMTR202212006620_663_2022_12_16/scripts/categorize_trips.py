# Carregar bibliotecas
import pandas as pd
import numpy as np


# 1 - Classifica as viagens do gabarito do mesmo veículo e com horários e dias sobrepostos
# como "Viagem inválida - sobreposição de viagem"

def remove_overlapping_trips(df: pd.DataFrame) -> pd.DataFrame:
    # Fazendo uma cópia do dataframe original para evitar mudanças indesejadas no dataframe original
    df_processed = df.copy()
    
    # Converter as colunas para o tipo datetime
    df_processed['datetime_partida'] = pd.to_datetime(df_processed['datetime_partida'])
    df_processed['datetime_chegada'] = pd.to_datetime(df_processed['datetime_chegada'])
    df_processed['id_veiculo'] = df_processed['id_veiculo'].astype(str)
    df_processed['servico'] = df_processed['servico'].astype(str)
    df_processed['status'] = np.nan

    # Verificação de sobreposição
    for index, row in df_processed.iterrows():
        mask = (
            (df_processed['id_veiculo'] == row['id_veiculo']) & 
            (df_processed['datetime_partida'] <= row['datetime_chegada']) & 
            (df_processed['datetime_chegada'] >= row['datetime_partida']) &
            (df_processed.index != index)
        )
    
        overlapping_rows = df_processed[mask]
    
        if overlapping_rows.shape[0] > 0:
            for overlapping_index in overlapping_rows.index:
                if df_processed.at[overlapping_index, 'datetime_partida'] == row['datetime_partida']:
                    if overlapping_index > index:
                        df_processed.at[overlapping_index, 'status'] = 'Viagem inválida - sobreposição de viagem'
                elif df_processed.at[overlapping_index, 'datetime_partida'] == row['datetime_chegada']:
                    df_processed.at[index, 'status'] = np.nan
                elif df_processed.at[overlapping_index, 'datetime_partida'] < row['datetime_chegada'] and df_processed.at[overlapping_index, 'datetime_chegada'] > row['datetime_partida']:
                    if overlapping_index > index:
                        df_processed.at[overlapping_index, 'status'] = 'Viagem inválida - sobreposição de viagem'
                        
    return df_processed

# 2 - Classifica as viagens caso elas estejam na tabela viagem_completa

def check_complete_trips(amostra: pd.DataFrame, viagem_completa: pd.DataFrame, intervalo: int) -> pd.DataFrame:
    # Filtrando as colunas necessárias
    viagem_completa = viagem_completa[['servico_informado','id_veiculo','sentido','datetime_partida','datetime_chegada']]
    
    # 1. Adicionar uma chave temporária
    amostra['tmp_key'] = amostra['id_veiculo']
    viagem_completa['tmp_key'] = viagem_completa['id_veiculo']

    # 2. Fazendo o merge usando a chave temporária
    tabela_comparativa = pd.merge(amostra, viagem_completa, on='tmp_key', suffixes=('_amostra', '_apurada'))

    # 3. Filtrar os resultados com base no critério do intervalo de tempo
    condition = (tabela_comparativa['datetime_partida_apurada'] >= (tabela_comparativa['datetime_partida_amostra'] - pd.Timedelta(minutes=intervalo))) & \
                (tabela_comparativa['datetime_partida_apurada'] <= (tabela_comparativa['datetime_partida_amostra'] + pd.Timedelta(minutes=intervalo)))

    tabela_comparativa = tabela_comparativa[condition]

    # Removendo a chave temporária e outras colunas desnecessárias
    tabela_comparativa.drop(columns=['tmp_key'], inplace=True)

    # Atualizar a coluna 'status' baseada nas condições
    tabela_comparativa.loc[tabela_comparativa['id_veiculo_amostra'] == tabela_comparativa['id_veiculo_apurada'], 'status'] = 'O veículo existe e operou na linha indicada pelo recurso'
    tabela_comparativa.loc[tabela_comparativa['id_veiculo_amostra'] != tabela_comparativa['id_veiculo_apurada'], 'status'] = 'Viagem encontrada no serviço, mas com veículo diferente'

    return tabela_comparativa

# Exemplo de uso:
# resultado = check_complete_trips(amostra_df, viagem_completa_df, 10)

