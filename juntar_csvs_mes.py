"""
Função para juntar dois arquivos CSV do mesmo mês.
Recebe o caminho da pasta onde os arquivos CSV estão localizados e junta arquivos do mesmo mês.
Cria um novo arquivo CSV combinado para cada mês encontrado.
"""

import os
import pandas as pd

def juntar_csvs_mes(caminho_pasta):
    # Obter lista de arquivos na pasta
    arquivos = [f for f in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, f))]

    # Criar um dicionário para armazenar dataframes por mês
    dfs_por_mes = {}

    # Iterar sobre os arquivos para carregar dataframes por mês
    for arquivo in arquivos:
        # Extrair o mês do nome do arquivo (assumindo que o mês é a primeira palavra)
        mes = arquivo.split()[0]

        # Ler o arquivo CSV
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')

        # Adicionar o dataframe ao dicionário
        if mes in dfs_por_mes:
            dfs_por_mes[mes].append(df)
        else:
            dfs_por_mes[mes] = [df]

    # Juntar dataframes do mesmo mês e salvar arquivos combinados
    for mes, dfs in dfs_por_mes.items():
        # Concatenar dataframes e remover duplicatas mantendo os dados
        df_combined = pd.concat(dfs, ignore_index=True).drop_duplicates()

        # Nome do novo arquivo combinado
        nome_novo_arquivo = f"{mes} combinado.csv"
        caminho_novo_arquivo = os.path.join(caminho_pasta, nome_novo_arquivo)

        # Salvar o dataframe combinado em um novo arquivo CSV
        df_combined.to_csv(caminho_novo_arquivo, sep=';', index=False, encoding='latin1')
        print(f"Arquivo combinado criado: {caminho_novo_arquivo}")
