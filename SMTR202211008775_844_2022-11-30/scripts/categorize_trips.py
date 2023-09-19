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
    viagem_completa = viagem_completa[['servico_informado', 'id_veiculo', 'sentido', 'datetime_partida', 'datetime_chegada']]
    
    # Separando linhas com status NaN e não NaN
    amostra_nan = amostra[amostra['status'].isna()]
    amostra_not_nan = amostra[~amostra['status'].isna()]
       
    
    # 1. Adicionar uma chave temporária
    amostra_nan['tmp_key'] = amostra_nan['id_veiculo']
    viagem_completa['tmp_key'] = viagem_completa['id_veiculo']

    # 2. Fazendo o merge usando a chave temporária
    tabela_comparativa = pd.merge(amostra_nan, viagem_completa, on='tmp_key', suffixes=('_amostra', '_apurada'))

    # 3. Filtrar os resultados com base no critério do intervalo de tempo
    condition = (tabela_comparativa['datetime_partida_apurada'] >= (tabela_comparativa['datetime_partida_amostra'] - pd.Timedelta(minutes=intervalo))) & \
                (tabela_comparativa['datetime_partida_apurada'] <= (tabela_comparativa['datetime_partida_amostra'] + pd.Timedelta(minutes=intervalo)))

    tabela_comparativa = tabela_comparativa[condition]

    # Removendo a chave temporária e outras colunas desnecessárias
    tabela_comparativa.drop(columns=['tmp_key'], inplace=True)

    # Atualizar a coluna 'status' baseada nas condições
    tabela_comparativa.loc[tabela_comparativa['id_veiculo_amostra'] == tabela_comparativa['id_veiculo_apurada'], 'status'] = 'O veículo existe e operou na linha indicada pelo recurso'
    tabela_comparativa.loc[tabela_comparativa['id_veiculo_amostra'] != tabela_comparativa['id_veiculo_apurada'], 'status'] = 'Viagem encontrada no serviço, mas com veículo diferente'

    # Verificar se existem dados duplicados no cruzamento de dados
    unique_data = tabela_comparativa[['id_veiculo_apurada', 'datetime_partida_apurada']].drop_duplicates()
    
    if tabela_comparativa.shape[0] == unique_data.shape[0]:
        print("Não existem casos duplicados no cruzamento de dados.")
    else:        
        duplicated_rows = tabela_comparativa[tabela_comparativa.duplicated(['id_veiculo_apurada', 'datetime_partida_apurada'])]        
        matching_rows = pd.merge(tabela_comparativa, duplicated_rows[['id_veiculo_apurada', 'datetime_partida_apurada']], on=['id_veiculo_apurada', 'datetime_partida_apurada'], how='inner')
        print("\nCasos duplicados encontrados no cruzamento de dados:")
        print(matching_rows)
      
       
    # juntar tudo em uma tabela só
    
    new_column_names = {
        'id_veiculo': 'id_veiculo_amostra',
        'sentido': 'sentido_amostra',
        'datetime_partida': 'datetime_partida_amostra',
        'datetime_chegada': 'datetime_chegada_amostra'
    }
    
    amostra_not_nan = amostra_not_nan.rename(columns=new_column_names) 
        
    final_data = pd.concat([tabela_comparativa, amostra_not_nan], axis=0).reset_index(drop=True)
    
    # Adicionar dados que ainda têm o status NaN
    mask_datetime = amostra['datetime_partida'].isin(final_data['datetime_partida_amostra'])
    mask_veiculo = amostra['id_veiculo'].isin(final_data['id_veiculo_amostra'])

    # colocar nomes corretos das colunas
    tabela_sem_status = amostra[~(mask_datetime & mask_veiculo)]
    tabela_sem_status	
     
    # join
    tabela_sem_status = tabela_sem_status.rename(columns=new_column_names)      
    final_data = pd.concat([final_data, tabela_sem_status], axis=0).reset_index(drop=True)
    
    return final_data

# Exemplo de uso:
# resultado_final = check_complete_trips(amostra_df, viagem_completa_df, 10)
