import os
import requests
from bs4 import BeautifulSoup


class DadosAbertosDownloader:
    def __init__(self):
        self.base_url = 'https://dadosabertos.c3sl.ufpr.br/curitiba/SESPAMedicoUnidadesMunicipaisDeSaude/'

    @staticmethod
    def criar_pasta_se_nao_existir(caminho):
        if not os.path.exists(caminho):
            os.makedirs(caminho)

    def obter_links_csvs(self, ano):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        csv_links = [link['href'] for link in links if
                     link['href'].endswith('.csv') and link['href'].startswith(str(ano))]
        return csv_links, soup

    @staticmethod
    def obter_tamanho_arquivos(soup, csv_links):
        total_size = 0
        for link in csv_links:
            link_tag = soup.find('a', href=link)
            size_cell = link_tag.find_parent('tr').find_all('td')[-2]
            size_text = size_cell.text.strip()
            if 'M' in size_text:
                size = float(size_text.replace('M', ''))
            elif 'K' in size_text:
                size = float(size_text.replace('K', '')) / 1024
            total_size += size
        return total_size / 1024  # Convert to GB

    def baixar_arquivos(self, csv_links, pasta_destino):
        for link in csv_links:
            nome_arquivo = link.split('/')[-1]
            ano = nome_arquivo.split('-')[0]
            pasta_ano = os.path.join(pasta_destino, ano)
            self.criar_pasta_se_nao_existir(pasta_ano)

            print(f'Fazendo download de {nome_arquivo}...')
            response = requests.get(self.base_url + link)
            with open(os.path.join(pasta_ano, nome_arquivo), 'wb') as f:
                f.write(response.content)
            print(f'{nome_arquivo} baixado com sucesso.')

    def download_csvs(self, ano):
        csv_links, soup = self.obter_links_csvs(ano)

        # Check existing files
        pasta_destino = 'Dados abertos baixados'
        self.criar_pasta_se_nao_existir(pasta_destino)
        csv_links = [link for link in csv_links if
                     not os.path.exists(os.path.join(pasta_destino, ano, link.split('/')[-1]))]

        if not csv_links:
            print('Não há dados novos para baixar.')
            return

        total_size_gb = self.obter_tamanho_arquivos(soup, csv_links)

        print(f'Encontrados {len(csv_links)} arquivos novos para o ano {ano} em {self.base_url}')
        print(
            f'ATENÇÃO: O tamanho total dos arquivos baixados será de {total_size_gb:.2f} GB. Recomenda-se que você tenha pelo menos {total_size_gb * 2:.2f} GB livres. Deseja continuar? Digite S ou N')

        resposta = input().strip().upper()
        if resposta != 'S':
            print('Download cancelado pelo usuário.')
            return

        print('Iniciando download...')
        self.baixar_arquivos(csv_links, pasta_destino)
        print('Todos os arquivos baixados com sucesso.')


