import os
import sqlite3
import pandas as pd
from tqdm import tqdm


def criar_base_de_dados_sql(ano):

    pasta_arquivos = f'Dados abertos baixados/{ano}/Arquivos'
    caminho_banco_dados = f'Dados abertos baixados/{ano}/Arquivos/base_de_dados.db'

    conn = sqlite3.connect(caminho_banco_dados)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS atendimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_atendimento TEXT,
        data_nascimento TEXT,
        sexo TEXT,
        tipo_unidade TEXT,
        descricao_unidade TEXT,
        codigo_cid TEXT,
        descricao_cid TEXT
    )
    ''')

    arquivos_csv = [f for f in os.listdir(pasta_arquivos) if f.endswith('.csv')]

    for arquivo in tqdm(arquivos_csv, desc="Criando base de dados a partir dos arquivos"):
        caminho_arquivo = os.path.join(pasta_arquivos, arquivo)
        try:
            df = pd.read_csv(caminho_arquivo, delimiter=';', encoding='latin1')
        except UnicodeDecodeError:
            print(f"Erro ao ler o arquivo {arquivo}. Codificação desconhecida.")
            continue

        df.columns = ['data_atendimento', 'data_nascimento', 'sexo', 'tipo_unidade',
                      'descricao_unidade', 'codigo_cid', 'descricao_cid']

        df.to_sql('atendimentos', conn, if_exists='append', index=False)

        os.remove(caminho_arquivo)

    # Fechar conexão com o banco de dados
    conn.commit()
    conn.close()

    print("Base de dados criada com sucesso.")

