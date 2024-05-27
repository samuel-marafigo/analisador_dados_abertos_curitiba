import os
import pandas as pd

def juntar_csvs_mes(ano):

    caminho_pasta = f'Dados abertos baixados/{ano}/Arquivos'
    arquivos = [f for f in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, f))]

    dfs_por_mes = {}

    for arquivo in arquivos:
        mes = arquivo.split()[0]

        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')

        if mes in dfs_por_mes:
            dfs_por_mes[mes].append((df, caminho_arquivo))
        else:
            dfs_por_mes[mes] = [(df, caminho_arquivo)]

    for mes, df_tuplas in dfs_por_mes.items():
        dfs = [df for df, _ in df_tuplas]
        df_combined = pd.concat(dfs, ignore_index=True).drop_duplicates()

        nome_novo_arquivo = f"{mes} combinado.csv"
        caminho_novo_arquivo = os.path.join(caminho_pasta, nome_novo_arquivo)

        df_combined.to_csv(caminho_novo_arquivo, sep=';', index=False, encoding='latin1')
       # print(f"Arquivo combinado criado: {caminho_novo_arquivo}")

        # Deletar os arquivos antigos
        for _, caminho_arquivo_original in df_tuplas:
            os.remove(caminho_arquivo_original)
            #print(f"Arquivo original deletado: {caminho_arquivo_original}")

