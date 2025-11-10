import os
import time
# -*- coding: utf-8 -*-
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env com codificação Latin-1 para lidar com caracteres especiais no Windows
load_dotenv(encoding='latin-1')

from ai_agent import AIAgent

def run_tests():
    """
    Carrega as variáveis de ambiente e executa uma série de perguntas de teste
    através do AIAgent.
    """
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Chave da API Gemini não encontrada. Verifique o arquivo .env.")
        return

    # Instancia o agente de IA
    agent = AIAgent()

    # Lista de perguntas para testar
    test_questions = [
        "Qual celular vendeu mais em junho de 2024?",
        "qual foi valor de vendas de outubro de 2024?",
        "quanto vendeu de cada aparelho em fevereiro de 2025?",
        "quais 3 celulares que venderam mais e qual valor de cada em maio de 2025?"
    ]

    # Itera sobre cada pergunta, processa e imprime a resposta
    for i, question in enumerate(test_questions):
        print(f"\n==================== PERGUNTA {i+1} ====================")
        print(f"Pergunta: {question}")
        
        # Processa a mensagem usando o agente
        response = agent.process_message(question)
        
        print("\n---------- Resposta do Agente ----------")
        print(response)
        print("----------------------------------------")
        time.sleep(20)  # Adiciona um atraso de 20 segundos

if __name__ == "__main__":
    run_tests()