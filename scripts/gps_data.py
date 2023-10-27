import pandas as pd
import sys

from query import *
from categorize_trips import *
from treat_data import *


def gps_data(todas_as_viagens: pd.DataFrame) -> pd.DataFrame:
    
    """
    Esta função realiza o acesso, o tratamento e a classificação dos dados de GPS.   
    """
    linhas_nan = todas_as_viagens[pd.isna(todas_as_viagens['status'])]
    # Confirmar se a query dos dados de GPS deve ser feita

    dados_gps = query_gps(linhas_nan)

    print('Acesso aos sinais de GPS concluído com sucesso.')
    
    ### --- 7.2 Tratar os sinais de GPS --- ###
    dados_gps = treat_gps(dados_gps)
    print('Tratamento de dados de GPS concluído com sucesso.')


    ### --- 7.3 Comparar amostra com os sinais de GPS --- ###
    viagens_gps_classificadas_nan = todas_as_viagens[todas_as_viagens['status'].isna()]
    viagens_gps_classificadas_not_nan = todas_as_viagens[todas_as_viagens['status'].notna()]    

    # Aplicar a função quando o status da viagem for nan
    results = viagens_gps_classificadas_nan.apply(lambda row: check_gps(row, dados_gps), axis=1)
    viagens_gps_classificadas_nan['status'] = results.apply(lambda x: x[0])
    viagens_gps_classificadas_nan['servico_apurado'] = results.apply(lambda x: x[1])

    # Juntar tabela com status nan e status não nan
    viagens_gps_classificadas = pd.concat([viagens_gps_classificadas_nan, viagens_gps_classificadas_not_nan], ignore_index=True)

    # Quando houver sinal de GPS para um serviço além do serviço da amostra, deixar apenas o
    # serviço diferente da amostra em serviço apurado (para realizar o reprocessamento de forma correta)
    
    def remover_valor(row): 
        if pd.isna(row['servico_apurado']) or pd.isna(row['servico_amostra']):
            return ""
        elif str(row['servico_amostra']) != str(row['servico_apurado']):
            valor_a_remover = str(row['servico_amostra']) 

            # Divide o servico_apurado em partes, separadas por ','
            partes = row['servico_apurado'].split(',')

            # Remove o valor a ser removido de cada parte, verificando condições
            partes_modificadas = [p.strip().replace(valor_a_remover, '') 
                                if (
                                    p.strip()[0].isdigit() or 
                                    p.strip() == valor_a_remover
                                ) else p.strip() 
                                for p in partes]

            # Junta as partes modificadas de volta em uma string e retorna
            # Garantindo que não há espaços e vírgulas extras
            resultado = ', '.join([p for p in partes_modificadas if p]).strip()
            
            # Removendo possíveis vírgulas extras no final
            return resultado.rstrip(', ')
        else:
            return row['servico_apurado']


    viagens_gps_classificadas['servico_apurado'] = viagens_gps_classificadas.apply(remover_valor, axis=1)
    
    return viagens_gps_classificadas 