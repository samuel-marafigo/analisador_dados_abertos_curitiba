from limpar_csv import limpar_csv_em_pasta
from download_de_dados import DadosAbertosDownloader
from separar_meses_em_diferentes_arquivos import separar_meses_em_diferentes_arquivos
from juntar_csvs_mes import juntar_csvs_mes
from criar_base_de_dados import criar_base_de_dados_sql

downloader = DadosAbertosDownloader()
ano = input("Digite o ano para baixar os arquivos CSV: ").strip()
#ano = "2024"
downloader.download_csvs(ano)
limpar_csv_em_pasta(ano, limpeza_maxima=True)
separar_meses_em_diferentes_arquivos(ano)
juntar_csvs_mes(ano)
criar_base_de_dados_sql(ano)