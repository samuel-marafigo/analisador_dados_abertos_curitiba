import pandas as pd
import os
import glob
from tqdm import tqdm

def separar_meses_em_diferentes_arquivos(ano):
    """
    Função para separar arquivos CSV em diferentes arquivos com base no mês da coluna "Data do Atendimento".
    Processa todos os arquivos CSV na pasta 'Arquivos' cujo nome contém 'LIMPO {ano}'.
    Após o processamento, remove os arquivos originais 'LIMPO {ano}'.
    """
    pasta = f'Dados abertos baixados/{ano}/Arquivos'
    padrao_arquivo = os.path.join(pasta, f'LIMPO {ano}*.csv')
    arquivos = glob.glob(padrao_arquivo)

    for caminho_csv in tqdm(arquivos, desc="Processando datas de atendimento", unit="arquivo"):
        df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')
        df['Data do Atendimento'] = pd.to_datetime(df['Data do Atendimento'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

        if df['Data do Atendimento'].isnull().any():
            raise ValueError(f"Erro ao converter a coluna 'Data do Atendimento' para datetime no arquivo {caminho_csv}.")

        # Ensure the column is of datetime type before filtering
        if not pd.api.types.is_datetime64_any_dtype(df['Data do Atendimento']):
            raise TypeError("A coluna 'Data do Atendimento' não é do tipo datetime após a conversão.")

        # Filter rows to only include the specified year
        df_filtered = df[df['Data do Atendimento'].dt.year == int(ano)].copy()

        if df_filtered.empty:
            print(f"Nenhum dado encontrado para o ano {ano} no arquivo {caminho_csv}.")
            continue

        df_filtered.loc[:, 'Mês'] = df_filtered['Data do Atendimento'].dt.strftime('%B')

        for mes, grupo in df_filtered.groupby('Mês'):
            nome_novo_arquivo = os.path.join(pasta, f"{mes} {os.path.basename(caminho_csv)}")
            grupo.drop(columns=['Mês']).to_csv(nome_novo_arquivo, sep=';', index=False, encoding='latin1')
            #print(f"Arquivo criado: {nome_novo_arquivo}")

    for caminho_csv in tqdm(arquivos, desc="Removendo arquivos antigos", unit="arquivo"):
        os.remove(caminho_csv)
        #print(f"Arquivo antigo removido: {caminho_csv}")

