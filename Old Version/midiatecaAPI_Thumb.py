import requests
import json
import os
from urllib.parse import urlparse
from PIL import Image
import csv

# Range de números para substituir na URL
start_page = 1
end_page = 48

# Lista de URLs contendo JSON
url_list = [
    f"https://midiateca.es.gov.br/site/wp-json/tainacan/v2/collection/5/items/?order=ASC&orderby=date&perpage=96&exposer=json-flat&paged={page}"
    for page in range(start_page, end_page + 1)
]


# Diretório de destino para salvar as imagens
destination_directory = "imagensthumb2/"

# Cria o diretório de destino se não existir
os.makedirs(destination_directory, exist_ok=True)

# Caminho do arquivo CSV
csv_path = "imagensthumb.csv"

# Extensões de arquivo de imagem suportadas
image_extensions = [".jpg", ".jpeg", ".png", ".tif"]

# Cria o arquivo CSV e escreve o cabeçalho
with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Image_Name", "Document_URL", "Item_Page"])

    # Itera sobre a lista de URLs
    for url in url_list:
        # Obtém o JSON da URL
        response = requests.get(url)
        data = response.json()

        # Obtém a lista de itens do JSON
        items = data.get("items", [])

        # Itera sobre cada item na lista de itens
        for item in items:
            # Obtém os campos relevantes do item
            document_urls = item.get("thumbnail")
            image_id = str(item.get("id"))
            itempage = str(item.get("url"))

            # Verifica se o campo "thumbnail" existe e se é uma lista de URLs válidas
            if document_urls and isinstance(document_urls, list):
                for document_url in document_urls:
                    # Verifica se a URL é válida
                    if isinstance(document_url, str) and urlparse(document_url).scheme:
                        # Verifica se a extensão do arquivo é uma extensão de imagem
                        _, file_extension = os.path.splitext(document_url)
                        if file_extension.lower() in image_extensions:
                            # Faz o download da imagem
                            response = requests.get(document_url)
                            image_data = response.content

                            # Define o caminho de destino para salvar a imagem
                            image_path = os.path.join(destination_directory, f"{image_id}.png")

                            # Salva a imagem no caminho de destino
                            with open(image_path, "wb") as image_file:
                                image_file.write(image_data)

                            print(f"Imagem {image_id} salva com sucesso.")

                            # Escreve a linha no arquivo CSV
                            writer.writerow([f"{image_id}", document_url, itempage])

                        else:
                            print(f"O URL do documento não é uma imagem para o ID {image_id}")
                    else:
                        print(f"URL inválida para o ID {image_id}")

print('Download concluído')
