import pandas as pd
import os
from tqdm import tqdm

def limpar_csv_em_pasta(ano, limpeza_maxima=False):
    pasta_base = os.path.dirname(os.path.abspath(__file__))
    pasta_dados = os.path.join(pasta_base, "Dados abertos baixados", str(ano))
    pasta_arquivos = os.path.join(pasta_dados, "Arquivos")

    if not os.path.exists(pasta_dados):
        print(f"Pasta não encontrada: {pasta_dados}")
        return

    if not os.path.exists(pasta_arquivos):
        os.makedirs(pasta_arquivos)

    colunas_para_remover = [
        "Código do Tipo de Unidade", "Código da Unidade", "Código do Procedimento",
        "Código do CBO", "Solicitação de Exames", "Qtde Prescrita Farmácia Curitibana",
        "Qtde Dispensada Farmácia Curitibana", "Qtde de Medicamento Não Padronizado",
        "Área de Atuação", "Tratamento no Domicílio", "Abastecimento", "Energia Elétrica",
        "Tipo de Habitação", "Destino Lixo", "Fezes/Urina", "Cômodos", "Em Caso de Doença",
        "Grupo Comunitário", "Meio de Comunicação", "Meio de Transporte", "cod_usuario",
        "origem_usuario", "residente", "cod_profissional", "Meio de Comunicacao"
    ]

    if limpeza_maxima:
        colunas_para_remover.extend([
            "Descrição do Procedimento", "Solicitação de Exames",
            "Encaminhamento para Atendimento Especialista", "Área de Atuação",
            "Desencadeou Internamento", "Data do Internamento", "Estabelecimento Solicitante",
            "Estabelecimento Destino", "CID do Internamento", "Nacionalidade", "Descrição do CBO",
            "Municício", "Bairro"
        ])

    arquivos_csv = [f for f in os.listdir(pasta_dados) if f.endswith(".csv")]
    for nome_arquivo in tqdm(arquivos_csv, desc="Limpando colunas desnecessárias", unit="arquivo"):
        caminho_csv = os.path.join(pasta_dados, nome_arquivo)
        df = pd.read_csv(caminho_csv, sep=';', encoding="latin1", low_memory=False)
        df_limpo = df.drop(columns=colunas_para_remover, errors='ignore')
        nome_novo_arquivo = f"LIMPO {nome_arquivo}"
        caminho_novo_csv = os.path.join(pasta_arquivos, nome_novo_arquivo)
        df_limpo.to_csv(caminho_novo_csv, sep=';', index=False, encoding="latin1")
        #print(f"Arquivo limpo criado: {caminho_novo_csv}")

    print("Processo concluído.")
