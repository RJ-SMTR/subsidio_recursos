## --- Treatment functions --- ###

### --- 1. Importar bibliotecas --- ###
import pandas as pd



### --- 2. Tratamento da amostra --- ###

def treat_sample(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Trata os dados da amostra.
    
    Parâmetros:
    amostra (dataframe): Dataframe contendo a amostra.
    
    Retorna:
    dataframe: com as colunas nos tipos corretos para serem usados pelo algoritmo de recursos.
    
    Exemplos:
    >>> treat_sample(amostra)
    """        
    dados['servico'] = dados['servico'].astype(str)
    dados['data'] = dados['data'].astype(str)
    dados['id_veiculo'] = dados['id_veiculo'].astype(str)
    dados['hora_inicio'] = dados['hora_inicio'].astype(str)
    dados['datetime_partida'] = pd.to_datetime(dados['data'] + ' ' + dados['hora_inicio'])
    dados['hora_fim'] = dados['hora_fim'].astype(str)
    dados['datetime_chegada'] = pd.to_datetime(dados['data'] + ' ' + dados['hora_fim'])
    
    print('Tratamento da amostra concluído com sucesso.')   
    return dados


### --- 3. Tratamento das viagens completa e conformidade --- ###

def treat_trips(dados: pd.DataFrame) -> pd.DataFrame:
    
    """
    Trata os dados das viagens. Deve ser usada após as queries das tabelas 
    viagem_completa ou viagem_conformidade.
    
    Parâmetros:
    dados (dataframe): Dataframe contendo as viagens.
    
    Retorna:
    dataframe: com as colunas nos tipos corretos para serem usados pelo algoritmo de recursos.
    
    Exemplos:
    >>> treat_trips(viagem_completa)
    """    
    
    dados['servico_informado'] = dados['servico_informado'].astype(str)
    dados['data'] = dados['data'].astype(str)
    dados['id_veiculo'] = dados['id_veiculo'].astype(str)
    dados['datetime_partida'] = pd.to_datetime(dados['datetime_partida'])
    dados['datetime_chegada'] = pd.to_datetime(dados['datetime_chegada']) 
    dados = dados.sort_values(by = 'datetime_partida')
    
    return dados
    
    
    
### --- 4. Tratamento dos dados de GPS --- ###

def treat_gps(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Trata os dados de GPS das tabelas gps_sppo e aux_registros_status_trajeto.
    
    Parâmetros:
    dados (dataframe): Dataframe contendo os dados de GPS.
    
    Retorna:
    dataframe: com as colunas nos tipos corretos para serem usados pelo algoritmo de recursos.
    
    Exemplos:
    >>> treat_gps(gps)
    """         
    # trata as tabelas gps_sppo e a tabela de status (colocar o nome aqui)
    dados['servico'] = dados['servico'].astype(str)
    dados['id_veiculo'] = dados['id_veiculo'].astype(str)
    dados['timestamp_gps'] = pd.to_datetime(dados['timestamp_gps'])
    
    return dados


   
### --- 5. Tratamento dos filtros das queries --- ###

def query_values(dados: pd.DataFrame, col_name: str) -> str:
    """
    Coleta os valores únicos de determinada coluna de um dataframe e retorna separado por vírgulas, 
    para ser utilizado em filtros do SQL
    """
    # Verifica se col_name está presente no DataFrame
    if col_name not in dados.columns:
        raise ValueError(f'A coluna {col_name} não está presente no DataFrame.')

    if col_name == 'data':
        dados['data'] = pd.to_datetime(dados['data']).dt.strftime('%Y-%m-%d')
        
    unique_values = dados[col_name].drop_duplicates().tolist()
    
    # Formata os valores para uso em uma consulta SQL
    formatted_values = ','.join([f"'{value}'" for value in unique_values])

    return formatted_values

   