### --- 1. Carregar bibliotecas --- ###
from pathlib import Path 
from geopy.distance import geodesic
import numpy as np
import pandas as pd


current_path = Path().resolve().parent
parent_path = current_path.parent

paths = dict()
paths["data_processing"] = current_path 
paths["queries"] = parent_path / 'queries'
paths["dataviz"] = parent_path / 'dataviz'


import re
from treat_data import *
from query import *


### --- 2. Função de verificação de viagens sobrepostas --- ###

def remove_overlapping_trips(df: pd.DataFrame) -> pd.DataFrame:
    
    """
    Classifica o status das viagens da amostra como "Viagem inválida - sobreposição de viagem" nos casos 
    em que um mesmo veículo tem duas viagens no mesmo intervalo de tempo.
    
    Parâmetros:
    df (dataframe): Dataframe contendo a amostra.
    
    Retorna:
    dataframe: Um dataframe com a coluna status preenchida para casos de viagens sobrepostas.
    
    Exemplos:
    >>> remove_overlapping_trips(amostra)
    
    Notas:
    Caso o mesmo veículo inicie uma viagem no mesmo minuto do término da viagem anterior, não é considerada sobreposição de viagem.
    """
    
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
                        df_processed.at[overlapping_index, 'status'] = 'Viagem duplicada na amostra'
                elif df_processed.at[overlapping_index, 'datetime_partida'] == row['datetime_chegada']:
                    df_processed.at[index, 'status'] = np.nan
                elif df_processed.at[overlapping_index, 'datetime_partida'] < row['datetime_chegada'] and df_processed.at[overlapping_index, 'datetime_chegada'] > row['datetime_partida']:
                    if overlapping_index > index:
                        df_processed.at[overlapping_index, 'status'] = 'Viagem duplicada na amostra'
    
               
    return df_processed


### --- 3. Função de classificação de viagens --- ###

def check_trips(amostra: pd.DataFrame, query_trip_table: pd.DataFrame, status: str) -> pd.DataFrame:
        
    """
    Verifica quais viagens do dataframe query_trip_table têm o datetime_partida dentro de um intervalo
    de + ou - 10 minutos do datetime do dataframe amostra. Para viagens com duração menor do que 10 minutos,
    o intervalo de comparação é de + ou - 5 minutos. A função também classifica o status de acordo com a string
    que é passada no argumento status da função.
    
    Parâmetros:
    amostra (dataframe): Dataframe contendo a amostra.
    query_trip_table (dataframe): Dataframe contendo viagens completas ou viagem conformidade.
    status(str): Valor que deve ser atribuido na coluna status caso a condição seja satisfeita.
    
    Retorna:
    dataframe: Um dataframe com a coluna status preenchida para casos de viagens encontradas.
    
    Exemplos:
    >>> check_trips(amostra, viagem_completa, "Viagem circular identificada e já paga")
    """        
        
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
    
    cols = list(amostra_nan.columns)
    cols.insert(0, cols.pop(cols.index('data')))
    amostra_nan = amostra_nan[cols]

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
    
    
    # Definir o intervalo do join:
    # caso a viagem seja muito curta e dure menos de 10 minutos, o join será feito com uma margem de 5 minutos, e não 10 minutos
    condition = (tabela_comparativa['datetime_chegada_amostra'] - tabela_comparativa['datetime_partida_amostra'] < pd.Timedelta(minutes=10))
    tabela_comparativa['intervalo'] = np.where(condition, 5, 10)
    
    condition = (tabela_comparativa['datetime_partida_apurado'] >= 
                (tabela_comparativa['datetime_partida_amostra'] - 
                pd.to_timedelta(tabela_comparativa['intervalo'], unit="m"))) & \
                (tabela_comparativa['datetime_partida_apurado'] <= 
                (tabela_comparativa['datetime_partida_amostra'] + 
                pd.to_timedelta(tabela_comparativa['intervalo'], unit="m")))

    tabela_comparativa = tabela_comparativa[condition]  
    
    
    
    # Remover a chave temporária e outras colunas desnecessárias
    tabela_comparativa.drop(columns=['tmp_key'], inplace=True)

    # Atualizar a coluna 'status' baseada nas condições
    condition = (tabela_comparativa['id_veiculo_amostra'] == tabela_comparativa['id_veiculo_apurado']) & \
            (tabela_comparativa['servico_amostra'] == tabela_comparativa['servico_apurado'])

    tabela_comparativa.loc[condition, 'status'] = status
    
    condition = (tabela_comparativa['id_veiculo_amostra'] == tabela_comparativa['id_veiculo_apurado']) & \
            (tabela_comparativa['servico_amostra'] != tabela_comparativa['servico_apurado'])

    tabela_comparativa.loc[condition, 'status'] = status + " para serviço diferente da amostra"
        

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

    final_data.drop(['intervalo', 'data_amostra'], axis=1, inplace=True)


    return final_data 



