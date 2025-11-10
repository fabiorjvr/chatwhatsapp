# Chatbot de Análise de Vendas de Smartphones

Este projeto consiste em um agente de IA (chatbot) desenvolvido em Python, capaz de se conectar a um banco de dados PostgreSQL e responder a perguntas complexas em linguagem natural sobre dados de vendas de smartphones.

## Funcionalidades

O chatbot pode responder a uma variedade de perguntas de negócios, incluindo:

- **Desempenho de Produtos:**
  - Identificar os produtos mais e menos vendidos.
  - Obter o total de vendas para um produto específico.
- **Análise de Receita:**
  - Calcular a receita total anual ou mensal.
  - Identificar o mês com a maior receita.
- **Análise de Mercado:**
  - Comparar o desempenho de vendas entre diferentes fabricantes.
  - Calcular a participação de mercado de cada fabricante.
- **Análise Comparativa:**
  - Comparar as vendas de múltiplos produtos em uma única pergunta.

## Tecnologias Utilizadas

- **Linguagem:** Python 3
- **IA e Processamento de Linguagem Natural:** Google Generative AI (Gemini)
- **Banco de Dados:** PostgreSQL
- **Conexão com Banco de Dados:** `psycopg2-binary`
- **Gerenciamento de Variáveis de Ambiente:** `python-dotenv`

## Estrutura do Projeto

- `ai_agent.py`: O cérebro do chatbot, responsável por processar as mensagens, selecionar ferramentas e formatar as respostas.
- `tools.py`: Contém o conjunto de ferramentas que o agente usa para interagir com o banco de dados.
- `test_agent.py`: Script de teste para validar o funcionamento do agente com uma série de perguntas predefinidas.
- `setup.sql`: Scripts SQL para criar o banco de dados e a tabela.
- `vendas_smartphones.csv`: Dados de exemplo para popular o banco de dados.
- `.env`: Arquivo para armazenar a chave da API do Google (não versionado).

## Como Configurar e Executar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/fabiorjvr/chatwhatsapp.git
    cd chatwhatsapp
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados PostgreSQL:**
    - Certifique-se de ter o PostgreSQL instalado e em execução.
    - Crie um banco de dados chamado `loja_celulares`.
    - Execute os scripts `create_table.sql` e `populate_sales.sql` para configurar a tabela e popular os dados.

5.  **Configure as Variáveis de Ambiente:**
    - Renomeie o arquivo `.env.example` para `.env` (se houver) ou crie um novo.
    - Adicione sua chave da API do Google Gemini ao arquivo `.env`:
      ```
      GOOGLE_API_KEY="SUA_API_KEY_AQUI"
      ```

6.  **Execute o script de teste para validar:**
    ```bash
    python test_agent.py
    ```