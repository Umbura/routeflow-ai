import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from src.services import GeoService, RouteOptimizer
from src.models import RoutePlan

# Carrega variáveis de ambiente
load_dotenv()

class LogisticsAgent:
    """
    Agente responsável por orquestrar a interpretação de linguagem natural
    e a execução das ferramentas de logística.
    """
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("A chave GROQ_API_KEY não foi encontrada no arquivo .env")
        
        if not api_key.startswith("gsk_"):
            st.error(f"⚠️ A chave no arquivo .env parece inválida. Verifique se inicia com 'gsk_'.")
            
        # Configura o cliente OpenAI apontando para a infraestrutura da Groq
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Modelo Llama 3.3 Versatile (Otimizado para JSON e instruções complexas)
        self.model = "llama-3.3-70b-versatile"
        
        # Inicializa os serviços auxiliares (Tools)
        self.geo_service = GeoService()
        self.optimizer = RouteOptimizer()

    def _extract_addresses(self, text: str) -> list[str]:
        """
        Utiliza LLM para extrair endereços estruturados de texto livre.
        Retorna uma lista de strings com os endereços identificados.
        """
        system_prompt = """
        Você é um assistente especializado em logística e extração de dados (NER).
        Sua tarefa é analisar o texto do usuário e extrair todos os endereços físicos completos.
        
        REGRAS DE SAÍDA:
        1. Retorne APENAS um objeto JSON válido.
        2. O formato deve ser estritamente: {"addresses": ["Endereço 1", "Endereço 2"]}
        3. Se a cidade não for mencionada no endereço, assuma que é São Paulo, SP.
        4. Não adicione explicações ou texto fora do JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"},
                temperature=0
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            return data.get("addresses", [])
            
        except Exception as e:
            self._handle_api_error(e)
            return []

    def _handle_api_error(self, e: Exception):
        """Trata erros da API de forma amigável na interface."""
        error_msg = str(e)
        if "401" in error_msg:
            st.error("🚨 Erro de Autenticação (401): Verifique sua chave API no arquivo .env.")
        elif "404" in error_msg:
            st.error(f"🚨 Erro de Modelo (404): O modelo '{self.model}' não está disponível.")
        elif "429" in error_msg:
            st.error("🚨 Limite de Requisições (429): A API da Groq está sobrecarregada no momento.")
        else:
            st.error(f"🚨 Erro na API de IA: {error_msg}")

    def process_request(self, raw_text: str) -> RoutePlan:
        """
        Executa o pipeline completo:
        1. Extração de Texto (LLM)
        2. Geolocalização (Nominatim)
        3. Otimização de Rota (TSP Heuristic)
        """
        # 1. Extração
        address_strings = self._extract_addresses(raw_text)
        
        if not address_strings:
             return None 

        # 2. Geolocalização
        valid_locations = []
        for addr in address_strings:
            loc = self.geo_service.get_coordinates(addr)
            if loc:
                valid_locations.append(loc)
        
        if not valid_locations:
            st.warning("A IA identificou endereços, mas o serviço de mapas não encontrou coordenadas. Tente ser mais específico (ex: inclua a cidade).")
            # Retorna plano vazio para evitar crash
            return RoutePlan(raw_input=raw_text, stops=[], total_distance_km=0.0)

        # 3. Otimização
        optimized_path = self.optimizer.optimize_nearest_neighbor(valid_locations)
        total_dist = self.optimizer.calculate_total_distance(optimized_path)

        return RoutePlan(
            raw_input=raw_text,
            stops=optimized_path,
            total_distance_km=total_dist
        )