### --- 4. Função de classificação de dados de GPS --- ###

def check_gps(row, df_check):
    """
    Verifica se o veículo teve sinal de GPS no momento da viagem e retorna o status informando
    se ele operou no serviço correto ou se não houve sinal de GPS no momento da viagem.
        
    Parâmetros:
    row: Linha do dataframe da amostra com as viagens não identificadas.
    df_check (dataframe): Dataframe contendo os dados de GPS.   

    """     
    
    # Filtrar df_check pelo id_veiculo e pelo intervalo
    filtered_df = df_check[
        (df_check['id_veiculo'] == row['id_veiculo_amostra']) & 
        (df_check['timestamp_gps'] >= row['datetime_partida_amostra']) & 
        (df_check['timestamp_gps'] <= row['datetime_chegada_amostra'])
    ]
    
    # Identificar serviços
    unique_servicos = filtered_df['servico'].unique()
    servico_apurado = ', '.join(unique_servicos)

    if not filtered_df.empty and np.isnan(row['status']):
        if all(filtered_df['servico'] == row['servico_amostra']):
            return ("Sinal de GPS encontrado para o veículo operando no mesmo serviço da amostra", servico_apurado)
        else:
            return ("Sinal de GPS encontrado para o veículo operando em serviço diferente da amostra", servico_apurado)
    else:
        return ("Sinal de GPS não encontrado para o veículo no horário da viagem", np.nan)


### --- 5. Função de classificação de viagens circulares --- ###

# Classificar meias viagens da amostra

