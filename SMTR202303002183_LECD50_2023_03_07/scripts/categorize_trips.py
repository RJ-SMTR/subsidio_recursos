# Carregar bibliotecas
import pandas as pd
import numpy as np
import basedosdados as bd


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






# 2 - Função check_trips
# Esta função serve para comparar a amostra com as tabelas de viagens completas e conformidade.
# Ela recebe as duas tabelas, o intervalo que deve ser usado no join entre as colunas datetime_partida
# das duas tabelas (em minutos) e o status que as linhas que derem match devem receber.

def check_trips(amostra: pd.DataFrame, query_trip_table: pd.DataFrame, intervalo: int, status: str) -> pd.DataFrame:
    
    # Identificar colunas que iniciam com os prefixos abaixo
    for prefix in ['id_veiculo', 'datetime_partida', 'datetime_chegada', 'servico', 'sentido']:
        amostra_cols = [col for col in amostra.columns if col.startswith(prefix)]
        query_cols = [col for col in query_trip_table.columns if col.startswith(prefix)]
        
        # Erro caso a coluna não exista
        if not amostra_cols or not query_cols:
            raise ValueError(f"O DataFrame deve ter colunas que começam com {prefix}")
        
        # Renomear para um nome padrão
        amostra.rename(columns={amostra_cols[0]: prefix}, inplace=True)
        query_trip_table.rename(columns={query_cols[0]: prefix}, inplace=True)
    
    # Separando linhas que serão classificadas (aquelas em que a coluna status é NaN)
    amostra_nan = amostra[amostra['status'].isna()]
    amostra_not_nan = amostra[~amostra['status'].isna()]
    
    # selecionar apenas as colunas da amostra_nan que serão usadas:
    # Encontre as posições da coluna inicial e final
    start_col = amostra_nan.columns.get_loc('data')
    end_col = amostra_nan.columns.get_loc('status')
    # Selecione as colunas do DataFrame
    amostra_nan = amostra_nan.iloc[:, start_col:end_col + 1]
    
    
    
    # Adicionar uma chave temporária
    amostra_nan['tmp_key'] = amostra_nan['id_veiculo']
    query_trip_table['tmp_key'] = query_trip_table['id_veiculo']

    # Fazer o merge usando a chave temporária
    tabela_comparativa = pd.merge(amostra_nan, query_trip_table, 
                                  on='tmp_key', 
                                  suffixes=('_amostra', '_apurado'))
    
    # Filtrar os resultados com base no critério do intervalo de tempo
    condition = (tabela_comparativa['datetime_partida_apurado'] >= (tabela_comparativa['datetime_partida_amostra'] - pd.Timedelta(minutes=intervalo))) & \
                (tabela_comparativa['datetime_partida_apurado'] <= (tabela_comparativa['datetime_partida_amostra'] + pd.Timedelta(minutes=intervalo)))
        
    tabela_comparativa = tabela_comparativa[condition]
     
    # Remover a chave temporária e outras colunas desnecessárias
    tabela_comparativa.drop(columns=['tmp_key'], inplace=True)
    
    # Atualizar a coluna 'status' baseada nas condições
    tabela_comparativa.loc[tabela_comparativa['id_veiculo_amostra'] == tabela_comparativa['id_veiculo_apurado'], 'status'] = status
    
    # Verificar se existem dados duplicados no cruzamento de dados
    unique_data = tabela_comparativa[['id_veiculo_apurado', 'datetime_partida_apurado']].drop_duplicates()
    
    if tabela_comparativa.shape[0] == unique_data.shape[0]:
        print("Não existem casos duplicados no cruzamento de dados.")
    else:        
        duplicated_rows = tabela_comparativa[tabela_comparativa.duplicated(['id_veiculo_apurado', 'datetime_partida_apurado'])]        
        matching_rows = pd.merge(tabela_comparativa, duplicated_rows[['id_veiculo_apurado', 'datetime_partida_apurado']], 
                                 on=['id_veiculo_apurado', 'datetime_partida_apurado'], how='inner')
        print("\nCasos duplicados encontrados no cruzamento de dados:")
        print(matching_rows)
       
    # formatar tabelas para retornar todas as linhas da amostra que foi inserida
    new_column_names = {
        'id_veiculo': 'id_veiculo_amostra',
        'sentido': 'sentido_amostra',
        'servico': 'servico_amostra',
        'datetime_partida': 'datetime_partida_amostra',
        'datetime_chegada': 'datetime_chegada_amostra'
    }
    
    amostra_not_nan = amostra_not_nan.rename(columns=new_column_names)  

    amostra_nan.drop(columns=['tmp_key'], inplace=True)
    
    amostra_nan = amostra_nan.rename(columns=new_column_names) 
     
    # excluir da amostra_nan aquelas linhas que o status era nan e foram classificadas em tabela_comparativa
    amostra_nan['unique_key'] = amostra_nan['id_veiculo_amostra'].astype(str) + '_' + amostra_nan['datetime_partida_amostra'].astype(str)
    tabela_comparativa['unique_key'] = tabela_comparativa['id_veiculo_amostra'].astype(str) + '_' + tabela_comparativa['datetime_partida_amostra'].astype(str)
    
    
    
    
    # Identificando as linhas que estão apenas em amostra_nan e não em tabela_comparativa
    amostra_nan = amostra_nan.loc[~amostra_nan['unique_key'].isin(tabela_comparativa['unique_key'])]
    
    # Removendo a coluna 'unique_key' se não for mais necessária
    amostra_nan.drop(columns=['unique_key'], inplace=True)
    tabela_comparativa.drop(columns=['unique_key'], inplace=True)
                

    final_data = pd.concat([amostra_not_nan, amostra_nan, tabela_comparativa], axis=0).reset_index(drop=True)
    
    final_data['data'] = final_data['datetime_partida_amostra'].dt.date # atribuir coluna data, caso ela não esteja presente

    return final_data 
# ex: check_trips(amostra, viagem_completa, 10, "Viagem identificada e já paga")
