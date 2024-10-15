# Projeto: Análise de Redes Políticas e Visualização de Dados

## Descrição

Este projeto consiste em uma interface bot, desenvolvida como parte da disciplina AEDS3, para analisar e visualizar redes políticas. Utilizando a biblioteca `networkx` para a criação de grafos, o sistema mapeia conexões políticas com base em dados de votação e filiação partidária dos deputados, gerando gráficos, heatmaps e medidas de centralidade, facilitando a visualização da influência política.

## Funcionalidades

- **Leitura de Arquivos**: O programa lê arquivos que contêm informações sobre políticos, seus partidos e seus votos.
- **Geração de Grafos**: Criação de grafos que representam conexões entre políticos com base em suas relações e partidos.
- **Normalização de Pesos**: Os grafos são normalizados considerando os votos dos políticos.
- **Filtragem por Threshold**: Aplicação de um threshold (percentual mínimo de concordância) para remover arestas menos relevantes.
- **Cálculo de Centralidade**: Geração de gráficos de centralidade de intermediação (betweenness) para identificar políticos mais influentes.
- **Geração de Heatmaps**: Criação de heatmaps para visualização das conexões políticas.
- **Interface Telegram**: Um bot interativo que recebe comandos e parâmetros do usuário via Telegram e gera os gráficos e resultados solicitados.

## Estrutura do Projeto

### Arquivos Principais

1. **`program_logic.py`**:
    - Contém toda a lógica de análise e manipulação dos dados.
    - Gera gráficos e visualizações com base nos dados fornecidos.
2. **`telegram_bot.py`**:
    - Implementa um bot do Telegram que interage com o usuário.
    - Coleta informações sobre o ano, partidos e threshold, gerando gráficos e respondendo diretamente no chat.

### Bibliotecas Utilizadas

- `networkx`: Para a criação e manipulação de grafos.
- `matplotlib`: Para a geração de gráficos e visualizações.
- `numpy`: Para trabalhar com matrizes e cálculos numéricos.
- `random`: Para gerar cores aleatórias nos nós dos grafos.
- `re`: Para manipulação de strings e padrões, como a inversão de cores hexadecimais.
- `telegram.ext`: Para integração com o Telegram e criação do bot interativo.

## Como Executar

1. **Configuração Inicial**:
    
    - Certifique-se de instalar as dependências:
    ```bash
        pip install -r requirements.txt
    ```
2. **Rodando via terminal**:
    
    - Execute `program_logic.py` diretamente no terminal:
    ```bash
        python program_logic.py
    ```
    - O programa solicitará os parâmetros: ano, partidos e threshold, e, em seguida, gerará os gráficos.
    - Obs: ao rodar via terminal, caso queira incluir todos os partidos, pressione _Enter_ quando solicitado.
3. **Rodando via Telegram**:
    
    - Substitua o token do bot no arquivo `telegram_bot.py` e execute:
    ```bash
        python telegram_bot.py
    ```
    - Interaja com o bot no Telegram para gerar gráficos e visualizações diretamente no chat.

## Exemplo de Uso

Ao iniciar o bot no Telegram:

- Ele solicitará o ano e os partidos que você deseja analisar.
- Em seguida, o bot pedirá o threshold de concordância entre 0 e 1.
- Após o processamento, o bot enviará gráficos de centralidade, heatmaps e a visualização do grafo.
