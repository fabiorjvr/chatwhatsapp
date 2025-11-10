import os
import time
from ai_agent import AIAgent
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def run_tests():
    """
    Executa uma série de perguntas de teste para o agente de IA e imprime as respostas.
    """
    agent = AIAgent()

    questions = [
        "Qual foi o produto mais vendido em janeiro de 2024?",
        "Qual foi a receita total no ano de 2024?",
        "Quantas unidades do 'iPhone 15 Pro Max' foram vendidas em 2024?",
        "Qual a receita total de vendas da 'Samsung' em 2024?",
        "Quais foram os 3 produtos mais vendidos em dezembro de 2024?",
        "Qual a média de unidades vendidas por mês em 2024?",
        "Qual o mês com a maior receita em 2024?",
        "Qual o produto com a menor receita em 2024?",
        "Qual a participação de mercado (em receita) de cada fabricante em 2024?",
        "Compare as vendas do 'iPhone 15 Pro Max' e do 'Samsung Galaxy S24 Ultra' em 2024."
    ]

    for i, question in enumerate(questions):
        print(f"--- Pergunta {i+1}: {question} ---")
        response = agent.process_message(question)
        print(f"Resposta: {response}\n")
        time.sleep(65) # Adiciona um intervalo de 65 segundos

if __name__ == "__main__":
    run_tests()