def check_circular_trip(viagens_circulares_sem_status, viagem_completa, viagem_conformidade):
    """ 
    Esta função deve ser usada apenas nos casos em que a amostra recebida contém dados de uma viagem
    circular, mas está separada em ida e volta. Ou seja, a amostra (viagens_circulares_sem_status)
    deve conter o sentido "I" ou "V", enquanto os dados de viagem_completa e viagem_conformidade
    devem conter o sentido "C". Esta função faz a equivalência entre as viagens da amostra e as
    viagens completas e de conformidade.
    
    Parâmetros:
    viagens_circulares_sem_status (dataframe): Dataframe da amostra com as viagens não identificadas.
    viagem_completa (dataframe): Dataframe contendo os dados das viagens completas.
    viagem_conformidade (dataframe): Dataframe contendo os dados das viagens conformidade.
    """  
    
    # Setar tipos de dados das colunas
    viagens_circulares_sem_status['datetime_partida_amostra'] = pd.to_datetime(viagens_circulares_sem_status['datetime_partida_amostra'])
    viagens_circulares_sem_status['id_veiculo_amostra'] = viagens_circulares_sem_status['id_veiculo_amostra'].astype(str)
    
    viagem_completa['datetime_partida'] = pd.to_datetime(viagem_completa['datetime_partida'])
    viagem_completa['datetime_chegada'] = pd.to_datetime(viagem_completa['datetime_chegada'])
    
    viagem_conformidade['datetime_partida'] = pd.to_datetime(viagem_conformidade['datetime_partida'])
    viagem_conformidade['datetime_chegada'] = pd.to_datetime(viagem_conformidade['datetime_chegada'])        
    
    
    for index, row in viagens_circulares_sem_status.iterrows():
        # Primeira verificação com viagem_completa
        mask_completa = (
            (viagem_completa['id_veiculo'] == row['id_veiculo_amostra']) &
            (viagem_completa['data'] == row['data']) & 
            (viagem_completa['datetime_partida'] <= row['datetime_partida_amostra']) & 
            (viagem_completa['datetime_chegada'] >= row['datetime_partida_amostra'])
        )

        # Se existir uma linha correspondente, atualize o status e copie os valores, depois continue para a próxima iteração
        if viagem_completa[mask_completa].shape[0] > 0:
            viagens_circulares_sem_status.loc[index, 'status'] = "Viagem identificada e já paga"
            matching_row = viagem_completa[mask_completa].iloc[0]
            viagens_circulares_sem_status.loc[index, ['data_apurado', 'id_veiculo_apurado', 'servico_apurado', 
                                            'sentido_apurado', 'datetime_partida_apurado', 
                                            'datetime_chegada_apurado']] = matching_row[['data', 'id_veiculo', 
                                                                                        'servico', 'sentido', 
                                                                                        'datetime_partida', 
                                                                                        'datetime_chegada']].values
            
            
            continue
        
        # Segunda verificação com viagem_conformidade se a primeira falhar
        mask_conformidade = (
            (viagem_conformidade['id_veiculo'] == row['id_veiculo_amostra']) &
            (viagem_conformidade['data'] == row['data']) & 
            (viagem_conformidade['datetime_partida'] <= row['datetime_partida_amostra']) & 
            (viagem_conformidade['datetime_chegada'] >= row['datetime_partida_amostra'])
        )
        
        # Se existir uma linha correspondente, atualize o status e copie os valores
        if viagem_conformidade[mask_conformidade].shape[0] > 0:
            viagens_circulares_sem_status.loc[index, 'status'] = "Viagem inválida - Não atingiu % de GPS ou trajeto correto"
            matching_row = viagem_conformidade[mask_conformidade].iloc[0]
            viagens_circulares_sem_status.loc[index, ['data_apurado', 'id_veiculo_apurado', 'servico_apurado', 
                                            'sentido_apurado', 'datetime_partida_apurado', 
                                            'datetime_chegada_apurado']] = matching_row[['data', 'id_veiculo', 
                                                                                        'servico', 'sentido', 
                                                                                        'datetime_partida', 
                                                                                        'datetime_chegada']].values
            
            
    return viagens_circulares_sem_status




### --- 6. Função de classificação de sinais de GPS no raio de 500m dos pontos inicial e final da viagem --- ###

