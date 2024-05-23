"""
Função para limpar um arquivo CSV específico.
Recebe o caminho ou nome do arquivo CSV a ser limpo e uma opção de limpeza máxima.
Cria um novo arquivo CSV limpo na mesma pasta com o nome "LIMPO (nome original).csv".
"""

import pandas as pd


def limpar_csv(caminho_csv, limpeza_maxima=False):
    colunas_para_remover = [
        "Código do Tipo de Unidade", "Código da Unidade", "Código do Procedimento",
        "Código do CBO", "Solicitação de Exames", "Qtde Prescrita Farmácia Curitibana",
        "Qtde Dispensada Farmácia Curitibana", "Qtde de Medicamento Não Padronizado",
        "Área de Atuação", "Tratamento no Domicílio", "Abastecimento", "Energia Elétrica",
        "Tipo de Habitação", "Destino Lixo", "Fezes/Urina", "Cômodos", "Em Caso de Doença",
        "Grupo Comunitário", "Meio de Comunicacao", "Meio de Transporte", "cod_usuario",
        "origem_usuario", "residente", "cod_profissional"
    ]

    if limpeza_maxima:
        colunas_para_remover.extend([
            "Descrição do Procedimento", "Solicitação de Exames",
            "Encaminhamento para Atendimento Especialista", "Área de Atuação",
            "Desencadeou Internamento", "Data do Internamento", "Estabelecimento Solicitante",
            "Estabelecimento Destino", "CID do Internamento", "Nacionalidade", "Descrição do CBO",
            "Municício", "Bairro"
        ])

    df = pd.read_csv(caminho_csv, sep=';', encoding="latin1")
    df_limpo = df.drop(columns=colunas_para_remover)
    nome_novo_arquivo = "LIMPO " + caminho_csv
    df_limpo.to_csv(nome_novo_arquivo, sep=';', index=False, encoding="latin1")

    print(f"Arquivo limpo criado: {nome_novo_arquivo}")