import requests
import json
import os
from urllib.parse import urlparse
from colorthief import ColorThief
from tqdm import tqdm
from PIL import Image
import time
import csv
import pandas as pd

# Range de números para substituir na URL
start_page = 1
end_page = 100

# Lista de URLs contendo JSON
url_list = [
    f"https://midiateca.es.gov.br/site/wp-json/tainacan/v2/collection/5/items/?order=ASC&orderby=date&perpage=96&exposer=json-flat&paged={page}"
    for page in range(start_page, end_page + 1)
]


# Diretório de destino para salvar as imagens
destination_directory = "temp_imagens"

# Cria o diretório de destino se não existir
os.makedirs(destination_directory, exist_ok=True)

# Caminho do arquivo CSV
csv_path = "dataimages.csv"
#arquivo_saida_colors = "cores_dominantes.csv"

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
            writer.writerow(["image_name", "document_url", "item_page", "museu", "cidade", "item_description"])

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
                museu = str(item.get("data", {}).get("museu", {}).get("value"))
                cidade = str(item.get("data", {}).get("cidade-2", {}).get("value"))
                description = str(item.get("data", {}).get("description", {}).get("value"))

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
                                if description:
                                    writer.writerow([f"{image_id}", document_url, itempage, museu, cidade, description])
                                else:
                                    description = ""
                                    writer.writerow([f"{image_id}", document_url, itempage, museu, cidade, description])

                            #else:
                                #print(f"O URL do documento não é uma imagem para o ID {image_id}")
                        #else:
                            #print(f"URL inválida para o ID {image_id}")

    print('Download concluído')

def colors():
    diretorio = destination_directory
    imagens = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

    color_data = []  # A list to collect dominant color information

    for imagem_nome in tqdm(imagens, desc='Processing images', unit='image'):
        imagem_path = os.path.join(diretorio, imagem_nome)
        try:
            color_thief = ColorThief(imagem_path)
            cor_dominante = color_thief.get_color(quality=1)
            cor_hex = '#%02x%02x%02x' % cor_dominante

            # Remove a extensão do nome do arquivo
            imagem_nome_sem_extensao = os.path.splitext(imagem_nome)[0]

            # Append the new data to the color_data list as a dictionary
            color_data.append({"image_name": imagem_nome_sem_extensao, "HEX": cor_hex})
        except Exception as e:
            print(f"Erro ao analisar a imagem {imagem_nome}: {str(e)}")

    # Now, open the CSV file to update its content with the collected data
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=",")
        existing_fields = reader.fieldnames

        # Create a new CSV file with the updated data
        temp_file_path = csv_path + ".temp"
        with open(temp_file_path, "w", newline='', encoding="utf-8") as new_file:
            new_fields = existing_fields + ["HEX"]
            writer = csv.DictWriter(new_file, fieldnames=new_fields, delimiter=",")
            writer.writeheader()

            # Write the updated data to the new CSV file
            for row in reader:
                imagem_nome = row["image_name"]
                cor_hex = None
                for color_row in color_data:
                    if color_row["image_name"] == imagem_nome:
                        cor_hex = color_row["HEX"]
                        break

                # Create a new row with the existing data and the new "HEX" value
                new_row = row.copy()
                new_row["HEX"] = cor_hex
                writer.writerow(new_row)

    # Replace the original CSV file with the temporary one
    os.replace(temp_file_path, csv_path)

    print("Analise de Cores Concluida")

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