def check_start_end_gps(viagens_gps_classificadas: pd.DataFrame) -> pd.DataFrame:
    
    status_check = 'Sinal de GPS encontrado para o veículo operando no mesmo serviço da amostra'
    viagens_com_gps = viagens_gps_classificadas[viagens_gps_classificadas['status'] == status_check]
    viagens_ja_classificadas = viagens_gps_classificadas[viagens_gps_classificadas['status'] != status_check]

    dados_shape = query_planned_trips(viagens_com_gps,
                                    include_shape_direction = False,
                                    geometry_data = True)        
            
    dados_shape['servico'] = dados_shape['servico'].astype(str)
        
    # Acessar e tratar dados de GPS
    filtro_gps = viagens_com_gps[['id_veiculo_amostra','data']].drop_duplicates(subset=['id_veiculo_amostra', 'data'])  
    
    dados_gps = query_gps(viagens_com_gps)
    dados_gps = treat_gps(dados_gps)

    dados_gps['data'] = dados_gps['timestamp_gps'].dt.date.astype(str)
    dados_gps['id_veiculo'] = dados_gps['id_veiculo'].astype(str)
    filtro_gps['data'] = filtro_gps['data'].astype(str)
    filtro_gps['id_veiculo_amostra'] = filtro_gps['id_veiculo_amostra'].astype(str)

    dados_gps = dados_gps.merge(filtro_gps, 
                                left_on=['data','id_veiculo'], 
                                right_on=['data','id_veiculo_amostra'], 
                                how='inner')
          
            
    # Acessar e tratar dados do shape/viagem_planejada
    filtro_shape = viagens_com_gps[['servico_amostra','data']].drop_duplicates(subset=['servico_amostra', 
                                                                                    'data']) 

    dados_shape['data'] = dados_shape['data'].astype(str)
    dados_shape['servico'] = dados_shape['servico'].astype(str)
    filtro_shape['data'] = filtro_shape['data'].astype(str)
    filtro_shape['servico_amostra'] = filtro_shape['servico_amostra'].astype(str)
        
    # juntar dados de GPS com os respectivos ponto final/inicial
    dados_shape = dados_shape.merge(filtro_shape, 
                                left_on=['data','servico'], 
                                right_on=['data','servico_amostra'], 
                                how='inner')
     
    
    # Verificar pontos nos raios de 500m inicial e final   
    merged_data = pd.merge(dados_shape, 
                        dados_gps, on=['data', 'servico'], how='inner')  
    
       
    # converter formato dos pontos
    def point_to_tuple(point_string):
        # Extrair os valores numéricos
        coords = re.findall(r"[-+]?\d*\.\d+|\d+", point_string)
        # Retorna as coordenadas como uma tupla de floats
        return (float(coords[1]), float(coords[0]))  # conversão para (lat, lon)

    merged_data['end_pt'] = merged_data['end_pt'].apply(point_to_tuple)
    merged_data['start_pt'] = merged_data['start_pt'].apply(point_to_tuple)    
    merged_data['posicao_veiculo_geo'] = merged_data['posicao_veiculo_geo'].apply(point_to_tuple)

    # Função para verificar se as coordenadas estão dentro do raio de 500m
    def is_within_radius(point1, point2, radius):
        distance = geodesic(point1, point2).meters
        return 1 if distance <= radius else 0

    # Criar colunas que indicam se o sinal de GPS está dentro do raio de 500m

   
    merged_data['check_start_pt'] = merged_data.apply(lambda row: is_within_radius(row['start_pt'], row['posicao_veiculo_geo'], 500), axis=1)
    merged_data['check_end_pt'] = merged_data.apply(lambda row: is_within_radius(row['end_pt'], row['posicao_veiculo_geo'], 500), axis=1)


    # Identificar a quais viagens pertencem os dados de GPS capturados
    # Dados capturados no raio de 500m do ponto de partida:
    partida = []  

    for index, row in viagens_com_gps.iterrows():
        mask = (merged_data['id_veiculo'] == row['id_veiculo_amostra']) & (merged_data['timestamp_gps'] > row['datetime_partida_amostra']) & (merged_data['timestamp_gps'] < (row['datetime_partida_amostra'] + pd.Timedelta(minutes=5)))
        filtered_data = merged_data[mask]
        
        # Agregar dados
        aggregated_data = filtered_data.groupby('id_veiculo').agg({
            'check_start_pt': 'sum',
            'check_end_pt': 'sum',
            'timestamp_gps': 'mean'
        }).reset_index()
        
        partida.append(aggregated_data)

    # Concatenar ao final do loop
    df_partida = pd.concat(partida) 

    df_partida = df_partida.rename(columns={
    'check_start_pt': 'check_start_pt_partida',
    'check_end_pt': 'check_end_pt_partida',
    'timestamp_gps': 'timestamp_gps_partida'
    })


    # Dados capturados no raio de 500m do ponto de chegada:
    chegada = []

    for index, row in viagens_com_gps.iterrows():
        mask = (merged_data['id_veiculo'] == row['id_veiculo_amostra']) & (merged_data['timestamp_gps'] < row['datetime_chegada_amostra']) & (merged_data['timestamp_gps'] > (row['datetime_chegada_amostra'] - pd.Timedelta(minutes=5)))        
        filtered_data = merged_data[mask]
        chegada.append(filtered_data)

    df_chegada = pd.concat(chegada)
        
    df_chegada = df_chegada.groupby('id_veiculo').agg({
        'check_start_pt': 'sum',
        'check_end_pt': 'sum',
        'timestamp_gps': 'mean'
    }).reset_index()

    df_chegada = df_chegada.rename(columns={
    'check_start_pt': 'check_start_pt_chegada',
    'check_end_pt': 'check_end_pt_chegada',
    'timestamp_gps': 'timestamp_gps_chegada'
    })
            
        
    df_chegada['data'] = df_chegada['timestamp_gps_chegada'].dt.date.astype(str)
    df_partida['data'] = df_partida['timestamp_gps_partida'].dt.date.astype(str)
    viagens_com_gps['data'] = viagens_com_gps['data'].astype(str) 

    merged_partida = pd.merge(viagens_com_gps, df_partida,
                            left_on=['data','id_veiculo_amostra'], 
                            right_on=['data','id_veiculo'],                             
                            how='left')


    merged_chegada = pd.merge(merged_partida, df_chegada, 
                            left_on=['data','id_veiculo_amostra'], 
                            right_on=['data','id_veiculo'],                             
                            how='left')

    # Remover as posições de GPS que não são das viagens
    mask_partida = (merged_chegada['timestamp_gps_partida'] >= merged_chegada['datetime_partida_amostra']) & \
                (merged_chegada['timestamp_gps_partida'] <= merged_chegada['datetime_chegada_amostra'])

    mask_chegada = (merged_chegada['timestamp_gps_chegada'] >= merged_chegada['datetime_partida_amostra']) & \
                    (merged_chegada['timestamp_gps_chegada'] <= merged_chegada['datetime_chegada_amostra'])

    # Aplique as máscaras para definir valores vazios (NA) onde as condições não são atendidas
    columns_partida = ['id_veiculo_x', 'check_start_pt_partida', 'check_end_pt_partida', 'timestamp_gps_partida']
    columns_chegada = ['id_veiculo_y', 'check_start_pt_chegada', 'check_end_pt_chegada', 'timestamp_gps_chegada']

    merged_chegada.loc[~mask_partida, columns_partida] = np.nan
    merged_chegada.loc[~mask_chegada, columns_chegada] = np.nan

    # checar se a viagem teve sinais dentro de 500m do ponto inicial e final
    condition = (
    ((merged_chegada['check_start_pt_partida'] == 0) | merged_chegada['check_start_pt_partida'].isna()) |
    ((merged_chegada['check_start_pt_chegada'] == 0) | merged_chegada['check_start_pt_chegada'].isna()) |
    ((merged_chegada['check_end_pt_partida'] == 0) | merged_chegada['check_end_pt_partida'].isna()) |
    ((merged_chegada['check_end_pt_chegada'] == 0) | merged_chegada['check_end_pt_chegada'].isna())
    )

    # Atualizar a coluna 'status' com base na condição
    merged_chegada.loc[condition, 'status'] = "O veículo não passou no raio de 500m do ponto de partida/final do trajeto"

    start_idx = merged_chegada.columns.get_loc('id_veiculo_x')
    # Exclua todas as colunas a partir desse índice
    merged_chegada.drop(merged_chegada.columns[start_idx:], axis=1, inplace=True)

    viagens_gps_classificadas = pd.concat([viagens_ja_classificadas, merged_chegada], ignore_index=True)
    print(viagens_gps_classificadas.shape[0]) 
    print(viagens_gps_classificadas)
    
    viagens_gps_classificadas = viagens_gps_classificadas.drop_duplicates()
    return viagens_gps_classificadas


