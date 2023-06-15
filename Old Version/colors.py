import os
import csv
from colorthief import ColorThief

diretorio = input("Insira o caminho para o diretorio das Imagens:")
arquivo_saida = "cores_dominantes.csv"

# Lista de todas as imagens no diretório
imagens = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

# Abrir o arquivo de saída para escrita
with open(arquivo_saida, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Image_Name", "HEX", "R", "G", "B"])

    # Percorrer todas as imagens
    for imagem_nome in imagens:
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
            
            print(f"Analisada a imagem: {imagem_nome}")
        except Exception as e:
            print(f"Erro ao analisar a imagem {imagem_nome}: {str(e)}")
