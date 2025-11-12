# -*- coding: utf-8 -*- 
from dotenv import load_dotenv
load_dotenv()

from groq import Groq
import os
import json
from tools import DatabaseTools
import sys
import inspect
import re

class AIAgent:
    """
    Agente de IA que interpreta perguntas e consulta o banco de dados usando a API Groq.
    """

    def __init__(self):
        self.db_tools = DatabaseTools()
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("A chave da API Groq não foi encontrada. Verifique o arquivo .env e a variável GROQ_API_KEY.")
        
        self.client = Groq(api_key=groq_api_key)
        self.model_name = "llama-3.1-8b-instant"

        # Converte as funções da classe DatabaseTools para o formato de ferramentas da API Groq/OpenAI
        self.tools = self._get_tools_definitions()
        self.system_prompt = self._build_system_prompt()

    def _get_tools_definitions(self) -> list:
        """
        Gera as definições das ferramentas para a API do Groq a partir da classe DatabaseTools,
        inspecionando as assinaturas das funções e analisando seus docstrings.
        """
        tool_definitions = []
        # Itera sobre todos os membros da classe DatabaseTools
        for name, func in inspect.getmembers(self.db_tools, inspect.isfunction):
            # Ignora funções privadas ou que não são destinadas a serem ferramentas
            if name.startswith("_") or name in ['conectar_banco', 'executar_query', 'fechar_conexao']:
                continue

            # Analisa o docstring para extrair a descrição principal e dos parâmetros
            docstring = inspect.getdoc(func)
            if not docstring:
                continue

            # A primeira linha é a descrição da função
            description_match = re.match(r"^(.*?)\n", docstring, re.DOTALL)
            description = description_match.group(1).strip() if description_match else "Sem descrição."

            # Extrai descrições de parâmetros do docstring (formato: "- nome (tipo): descrição")
            param_docs = dict(re.findall(r"-\s+([a-zA-Z_]+)\s+\([^)]+\):\s+(.*)", docstring))

            # Inspeciona a assinatura da função para obter os parâmetros
            sig = inspect.signature(func)
            parameters = sig.parameters
            
            tool_params = {
                "type": "object",
                "properties": {},
                "required": [],
            }

            # Itera sobre os parâmetros da função (ignorando 'self')
            for param_name, param in parameters.items():
                if param_name == 'self':
                    continue
                
                # Mapeia tipos Python para tipos JSON Schema
                param_type = "string"
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list:
                    param_type = "array"

                # Adiciona a definição do parâmetro
                tool_params["properties"][param_name] = {
                    "type": param_type,
                    "description": param_docs.get(param_name, ""),
                }

                # Adiciona à lista de parâmetros obrigatórios se não tiver valor padrão
                if param.default is inspect.Parameter.empty:
                    tool_params["required"].append(param_name)
            
            # Adiciona a definição completa da ferramenta
            tool_definitions.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": tool_params,
                },
            })
            
        return tool_definitions

    def _build_system_prompt(self) -> str:
        return '''
Você é um assistente de vendas de smartphones. Sua principal tarefa é analisar as perguntas do usuário e usar as ferramentas disponíveis para consultar um banco de dados de vendas.

**REGRAS DE OURO:**
1.  **SEMPRE USE UMA FERRAMENTA:** Para qualquer pergunta sobre vendas (produtos, receita, comparações, etc.), você DEVE usar uma das ferramentas. Não tente responder com base no seu conhecimento geral.
2.  **ANO PADRÃO = 2024:** Se o usuário não especificar o ano em sua pergunta, você DEVE assumir o ano de 2024 para todas as consultas.
3.  **SEJA DIRETO:** Forneça respostas claras, diretas e informativas com base nos dados retornados pelas ferramentas.
4.  **INFORME QUANDO NÃO HÁ DADOS:** Se uma ferramenta não retornar resultados, informe ao usuário de forma explícita que a informação não foi encontrada para os critérios solicitados.
5.  **NÃO INVENTE:** Nunca invente dados ou informações. Sua base de conhecimento é estritamente o que as ferramentas fornecem.
'''

    def _format_response(self, tool_name: str, data: list) -> str:
        """Formata os dados em resposta amigável."""
        if not data or ("erro" in data[0]):
            return f"❌ Não encontrei dados para essa consulta. Detalhe: {data[0].get('erro')}"

        try:
            if tool_name == "get_top_products":
                if len(data) == 1:
                    p = data[0]
                    return f"📱 O produto mais vendido foi:\n\n🏆 {p['modelo']} ({p['fabricante']})\n   {p['unidades_vendidas']:,} unidades vendidas\n   💰 R$ {p['receita_total']:,.2f}"
                else:
                    lines = ["📊 Ranking dos produtos mais vendidos:\n"]
                    for i, p in enumerate(data, 1):
                        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
                        lines.append(f"{emoji} {p['modelo']} ({p['fabricante']})")
                        lines.append(f"   📦 {p['unidades_vendidas']:,} unidades")
                        lines.append(f"   💰 R$ {p['receita_total']:,.2f}\n")
                    return "\n".join(lines)

            elif tool_name == "get_monthly_revenue":
                d = data[0]
                return f"💰 **Receita Total:** R$ {d['receita_total']:,.2f}\n📦 **Total de Unidades:** {d['total_unidades']:,}"

            elif tool_name == "get_product_sales_by_month":
                lines = ["📊 **Vendas do mês**:\n"]
                if len(data) > 10:
                    lines = [f"📊 **Vendas do mês** (mostrando top 10 de {len(data)} produtos):\n"]
                    data_to_show = data[:10]
                else:
                    data_to_show = data
                for p in data_to_show:
                    lines.append(f"📱 {p['modelo']} ({p['fabricante']})")
                    lines.append(f"   📦 {p['unidades_vendidas']:,} unidades")
                    lines.append(f"   💰 R$ {p['receita']:,.2f}\n")
                return "\n".join(lines)

            elif tool_name == "get_product_sales":
                if data:
                    p = data[0]
                    return f"📱 Vendas de {p['modelo']} ({p['fabricante']}):\n\n   📦 {p['unidades_vendidas']:,} unidades vendidas\n   💰 R$ {p['receita']:,.2f}"
                else:
                    return "❌ Não encontrei dados para esse produto."

            elif tool_name == "get_comparison_by_manufacturer":
                lines = ["📊 **Comparativo por Fabricante**:\n"]
                for fab in data:
                    lines.append(f"🏢 **{fab['fabricante']}**")
                    lines.append(f"   📦 Total de Unidades: {fab['total_unidades']:,}")
                    lines.append(f"   💰 Receita Total: R$ {fab['receita_total']:,.2f}\n")
                return "\n".join(lines)

            elif tool_name == "get_average_monthly_sales":
                d = data[0]
                return f"📊 **Média Mensal de Vendas**:\n\n   💰 Faturamento Médio: R$ {d['media_receita']:,.2f}\n   📦 Unidades Médias: {d['media_unidades']:,}"

            elif tool_name == "get_best_selling_month":
                d = data[0]
                return f"🏆 **Melhor Mês de Vendas**:\n\n   🗓️ Mês: {d['mes_nome']}\n   💰 Faturamento: R$ {d['receita_total']:,.2f}\n   📦 Unidades Vendidas: {d['total_unidades']:,}"

            elif tool_name == "get_least_sold_products":
                if len(data) == 1:
                    p = data[0]
                    return f"📉 O produto menos vendido foi:\n\n   {p['modelo']} ({p['fabricante']})\n   {p['unidades_vendidas']:,} unidades vendidas\n   💰 R$ {p['receita_total']:,.2f}"
                else:
                    lines = ["📉 Ranking dos produtos menos vendidos:\n"]
                    for i, p in enumerate(data, 1):
                        lines.append(f"{i}º {p['modelo']} ({p['fabricante']})")
                        lines.append(f"   📦 {p['unidades_vendidas']:,} unidades")
                        lines.append(f"   💰 R$ {p['receita_total']:,.2f}\n")
                    return "\n".join(lines)

            elif tool_name == "get_multiple_product_sales":
                lines = ["📊 **Comparativo de Vendas**:\n"]
                for p in data:
                    lines.append(f"📱 {p['modelo']} ({p['fabricante']})")
                    lines.append(f"   📦 {p['unidades_vendidas']:,} unidades vendidas")
                    lines.append(f"   💰 R$ {p['receita_total']:,.2f}\n")
                return "\n".join(lines)

        except (KeyError, IndexError) as e:
            return f"😕 Desculpe, não consegui formatar a resposta. Detalhe do erro: {e}"
        except Exception as e:
            return f"🐞 Ocorreu um erro inesperado ao formatar a resposta: {e}"

    def process_message(self, user_message: str) -> str:
        """
        Processa a mensagem do usuário, chama a IA e executa a ferramenta.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                tools=self.tools,
                tool_choice="auto",
                max_tokens=4096
            )

            response_message = chat_completion.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                available_tools = {
                    func_name: getattr(self.db_tools, func_name) 
                    for func_name in dir(self.db_tools) 
                    if callable(getattr(self.db_tools, func_name)) and not func_name.startswith("_")
                }
                
                messages.append(response_message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    try:
                        print(f"🤖 Chamando função: {function_name} com argumentos: {tool_call.function.arguments}", file=sys.stderr)
                        
                        if function_name not in available_tools:
                            raise AttributeError(f"A função '{function_name}' não foi encontrada.")

                        function_to_call = available_tools[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        function_response = function_to_call(**function_args)
                        
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps(function_response),
                            }
                        )
                    except (AttributeError, json.JSONDecodeError, Exception) as e:
                        print(f"🐞 Erro ao executar a ferramenta: {e}", file=sys.stderr)
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps({"error": str(e)})
                        })
                
                second_response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages
                )
                return second_response.choices[0].message.content
            else:
                return response_message.content

        except Exception as e:
            print(f"🐞 Erro na chamada da API Groq: {e}", file=sys.stderr)
            return f"🐞 Ocorreu um erro ao comunicar com a IA: {e}"

def main():
    try:
        if len(sys.argv) < 2:
            print("Erro: Pergunta não fornecida.", file=sys.stderr)
            sys.exit(1)

        question = sys.argv[1]
        agent = AIAgent()
        response = agent.process_message(question)
        print(response)

    except Exception as e:
        print(f"Erro inesperado em ai_agent.py: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()