def generate_html_visualization():
    # Carregar URLs das imagens e páginas
    imagenscolor = {}
    with open(csv_path, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                image_name = row.get('image_name', '')  
                item_page_url = row.get('item_page', '')  
                image_url = row.get('document_url', '')  
                hex_valor = row.get('HEX', '')  
                instituicao = row.get('museu', '') 
                city = row.get('cidade', '') 
                imagetext = row.get('item_description', '').replace('"', "'").replace('\n', ' ')  
                imagetext = imagetext if imagetext else ' '  # Se imagetext estiver em branco, atribui um espaço em branco
                imagenscolor[image_name] = (image_url, item_page_url, hex_valor, instituicao, city, imagetext)


    # Perguntar a ordem das cores ao usuário
    ordem_cores = ["1"]

    # Gerar código HTML para cada opção de cor
    for i, ordem in enumerate(ordem_cores):

        # Gerar código HTML (incluindo as alterações anteriores)
        html = '''<html>
    <head>
        <meta charset="UTF-8">
        <title>Midiateca em Cores</title>
        <link rel="icon" href="https://i.postimg.cc/BnN3LVwq/Midiateca-Cores.png">
        <link href="https://fonts.googleapis.com/css2?family=Oxanium:wght@700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Oxanium:wght@500&display=swap" rel="stylesheet">
        <style>
            .menu { 
                background-color: #C4544E; 
                padding: 10px; 
                text-align: center; 
                font-family: Oxanium, sans-serif; 
                font-weight: 600; 
                font-size: 15px; 
                margin-top: -30px;
            }
            .menu span { 
                background-color: #C4544E; 
                padding: 10px; 
                text-align: center; 
                font-family: Oxanium, sans-serif; 
                font-weight: 600; 
                font-size: 15px; 
                margin-top: -30px;
                color: white;
                border: white;
            }
            .menu ul { 
                list-style-type: none; 
                margin: 0; 
                padding: 0; 
            }
            .menu li { 
                display: inline-block; 
                margin-right: 30px; 
            }
            .menu a { color: #FFF; 
                text-decoration: none; 
                padding: 5px; 
            }
            .menu a:hover { 
                background-color: #424242; 
                border-radius: 5px; 
            }
            footer { 
                background-color: #C4544E; 
                color: #FFF; 
                font-family: Arial, sans-serif; 
                font-weight: bold; 
                padding: 10px; 
                text-align: center; 
                position: botton; 
                left: 0; 
                bottom: 0; 
                width: 100%; 
                margin-top: 50px; 
            }
            .footer a { 
                text-decoration: none; 
                color: #FFF 
            }
            .color-dot { 
                width: 17px; 
                height: 17px; 
                border-radius: 50%;
                display: inline-block; 
                margin: 3px; 
            }
            .image-preview { 
                width: 100px; 
                height: 100px; 
                border-radius: 30%; 
                background-color: #000;
                position: absolute; 
                display: none; 
            }
            h1 {
                font-family: Oxanium, sans-serif; 
                font-weight: 700; 
                font-size: 55px; 
                color: #C4544E; 
                padding: 0px; 
                text-align: center; 
                margin-top: 20px;
            }
            .dotbox {
                margin: 2vw 1.5vh;
                border: 8px solid #C4544E;
                padding: 8px; 
                display: flex; 
                flex-wrap: wrap; 
                justify-content: left;
                margin-top: 10px;                    
            }
            #searchInput {
                justify-content: center;
                font-family: Titillium Web, sans-serif; 
                font-weight: 700; 
                font-size: 13px; 
                border: 2px solid #C4544E;
                border-radius: 5px;
                cursor: pointer;
                outline: none;
                color: #C4544E;
                padding: 3px 7px;
            }

            .menuexp {
                text-align: center;
                font-family: Titillium Web, sans-serif;
                font-weight: 700;
                font-size: 15px;            
            }
            .menuexp ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
            }
            .menuexp li {
                display: inline-block;
                margin-right: 30px;
            }
            .menuexp a {
                color: #FFF;
                text-decoration: none;
                padding: 5px;
            }
            .menuexp a:hover {
                background-color: #424242;
                border-radius: 5px;
            }
            .footer {
                background-color: #C4544E;
                color: #FFF;
                font-family: Titillium Web, sans-serif;
                font-weight: 600;
                padding: 20px;
                text-align: center;
                font-size: 14px;
                width: fill;
                margin-top: 20px;
                text-align: center;
            }
            .footer a {
                text-decoration: none;
                color: #FFF
            }
            .word-cloud-container {
                display: flex;
                flex-wrap: wrap;
                margin: 5px;
                font-family: Titillium Web, sans-serif; 
                font-weight: 700; 
                border: 5px solid #C4544E;
                border-radius: 5px;
                outline: none;
                color: #C4544E;
                padding: 2px 7px;
                justify-content: space-around;
                cursor: pointer;
                vertical-align: middle;
                margin-bottom: 20px;
            }

            .word-cloud-container span {
                margin: 6px;
                display: inline-block;
                vertical-align: middle;
            }
            .Dropdown:hover {
                background-color: #C4544E;
                color: #ffffff;
            }
            .Dropdown {
                padding: 4px;
                font-family: Titillium Web, sans-serif;
                font-weight: 700;
                font-size: 11px;
                color: #C4544E;
                background-color: #ffffff;
                border: 2px solid #C4544E;
                border-radius: 5px;
                cursor: pointer;
                outline: none;
                text-transform: uppercase;
            }
            .display-mode-btn {
                display: flex;
                align-items: center;
            }
            #displayModeButton:hover {
                background-color: #C4544E;
                color: #ffffff;
            }
            #displayModeButton {
                padding: 4px 7px;
                font-family: Titillium Web, sans-serif;
                font-weight: 700;
                font-size: 11px;
                color: #C4544E;
                background-color: #ffffff;
                border: 2px solid #C4544E;
                border-radius: 5px;
                cursor: pointer;
                outline: none;
                text-transform: uppercase;
                margin-left: 5px; 
                margin-right: 5px; 
            }

            .display-mode-btn.active #displayModeButton {
                background-color: #C4544E;
                color: #ffffff;
            }
            .display-mode-btn #displayModeButton {
                transition: background-color 0.2s, color 0.2s;
            }
        </style>
    </head>
    <body>
        <h1><img src="https://i.postimg.cc/BnN3LVwq/Midiateca-Cores.png" alt="Logo" style="vertical-align: middle; height: 110px; margin-right: 10px; margin-top: 0px;">
            Midiateca em Cores</h1>

        <!-- Menu de organização dos Colordot -->
        <div class="menu">
            <ul>
                <li><a id="satMenu" href="#">Saturação</a></li>
                <li><a id="matizMenu" href="#">Matiz</a></li>
                <li><a id="brilhoMenu" href="#">Brilho</a></li>
                <!-- Dropdown para cidades -->
                <span>Cidade:</span>
                <select class="Dropdown" id="cidadeDropdown">
                    <option value="" disabled selected>Filtrar por cidade</option>
                    <option value="all">Mostrar tudo</option>
                </select>
                <!-- Dropdown para museus -->
                <span>Museu:</span>
                <select class="Dropdown" id="museuDropdown">
                    <option value="" disabled selected>Filtrar por instituição</option>
                    <option value="all">Mostrar tudo</option>
                </select>
                <input type="text" id="searchInput" placeholder="Filtrar por Termo">
                <li class="display-mode-btn" onclick="toggleDisplayMode()">
                    <button id="displayModeButton">Exibir Imagens</button>
                </li>

            </ul>
        </div>
            <div class ="dotbox" id="dotbox">'''

        # Gerar código HTML para cada cor
        for nome_arquivo in imagenscolor:
            image_url, item_page_url, hex_valor, instituicao, city, imagetext = imagenscolor[nome_arquivo]

            html += f'<a href="{item_page_url}" target="_blank"><div class="color-dot" id="color-dot" style="background-color: {hex_valor}" onmousemove="moveImagePreview(event, \'{image_url}\')" data-hex-value="{hex_valor}" data-image-url="{image_url}" data-museu="{instituicao}" data-cidade="{city}" data-imagetext="{imagetext}"></div></a>'
     
        html += '''</div>
            <div id="image-preview" style="position: absolute; display: none; width: 100px; height: 100px; border-radius: 30%; background-color: #000;"></div>'
                <script>
            // Função para alternar entre cor e imagem
            function toggleDisplayMode() {
                const colorDots = document.querySelectorAll(".color-dot");
                const displayModeButton = document.getElementById("displayModeButton");
                
                const buttonText = displayModeButton.innerHTML;
                displayModeButton.innerHTML = buttonText === "Exibir Imagens" ? "Exibir Cores" : "Exibir Imagens";

                displayModeButton.parentNode.classList.toggle("active");

                if (displayModeButton.parentNode.classList.contains("active")) {
                    colorDots.forEach(dot => {
                        const imageUrl = dot.dataset.imageUrl;
                        dot.style.backgroundImage = `url(${imageUrl})`;
                        dot.innerHTML = ""; 
                        if (!dot.dataset.originalWidth) {
                            dot.dataset.originalWidth = dot.style.width;
                            dot.dataset.originalHeight = dot.style.height;
                        }
                        
                        dot.style.width = "5vw";
                        dot.style.height = "5vw";
                        
                    });
                } else {
                    colorDots.forEach(dot => {
                        const hexValue = dot.dataset.hexValue;
                        dot.style.backgroundImage = ""; 
                        dot.style.backgroundColor = hexValue;
                        dot.style.width = dot.dataset.originalWidth;
                        dot.style.height = dot.dataset.originalHeight;  
                    });
                }
            }

            // Função para exibir a pre-visualização das imagens
            function moveImagePreview(event, image_url) {
                var previewDiv = document.getElementById("image-preview");
                previewDiv.style.display = "block";
                previewDiv.style.left = (event.pageX + 10) + "px";
                previewDiv.style.top = (event.pageY + 10) + "px";
                previewDiv.crossOriginResourcePolicy = false;
                previewDiv.style.backgroundImage = "url('" + image_url + "')";
                previewDiv.style.backgroundSize = "cover";
                previewDiv.style.backgroundPosition = "center";
            }

            // Função para expandir o menu mobile
            function toggleMenu() {
                var menuExpanded = document.querySelector('.menu-expanded');
                menuExpanded.style.display = (menuExpanded.style.display === 'block') ? 'none' : 'block';
            }

            // Função para expandir a metodologia
            function expandir() {
                var conteudoOculto = document.getElementById("conteudoOculto");
                var menuexp = document.getElementsByClassName("menuexp")[0];

                if (conteudoOculto.style.display === "none") {
                    conteudoOculto.style.display = "block";
                    menuexp.innerHTML = "<ul><li><a onclick='expandir()'>Recolher</a></li></ul>";
                } else {
                    conteudoOculto.style.display = "none";
                    menuexp.innerHTML = "<ul><li><a onclick='expandir()'>Expandir</a></li></ul>";
                }
            }

            // Função para converter um valor HEX em um objeto RGB
            function hexToRgb(hex) {
                const bigint = parseInt(hex.slice(1), 16);
                const r = (bigint >> 16) & 255;
                const g = (bigint >> 8) & 255;
                const b = bigint & 255;
                return { r, g, b };
            }

            // Função para calcular o brilho de um objeto RGB
            function calculateBrightness(rgb) {
                return (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
            }

            // Função para calcular a saturação e matiz de um objeto RGB
            function calculateSaturationAndHue(rgb) {
                const max = Math.max(rgb.r, rgb.g, rgb.b);
                const min = Math.min(rgb.r, rgb.g, rgb.b);
                
                const delta = max - min;
                const saturation = delta === 0 ? 0 : delta / max;
                
                let hue;
                if (delta === 0) {
                    hue = 0;
                } else if (max === rgb.r) {
                    hue = ((rgb.g - rgb.b) / delta) % 6;
                } else if (max === rgb.g) {
                    hue = (rgb.b - rgb.r) / delta + 2;
                } else {
                    hue = (rgb.r - rgb.g) / delta + 4;
                }
                
                hue = Math.round(hue * 60);
                if (hue < 0) {
                    hue += 360;
                }
                
                return { saturation, hue };
            }

            // Função para ordenar por brilho
            function sortColorDotsByBrightness() {
                const dotbox = document.getElementById('dotbox');
                const colorDots = [...dotbox.querySelectorAll('.color-dot')];

                colorDots.sort((a, b) => {
                    const aHex = a.getAttribute('data-hex-value');
                    const bHex = b.getAttribute('data-hex-value');
                    
                    const aRgb = hexToRgb(aHex);
                    const bRgb = hexToRgb(bHex);
                    
                    const aBrightness = calculateBrightness(aRgb);
                    const bBrightness = calculateBrightness(bRgb);
                    
                    return bBrightness - aBrightness;
                });

                colorDots.forEach(dot => {
                    const anchor = dot.parentElement; 
                    anchor.parentElement.appendChild(anchor);
                });
            }

            // Função para ordenar por matiz
            function sortColorDotsByHue() {
                const dotbox = document.getElementById('dotbox');
                const colorDots = [...dotbox.querySelectorAll('.color-dot')];

                colorDots.sort((a, b) => {
                    const aHex = a.getAttribute('data-hex-value');
                    const bHex = b.getAttribute('data-hex-value');
                    
                    const aRgb = hexToRgb(aHex);
                    const bRgb = hexToRgb(bHex);
                    
                    const aHue = calculateSaturationAndHue(aRgb).hue;
                    const bHue = calculateSaturationAndHue(bRgb).hue;
                    
                    return aHue - bHue;
                });

                colorDots.forEach(dot => {
                    const anchor = dot.parentElement;
                    anchor.parentElement.appendChild(anchor);
                });
            }

            // Função para ordenar por saturação
            function sortColorDotsBySaturation() {
                const dotbox = document.getElementById('dotbox');
                const colorDots = [...dotbox.querySelectorAll('.color-dot')];

                colorDots.sort((a, b) => {
                    const aHex = a.getAttribute('data-hex-value');
                    const bHex = b.getAttribute('data-hex-value');
                    
                    const aRgb = hexToRgb(aHex);
                    const bRgb = hexToRgb(bHex);
                    
                    const aSaturation = calculateSaturationAndHue(aRgb).saturation;
                    const bSaturation = calculateSaturationAndHue(bRgb).saturation;
                    
                    return bSaturation - aSaturation;
                });

                colorDots.forEach(dot => {
                    const anchor = dot.parentElement; 
                    anchor.parentElement.appendChild(anchor); 
                });
            }

            // Adicionar event listeners para os menus de ordenação

            const brilhoMenu = document.getElementById('brilhoMenu');
            brilhoMenu.addEventListener('click', () => sortColorDotsByBrightness());

            const matizMenu = document.getElementById('matizMenu');
            matizMenu.addEventListener('click', () => sortColorDotsByHue());

            const satMenu = document.getElementById('satMenu');
            satMenu.addEventListener('click', () => sortColorDotsBySaturation());

            // Script pesquisa por Termos
            document.getElementById('searchInput').addEventListener('input', function() {
                var searchValue = this.value.toLowerCase();
                var colorDots = document.getElementsByClassName('color-dot');

                for (var i = 0; i < colorDots.length; i++) {
                    var dot = colorDots[i];
                    var imagetext = dot.getAttribute('data-imagetext').toLowerCase();

                    if (imagetext.includes(searchValue)) {
                        dot.style.display = 'inline-block';
                    } else {
                        dot.style.display = 'none';
                    }
                }
            });

            // Script Wordcloud
            document.addEventListener("DOMContentLoaded", function() {
                const wordContainer = document.querySelector(".word-cloud-container");
                const colorDotElements = document.querySelectorAll(".color-dot");

                const excludedWords = ["de","do","g","que","mais","ao","foi","dos","se","caso","por", "da", "e", "a", "o", "em", "para", "com", "um", "uma", "os", "as", "no", "na", "nos", "nas", "$", "�", "é", "essa","à","á","tem","das","vai","até","ser","diz","conteúdo","há","está","incluso", "possui", "constam","inclusos", "verso" ];

                const wordFrequency = {};

                colorDotElements.forEach(element => {
                    const words = element.getAttribute("data-imagetext").split(" ");
                    
                    words.forEach(word => {
                        word = word.toLowerCase().trim();
                        
                        if (!excludedWords.includes(word) && /^[a-zA-ZÀ-ÿçÇ]+$/.test(word)) {
                            if (word in wordFrequency) {
                                wordFrequency[word]++;
                            } else {
                                wordFrequency[word] = 1;
                            }
                        }
                    });
                });

                const sortedWords = Object.keys(wordFrequency).sort((a, b) => wordFrequency[b] - wordFrequency[a]);
                const topWords = sortedWords.slice(0, 50);

                const shuffledTopWords = topWords.sort(() => Math.random() - 0.5); // Emabalhamento das palavras

                shuffledTopWords.forEach(word => {
                    const wordElement = document.createElement("span");
                    wordElement.textContent = word;
                    wordElement.classList.add("searchable-word"); 
                    const fontSize = (wordFrequency[word] / sortedWords.length) * 150 + 10; // Ajuste de tamanhos
                    wordElement.style.fontSize = `${fontSize}px`;
                    wordContainer.appendChild(wordElement);

                    // Função para permitir o click na palavra
                    wordElement.addEventListener("click", function() {
                        document.getElementById('searchInput').value = word;
                        document.getElementById('searchInput').dispatchEvent(new Event('input'));
                    });
                });
            });


            var colorDots = document.querySelectorAll("#color-dot");
            var cidadeDropdown = document.getElementById("cidadeDropdown");
            var museuDropdown = document.getElementById("museuDropdown");
            var cidadesSet = new Set();
            var museusSet = new Set();

            // Define os museus e cidades de acordo com a API
            colorDots.forEach(function (colorDot) {
            var dataMuseu = colorDot.getAttribute("data-museu");
            var dataCidade = colorDot.getAttribute("data-cidade");
            
            museusSet.add(dataMuseu);
            cidadesSet.add(dataCidade);
            });

            cidadesSet.forEach(function (cidade) {
            var cidadeOption = document.createElement("option");
            cidadeOption.value = cidade;
            cidadeOption.text = cidade;
            cidadeDropdown.appendChild(cidadeOption);
            });

            museusSet.forEach(function (museu) {
            var museuOption = document.createElement("option");
            museuOption.value = museu;
            museuOption.text = museu;
            museuDropdown.appendChild(museuOption);
            });

            cidadeDropdown.addEventListener("change", filtrarElementos);
            museuDropdown.addEventListener("change", filtrarElementos);

            // Função para filtrar os elementos de acordo com a cidade ou museu
            function filtrarElementos() {
            var cidadeSelecionada = cidadeDropdown.value;
            var museuSelecionado = museuDropdown.value;

            colorDots.forEach(function (colorDot) {
                var dataMuseu = colorDot.getAttribute("data-museu");
                var dataCidade = colorDot.getAttribute("data-cidade");

                // Verifica se o elemento corresponde à seleção de cidade ou museu
                var correspondeCidade = cidadeSelecionada === "" || cidadeSelecionada === "all" || cidadeSelecionada === dataCidade;
                var correspondeMuseu = museuSelecionado === "" || museuSelecionado === "all" || museuSelecionado === dataMuseu;

                // Oculte ou mostre o elemento com base na correspondência
                if (correspondeCidade && correspondeMuseu) {
                colorDot.style.display = "block"; // Mostrar o elemento
                } else {
                colorDot.style.display = "none"; // Ocultar o elemento
                }
            });
            }
        </script>
        <div style="text-align: center; color: #C4544E; font-family: Titillium Web, sans-serif; font-weight: 700; font-size: 20px; padding: 8px; margin-top: -15px;">
            <span style="display: inline-block; margin-top: -30px;">Palavras Recorrentes</span>
        </div>
        <div class="word-cloud-container"></div>
         <div style="background-color: #C4544E; text-align: center; color: white; font-family: Titillium Web, sans-serif; font-weight: 700; font-size: 20px; padding: 8px;">
            <span style="display: inline-block; margin-right: 10px;">Metodologia de Desenvolvimento</span>
            <div id="btnExpandir" class="menuexp">
                <ul>
                    <li><a onclick="expandir()">Expandir</a></li>
                </ul>
            </div>
        </div>                  
        <div id="conteudoOculto" style="display: none;">
            <div>
                <div style="display: flex; justify-content: center; align-items: center;">
                    <img src="https://i.postimg.cc/MGqp5wnp/Cores-Da-Midiateca-Organocgrama.png" alt="Logo" style="width: 80vw; max-height: 600px; margin-top: 2vh; margin-bottom: 2vh;">
                </div>
            </div>
        </div>
        <div class="footer"><a href="https://midiateca.es.gov.br/" target="_blank">
        <img src="https://midiateca.es.gov.br/site/wp-content/uploads/2022/04/Logo_da_Midiateca_Capixaba-2-1024x344.png" alt="Logo" style="vertical-align: middle; height: 40px; margin-right: 40px;">
        <img src="https://i.postimg.cc/vZ0C9mzL/Logo-Labic-2.png" alt="Logo" style="vertical-align: middle; height: 30px; margin-right: 40px;">
        <img src="https://servicos.fapes.es.gov.br/fapes_imposto/assets/images/logo%20branca.png" alt="Logo" style="vertical-align: middle; height: 30px; margin-right: 40px;">
        <img src="https://i.postimg.cc/x1vPmp3v/secult-horizontal.png" alt="Logo" style="vertical-align: middle; height: 60px; margin-right: 40px;">
        </div>
    </body>
</html>'''

        pastahtml = "data"
        # Salvar arquivo HTML para cada opção de cor
        ordem_nomes = ["MidiatecaEmCores"]
        caminho_arquivo_html = os.path.join(pastahtml, f'{ordem_nomes[i]}.html')
        with open(caminho_arquivo_html, 'w', encoding='utf-8') as file:
            file.write(html)
            print(f"A visualização HTML {ordem_nomes[i]} foi gerada com sucesso.")

print('Atualizar banco de imagens via API Tainacan?')
print('1 - Sim')
print('2 - Não')
optionapi = input('Digite a opção:')
if optionapi == '1':
    midiateca_api()
    print('Fazer analise de cor?')
    print('1 - Sim')
    print('2 - Não')
    optioncolor = input('Digite a opção:')
    if optioncolor == '1':
        colors()
        generate_html_visualization()
    elif optioncolor == '2':
        generate_html_visualization()
    else:
        print('Opção invalida')
elif optionapi == '2':
    print('Fazer analise de cor?')
    print('1 - Sim')
    print('2 - Não')
    optioncolor = input('Digite a opção:')
    if optioncolor == '1':
        colors()
        generate_html_visualization()
    elif optioncolor == '2':
        generate_html_visualization()
    else:
        print('Opção invalida')
else:
    print('Opção invalida')
