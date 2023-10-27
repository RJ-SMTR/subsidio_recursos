
import argparse
import numpy as np
import pandas as pd

from categorize_trips import *
from query import *


def circular_trips(dados: pd.DataFrame, 
                   viagem_completa:pd.DataFrame, 
                   viagem_conformidade:pd.DataFrame) -> pd.DataFrame:
    """
    Esta função executa todo o processo de identificação de meias viagens circulares e faz a sua classificação,
    """
    # este dataframe inalterado será retornado caso não sejam encontradas viagens circulares
    dados_original = dados.copy()    
    
    ### --- 6.1 Identificar se a linha é circular --- ###  

    print('Verificando se existem linhas circulares.')

    # verifica os serviços e as datas presentes na amostra    
    tipo_servico = query_planned_trips(dados, include_shape_direction = True)

    tipo_servico['circular_dividida'] = np.where(
        (tipo_servico['sentido'] == 'C') & (tipo_servico['sentido_shape'] != 'C'), 
        1,  # a linha circular tem o shape dividido em ida e volta
        0   # a linha circular não tem o shape dividido em ida e volta
    )

    tipo_servico = tipo_servico.drop(columns=['sentido','sentido_shape'])
    tipo_servico['data'] = tipo_servico['data'].astype(str)
    tipo_servico['servico'] = tipo_servico['servico'].astype(str)
    tipo_servico = tipo_servico.drop_duplicates()
    dados['servico_amostra'] = dados['servico_amostra'].astype(str)
    dados['data'] = dados['data'].astype(str)

    dados = dados.merge(
        tipo_servico, 
        how = 'left',
        left_on=['data', 'servico_amostra'], 
        right_on=['data', 'servico']
    )

    dados.drop_duplicates()
        
    # Caso não encontre o serviço em viagem planejada
    dados['status'] = np.where(
        dados['circular_dividida'].isna(),
        "Serviço não planejado para o dia",
        dados['status']
    )

    dados = dados.drop(columns=['servico'])
    
    ### --- 5.2 Identificar viagens circulares que ainda não foram classificadas --- ###  

    # Criar um df com as viagens que serão procuradas

    df_circular_na = dados[
        (dados['circular_dividida'] == 1) &
        pd.isna(dados['status'])
    ]
    
    print(df_circular_na)

    # Criando o DataFrame df_demais_casos
    df_demais_casos = dados.drop(df_circular_na.index)


    if not df_circular_na.empty:
        # Código a ser executado caso df_circular não esteja vazio
        print('Foram identificadas viagens circulares divididas em shapes de ida e volta e podem ser visualizadas em "/data/treated/viagem_conformidade_classificada_circular.xlsx"')
        
        # Esta função classifica as meia viagens circulares que não foram identificadas nos passos anteriores
        df_circular_na = check_circular_trip(df_circular_na, viagem_completa, viagem_conformidade)
                                    
        dados = pd.concat([df_circular_na, df_demais_casos], ignore_index=True)  
        
        dados.to_excel('../data/treated/viagem_conformidade_classificada_circular.xlsx', index = False)
  
        return dados    

    else:
        print('Não existem viagens circulares divididas em shapes de ida e volta.')
        
        return dados_original
