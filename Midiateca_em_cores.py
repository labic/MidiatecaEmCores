import requests
import json
import os
from urllib.parse import urlparse
from colorthief import ColorThief
from tqdm import tqdm
from PIL import Image
import csv

# Range de números para substituir na URL
start_page = 1
end_page = 100

# Lista de URLs contendo JSON
url_list = [
    f"https://midiateca.es.gov.br/site/wp-json/tainacan/v2/collection/5/items/?order=ASC&orderby=date&perpage=96&exposer=json-flat&paged={page}"
    for page in range(start_page, end_page + 1)
]


# Diretório de destino para salvar as imagens
destination_directory = "imagens/"

# Cria o diretório de destino se não existir
os.makedirs(destination_directory, exist_ok=True)

# Caminho do arquivo CSV
csv_path = "imagens_link.csv"
arquivo_saida_colors = "cores_dominantes.csv"

# Extensões de arquivo de imagem suportadas
image_extensions = [".jpg", ".jpeg", ".png", ".tif"]

def midiateca_api():
    # Verifica se o arquivo CSV já existe
    csv_exists = os.path.exists(csv_path)

    # Abre o arquivo CSV no modo apropriado
    with open(csv_path, "a" if csv_exists else "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Escreve o cabeçalho apenas se o arquivo CSV foi criado agora
        if not csv_exists or os.stat(csv_path).st_size == 0:
            writer.writerow(["Image_Name", "Document_URL", "Item_Page"])

        # Itera sobre a lista de URLs com barra de progresso
        for url in tqdm(url_list, desc="Progresso"):
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
                                # Define o caminho de destino para salvar a imagem
                                image_path = os.path.join(destination_directory, f"{image_id}.png")

                                # Verifica se o arquivo já existe no diretório de destino
                                if os.path.exists(image_path):
                                    #print(f"Imagem {image_id} já baixada. Ignorando.")
                                    continue

                                # Faz o download da imagem
                                response = requests.get(document_url)
                                image_data = response.content

                                # Salva a imagem no caminho de destino
                                with open(image_path, "wb") as image_file:
                                    image_file.write(image_data)

                                #print(f"Imagem {image_id} salva com sucesso.")

                                # Escreve a linha no arquivo CSV
                                writer.writerow([f"{image_id}", document_url, itempage])

                            #else:
                                #print(f"O URL do documento não é uma imagem para o ID {image_id}")
                        #else:
                            #print(f"URL inválida para o ID {image_id}")

    print('Download concluído')

def colors():
    diretorio = destination_directory

    # Lista de todas as imagens no diretório
    imagens = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

    # Abrir o arquivo de saída para escrita
    with open(arquivo_saida_colors, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Image_Name", "HEX", "R", "G", "B"])

        # Percorrer todas as imagens com barra de progresso
        for imagem_nome in tqdm(imagens):
            imagem_path = os.path.join(diretorio, imagem_nome)
            try:
                # Usar a biblioteca ColorThief para obter a cor dominante
                color_thief = ColorThief(imagem_path)
                cor_dominante = color_thief.get_color(quality=1)
                cor_hex = '#%02x%02x%02x' % cor_dominante
                
                # Obter o nome da imagem sem a extensão
                nome_sem_extensao = os.path.splitext(imagem_nome)[0]
                
                # Escrever as informações no arquivo .csv
                writer.writerow([nome_sem_extensao, cor_hex, cor_dominante[0], cor_dominante[1], cor_dominante[2]])
                
                #print(f"Analisada a imagem: {imagem_nome}")
            except Exception as e:
                print(f"Erro ao analisar a imagem {imagem_nome}: {str(e)}")
    print('Analise de cor concluída')

def hex_to_hsl(hex_value):
    hex_value = hex_value.lstrip('#')
    rgb = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = [x / 255.0 for x in rgb]
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn
    h = 0.0
    s = 0.0
    l = (mx + mn) / 2.0
    if diff != 0.0:
        if mx == r:
            h = (g - b) / diff % 6
        elif mx == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        s = diff / (1 - abs(2 * l - 1))
    h *= 60
    return h, s, l

def generate_html_visualization(cores_dominantes_file, imagens_file):
    # Carregar cores dominantes
    cores_dominantes = {}
    with open(cores_dominantes_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            image_name = row['Image_Name']
            hex_value = row['HEX']
            cores_dominantes[image_name] = hex_value
    
    # Perguntar a ordem das cores ao usuário
    ordem_cores = ["1", "2", "3", "4"]
    #("Escolha a ordem das cores:\n1 - Cores quentes para frias\n2 - Cores por matiz\n3 - Cores por brilho\n4 - Cores por saturação\n")

    imagens = {}
    with open(imagens_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            image_name = row['Image_Name']
            image_url = row['Document_URL']
            item_page_url = row['Item_Page']
            imagens[image_name] = (image_url, item_page_url)    

    # Gerar código HTML para cada opção de cor
    for i, ordem in enumerate(ordem_cores):
        cores_dominantes_ordenadas = []
        if ordem == "1":
            cores_dominantes_ordenadas = sorted(cores_dominantes.items(), key=lambda x: hex_to_hsl(x[1])[0], reverse=True)
        elif ordem == "2":
            cores_dominantes_ordenadas = sorted(cores_dominantes.items(), key=lambda x: hex_to_hsl(x[1])[0])
        elif ordem == "3":
            cores_dominantes_ordenadas = sorted(cores_dominantes.items(), key=lambda x: hex_to_hsl(x[1])[2])
        elif ordem == "4":
            cores_dominantes_ordenadas = sorted(cores_dominantes.items(), key=lambda x: hex_to_hsl(x[1])[1])
        else:
            print("Opção inválida. A ordem das cores será definida por padrão.")
            cores_dominantes_ordenadas = sorted(cores_dominantes.items(), key=lambda x: hex_to_hsl(x[1])[0])
    
    
        # Gerar código HTML (incluindo as alterações anteriores)
        html = '<html><head><meta charset="UTF-8"><title>Midiateca em Cores</title><link rel="icon" href="https://i.postimg.cc/BnN3LVwq/Midiateca-Cores.png">'
        html += '<link href="https://fonts.googleapis.com/css2?family=Oxanium:wght@700&display=swap" rel="stylesheet">'
        html += '<link href="https://fonts.googleapis.com/css2?family=Oxanium:wght@500&display=swap" rel="stylesheet">'
        html += '<style>'
        html += '.menu { background-color: #C4544E; padding: 10px; text-align: center; font-family: Oxanium, sans-serif; font-weight: 600; font-size: 15px; }'
        html += '.menu ul { list-style-type: none; margin: 0; padding: 0; }'
        html += '.menu li { display: inline-block; margin-right: 30px; }'
        html += '.menu a { color: #FFF; text-decoration: none; padding: 5px; }'
        html += '.menu a:hover { background-color: #424242; border-radius: 5px; }'
        html += '.footer { background-color: #C4544E; color: #FFF; font-family: Arial, sans-serif; font-weight: bold; padding: 10px; text-align: center; position: botton; left: 0; bottom: 0; width: 100%; margin-top: 50px; }'
        html += '.footer a { text-decoration: none; color: #FFF }'
        html += '.color-dot { width: 15px; height: 15px; border-radius: 50%; display: inline-block; margin: 3px; }'
        html += '.image-preview { width: 100px; height: 100px; border-radius: 30%; background-color: #000; position: absolute; display: none; }'
        html += '</style></head>'
        html += '<h1 style="font-family: Oxanium, sans-serif; font-weight: 700; font-size: 55px; color: #C4544E; padding: 0px; text-align: center; margin-top: 20px;">'
        html += '<img src="https://i.postimg.cc/BnN3LVwq/Midiateca-Cores.png" alt="Logo" style="vertical-align: middle; height: 110px; margin-right: 10px; margin-top: 0px;">'
        html += 'Midiateca em Cores</h1>'
        html += '<div class="menu"><ul>'
        html += '<li><a href="#" onclick="window.location.href=\'visualization1.html\'" >Temperatura</a></li>'
        html += '<li><a href="#" onclick="window.location.href=\'visualization4.html\'" >Saturação</a></li>'
        html += '<li><a href="#" onclick="window.location.href=\'visualization2.html\'" >Matiz</a></li>'
        html += '<li><a href="#" onclick="window.location.href=\'visualization3.html\'" >Brilho</a></li>'
        html += '</ul></div>'
        html += '<div style="margin: 40px 70px 0; border: 8px solid #C4544E; padding: 8px;">'

        for image_name, hex_value in cores_dominantes_ordenadas:
            if image_name in imagens:
                image_url, item_page_url = imagens[image_name]
                html += f'<a href="{item_page_url}" target="_blank"><div class="color-dot" style="background-color: {hex_value}" onmousemove="moveImagePreview(event, \'{image_url}\')"></div></a>'
        
        html += '</div>'
        html += '<div id="image-preview" style="position: absolute; display: none; width: 100px; height: 100px; border-radius: 30%; background-color: #000;"></div>'
        html += '<script>'
        html += 'function moveImagePreview(event, imageUrl) {'
        html += '    var previewDiv = document.getElementById("image-preview");'
        html += '    previewDiv.style.display = "block";'
        html += '    previewDiv.style.left = (event.pageX + 10) + "px";'
        html += '    previewDiv.style.top = (event.pageY + 10) + "px";'
        html += '    previewDiv.style.backgroundImage = "url(\'" + imageUrl + "\')";'
        html += '    previewDiv.style.backgroundSize = "cover";'
        html += '    previewDiv.style.backgroundPosition = "center";'
        html += '}'
        html += '</script>'
        html += '<div style="height: 50px; background-color: #C4544E; text-align: center; color: white; font-family: Oxanium, sans-serif; font-weight: 600; font-size: 30px; margin-top: 30px; padding-top: 15px;">Metodologia de Desenvolvimento</div>'
        html += '<div>'
        html += '<div style="display: flex; justify-content: center; align-items: center;">'
        html += '<img src="https://i.postimg.cc/MGqp5wnp/Cores-Da-Midiateca-Organocgrama.png" alt="Logo" style="width: 100%; max-height: 600px; margin: 40px;">'
        html += '</div>'
        html += '<div class="footer"><a href="https://midiateca.es.gov.br/" target="_blank">'
        html += '<img src="https://midiateca.es.gov.br/site/wp-content/uploads/2022/04/Logo_da_Midiateca_Capixaba-2-1024x344.png" alt="Logo" style="vertical-align: middle; height: 40px; margin-right: 40px;">'
        html += '<img src="https://i.postimg.cc/vZ0C9mzL/Logo-Labic-2.png" alt="Logo" style="vertical-align: middle; height: 30px; margin-right: 40px;">'
        html += '<img src="https://servicos.fapes.es.gov.br/fapes_imposto/assets/images/logo%20branca.png" alt="Logo" style="vertical-align: middle; height: 30px; margin-right: 40px;">'
        html += '<img src="https://i.postimg.cc/x1vPmp3v/secult-horizontal.png" alt="Logo" style="vertical-align: middle; height: 60px; margin-right: 40px;">'
        html += '</div>'
        html += '</body></html>'

    
        # Antes de gerar o código HTML
        html = html.replace("Satura��o", "Saturação")

        # Salvar arquivo HTML para cada opção de cor
        with open(f'visualization{i+1}.html', 'w', encoding='utf-8') as file:
            file.write(html)
    
        print("A visualização HTML foi gerada com sucesso.")

print('Atualizar banco de imagens via API Tainacan?')
print('1 - Sim')
print('2 - Não')
optionapi = input('Digite a opção:')
if optionapi == '1':
    midiateca_api()
    colors()
    generate_html_visualization(arquivo_saida_colors, csv_path)
elif optionapi == '2':
    print('Fazer analise de cor?')
    print('1 - Sim')
    print('2 - Não')
    optioncolor = input('Digite a opção:')
    if optioncolor == '1':
        colors()
        generate_html_visualization(arquivo_saida_colors, csv_path)
    elif optioncolor == '2':
        generate_html_visualization(arquivo_saida_colors, csv_path)
    else:
        print('Opção invalida')
else:
    print('Opção invalida')
