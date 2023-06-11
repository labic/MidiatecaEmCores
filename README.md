# Midiateca em Cores
Este repositório contém um código Python que gera visualizações HTML de cores dominantes a partir de arquivos CSV. Essas visualizações são usadas na Midiateca em Cores, uma aplicação web para explorar e navegar por imagens com base em suas cores dominantes.

## Pré-requisitos
Certifique-se de ter os seguintes requisitos instalados:

 - Python 3.x

## Como usar

### Clone este repositório em sua máquina local:

    git clone https://github.com/labic/MidiatecaEmCores

### Navegue até o diretório do projeto:

    cd MidiatecaEmCores

### Instale as dependências necessárias:

    pip install -r requirements.txt

### Execute o código Python para gerar as visualizações HTML:

    python MidiatecaEmCores.py

As visualizações HTML serão geradas no diretório do projeto.


## Arquivos

-   `MidiatecaEmCores.py`: Contém o código Python responsável por gerar as visualizações HTML.
-   `colors.py`: Contém o código Python responsável por extrair as cores dominantes das imagens.
-   `midiatecaAPI_Thumb.py`: Contém o código Python para baixar as imagens da Midiateca usando a API.
-   `cores_dominantes.csv`: Arquivo CSV contendo as cores dominantes das imagens.
-   `imagensthumb.csv`: Arquivo CSV contendo informações das imagens.
-   `imagensthumb2/`: Diretório de destino para salvar as imagens baixadas.

# Visualizações HTML

As visualizações HTML geradas são baseadas na ordem das cores escolhida pelo usuário. São gerados quatro arquivos HTML correspondentes a diferentes ordenações das cores:

-   `visualization1.html`: Visualização das cores ordenadas por temperatura.
-   `visualization2.html`: Visualização das cores ordenadas por matiz.
-   `visualization3.html`: Visualização das cores ordenadas por brilho.
-   `visualization4.html`: Visualização das cores ordenadas por saturação.

Cada visualização apresenta uma interface interativa que permite visualizar as cores dominantes das imagens e obter informações adicionais ao passar o mouse sobre cada cor.

##   Metodologia de Desenvolvimento

Este projeto foi desenvolvido utilizando a linguagem Python e as bibliotecas CSV e PIL para processar os arquivos de entrada e gerar as visualizações HTML. A metodologia de desenvolvimento seguiu as seguintes etapas:

1.  Desenvolvimento do código `midiatecaAPI_Thumb.py`: Nesta etapa, foi criado o código responsável por fazer o download das imagens de cada item do acervo da Midiateca e gerar um arquivo CSV contendo o código da imagem, a URL da thumbnail e a URL do item no acervo.
    
2.  Utilização do código `colors.py`: Nesta etapa, foi utilizado o código responsável por extrair a cor dominante de cada imagem. O código percorre as imagens baixadas, utilizando a biblioteca ColorThief, e gera um arquivo CSV associando o código de cada imagem à sua cor dominante.
    
3.  Desenvolvimento do código `MidiatecaEmCores.py`: Nesta etapa, foi criado o código responsável pela construção do HTML de cada visualização. O código lê os arquivos CSV gerados anteriormente, seleciona a ordem desejada das cores e gera o código HTML correspondente para cada opção de cor.

Essa metodologia permitiu a construção do projeto de forma modular, onde cada código desempenha uma função específica, desde o download das imagens até a geração das visualizações HTML. Dessa forma, foi possível obter as cores dominantes das imagens e apresentá-las em uma interface visual atraente.

O projeto também inclui um diagrama organizacional que ilustra a estrutura da Midiateca em Cores e uma seção de rodapé com os logotipos das instituições envolvidas.


## Sobre

Este projeto foi desenvolvido como parte da Midiateca Capixaba, uma iniciativa da Secretaria de Cultura do Espirito Santo em parceira com o Laboratório de Estudos sobre Imagem e Cibercultura (Labic) e a Fundação de Amparo à Pesquisa e Inovação do Espírito Santo (FAPES).

-   Midiateca em Cores: [Midiateca em Cores](https://www.labic.net/pulsao/visualization1.html)
-   Midiateca Capixaba: [https://midiateca.es.gov.br/](https://midiateca.es.gov.br/)
-   Labic: [https://labic.net/](https://labic.net/)
-   FAPES: [https://fapes.es.gov.br/](https://fapes.es.gov.br/)
