# Midiateca em Cores

Este repositório contém um código em Python chamado `Midiateca_em_cores.py` que realiza o download de imagens da Midiateca do Espírito Santo e extrai as cores dominantes dessas imagens. Em seguida, o código gera um arquivo HTML interativo que visualiza as imagens organizadas por cores dominantes em diferentes ordens.

## Requisitos

Certifique-se de ter os seguintes requisitos instalados no seu ambiente de desenvolvimento antes de executar o código:

-   Python 3.x
-   Bibliotecas Python: `colorthief==0.2.1`, `pandas==2.0.1`, `Pillow==9.5.0`, `requests==2.31.0`, `tqdm==4.65.0`

Você pode instalar essas dependências usando o comando:

    pip install -r requirements.txt

## Uso

1.  Clone o repositório para o seu ambiente de desenvolvimento:

    `git clone https://github.com/labic/MidiatecaEmCores`

2.  Navegue até o diretório clonado:

    `cd midiateca-em-cores`

3.  Execute o código Python:

    `python Midiateca_em_cores.py`

4.  O código fará o download das imagens da Midiateca através da API e extrairá as cores dominantes. Em seguida, ele gerará os arquivos HTML de visualização das imagens organizadas por cores.
    
5.  Abra o arquivo HTML de visualização desejado em um navegador da web para visualizar as imagens organizadas por cores.
    
## Arquivos gerados

-   `dataimages.csv`: um arquivo CSV que contém os dados extraidos da API e a cor dominante extraida pelo script.
-   `MidiatecaEmCores.html`: arquivo HTML que mostram as imagens organizadas por cores dominantes.

## Estrutura do código

O código `Midiateca_em_cores.py` possui as seguintes seções principais:

1.  Importação de bibliotecas: Importa todas as bibliotecas necessárias para o código.
    
2.  Configurações: Define as configurações iniciais, como o intervalo de páginas para baixar as imagens, a lista de URLs contendo JSON e o diretório de destino para salvar as imagens.
    
3.  Função `midiateca_api()`: Implementa o processo de download das imagens da Midiateca e a extração das informações relevantes de cada imagem. As informações são salvas em um arquivo CSV chamado `dataimages.csv`.
    
4.  Função `colors()`: Extrai as cores dominantes de todas as imagens baixadas usando a biblioteca `ColorThief`. As informações são salvas no arquivo `dataimage.csv`.
    
5.  Função `hex_to_hsl()`: Converte uma cor em formato HEX para formato HSL (Matiz, Saturação, Luminosidade).
    
6.  Função `generate_html_visualization()`: Gera um código HTML interativo para visualizar as imagens organizadas de acordo com diferentes critérios de ordenação das cores dominantes.

## Metodologia de Desenvolvimento

A metodologia de desenvolvimento utilizada neste projeto foi a seguinte:

1.  **Análise de requisitos:** Compreender os requisitos do projeto e identificar as necessidades específicas, como download de imagens, extração de cores e visualização.
2.  **Pesquisa e seleção de bibliotecas:** Realizar pesquisa para encontrar bibliotecas Python adequadas para realizar as tarefas necessárias, como solicitações HTTP, manipulação de imagens e extração de cores.
3.  **Configuração do ambiente:** Instalar as bibliotecas necessárias usando o gerenciador de pacotes `pip` e configurar o ambiente de desenvolvimento.
4.  **Desenvolvimento incremental:** Dividir o projeto em etapas menores e implementar cada etapa incrementalmente, testando e depurando conforme avançava.
5.  **Design da pagina:** Analisar a identidade visual da Midiateca e desenvolver um modelo HTML compativel com o codigo.
6.  **Integração e teste:** Integração das diferentes partes do projeto e realização de testes para verificar se o sistema está funcionando corretamente.
7.  **Otimização e aprimoramento:** Identificar possíveis melhorias no desempenho, usabilidade e qualidade do código, implementando as alterações necessárias.

## Sobre

Este projeto foi desenvolvido como parte da Midiateca Capixaba, uma iniciativa da Secretaria de Cultura do Espirito Santo em parceira com o Laboratório de Estudos sobre Imagem e Cibercultura (Labic) e a Fundação de Amparo à Pesquisa e Inovação do Espírito Santo (FAPES).

-   Midiateca em Cores:  [Midiateca em Cores](https://www.labic.net/mvm/MidiatecaEmCores.html)
-   Midiateca Capixaba:  [https://midiateca.es.gov.br/](https://midiateca.es.gov.br/)
-   Labic:  [https://labic.net/](https://labic.net/)
-   FAPES:  [https://fapes.es.gov.br/](https://fapes.es.gov.br/)