### --- 7. Função que classifica os status de forma mais simples --- ###


def simplified_status(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe.rename(columns={'status': 'observacao'}, inplace=True)
    
    # Criar a nova coluna "observacoes"
    status_mapping = {
        'Viagem identificada e já paga': ['Viagem identificada e já paga', 'Viagem identificada e já paga para serviço diferente da amostra'],
        'Viagem indeferida': ['Viagem indeferida - Não atingiu % de GPS ou trajeto correto após o reprocessamento',
                              'Viagem indeferida - Não atingiu % de GPS ou trajeto correto para serviço diferente da amostra',
                              'Viagem indeferida - Não atingiu % de GPS ou trajeto correto',
                              'O veículo não passou no raio de 500m do ponto de partida/final do trajeto',
                              'Sinal de GPS encontrado para o veículo operando em serviço diferente da amostra',
                              'Sinal de GPS não encontrado para o veículo no horário da viagem'],
        'Viagem não classificada pelo algoritmo': ['Sinal de GPS encontrado para o veículo operando no mesmo serviço da amostra']
    }

    # Criar a coluna status nova (com categorias simplificadas)
    dataframe['status'] = dataframe['observacao'].map({value: key for key, values in status_mapping.items() for value in values})
    
    # Reordenar as colunas da tabela
    cols = list(dataframe.columns)
    cols.remove('status')
    cols.remove('observacao')
    cols.insert(cols.index('datetime_chegada_amostra') + 1, 'status')
    cols.insert(cols.index('status') + 1, 'observacao')
    dataframe = dataframe[cols]
    
    return dataframe