# Midiateca em Cores
Este repositório contém um código Python que gera visualizações HTML de cores dominantes a partir de arquivos CSV. Essas visualizações são usadas na Midiateca em Cores, uma aplicação web para explorar e navegar por imagens com base em suas cores dominantes.

## Pré-requisitos
Certifique-se de ter os seguintes requisitos instalados:

 - Python 3.x

## Como usar

### Clone este repositório em sua máquina local:

    git clone https://github.com/seu-usuario/nome-do-repositorio.git

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

## Visualizações HTML

As visualizações HTML geradas são baseadas na ordem das cores escolhida pelo usuário. São gerados quatro arquivos HTML correspondentes a diferentes ordenações das cores:

-   `visualization1.html`: Visualização das cores ordenadas por temperatura.
-   `visualization2.html`: Visualização das cores ordenadas por matiz.
-   `visualization3.html`: Visualização das cores ordenadas por brilho.
-   `visualization4.html`: Visualização das cores ordenadas por saturação.

Cada visualização apresenta uma interface interativa que permite visualizar as cores dominantes das imagens e obter informações adicionais ao passar o mouse sobre cada cor.

## Metodologia de Desenvolvimento

Este projeto foi desenvolvido utilizando a linguagem Python e a biblioteca CSV para processar os arquivos de entrada e gerar as visualizações HTML. A metodologia de desenvolvimento seguiu as seguintes etapas:

1.  Carregar os dados das cores dominantes e das imagens a partir dos arquivos CSV.
2.  Solicitar ao usuário a ordem desejada das cores.
3.  Gerar o código HTML correspondente a cada opção de cor.
4.  Salvar os arquivos HTML para cada opção de cor.

O projeto também inclui um diagrama organizacional que ilustra a estrutura da Midiateca em Cores e uma seção de rodapé com os logotipos das instituições envolvidas.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas (issues) ou enviar solicitações de pull (pull requests) para melhorar este projeto.

## Sobre

Este projeto foi desenvolvido como parte da Midiateca Capixaba, uma iniciativa da Secretaria de Cultura do Espirito Santo em parceira com o Laboratório de Estudos sobre Imagem e Cibercultura (Labic) e a Fundação de Amparo à Pesquisa e Inovação do Espírito Santo (FAPES).

-   Midiateca em Cores: [Midiateca em Cores](https://www.labic.net/pulsao/visualization1.html)
-   Midiateca Capixaba: [https://midiateca.es.gov.br/](https://midiateca.es.gov.br/)
-   Labic: [https://labic.net/](https://labic.net/)
-   FAPES: [https://fapes.es.gov.br/](https://fapes.es.gov.br/)
