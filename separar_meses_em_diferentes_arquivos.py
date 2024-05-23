"""
Função para separar um arquivo CSV em diferentes arquivos com base no mês da coluna "Data do Atendimento".
Recebe o caminho ou nome do arquivo CSV e cria novos arquivos CSV nomeados "{MÊS} nome original.csv".
"""

import pandas as pd


def separar_meses_em_diferentes_arquivos(caminho_csv):
    # Ler o arquivo CSV com a codificação 'latin1'
    df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')

    # Converter a coluna "Data do Atendimento" para datetime
    df['Data do Atendimento'] = pd.to_datetime(df['Data do Atendimento'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

    # Verificar se a conversão teve sucesso
    if df['Data do Atendimento'].isnull().any():
        raise ValueError("Erro ao converter a coluna 'Data do Atendimento' para datetime.")

    # Criar uma coluna "Mês" baseada na coluna "Data do Atendimento"
    df['Mês'] = df['Data do Atendimento'].dt.strftime('%B')

    # Separar o DataFrame por mês e salvar arquivos separados
    for mes, grupo in df.groupby('Mês'):
        nome_novo_arquivo = f"{mes} {caminho_csv}"
        grupo.drop(columns=['Mês']).to_csv(nome_novo_arquivo, sep=';', index=False, encoding='latin1')
        print(f"Arquivo criado: {nome_novo_arquivo}")