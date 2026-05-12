import os
import json
from openai import OpenAI
from dotenv import load_dotenv

class AgenteLLM:
    def __init__(self):
        self.recargar_credenciales()

    def recargar_credenciales(self):
        load_dotenv(override=True)
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if self.api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
            self.modelo = "google/gemini-2.5-pro"
        else:
            self.client = None

    def extraer_intencion(self, orden):
        if not self.client:
            print("No hay API Key de OpenRouter configurada.")
            return None

        prompt_sistema = """
        Eres un asistente de automatización. El usuario te dará una orden.
        Debes extraer la intención y devolver un JSON estricto con el siguiente formato, sin ningún otro texto:
        {
            "herramienta": "clima|scraper|ninguna",
            "parametros": {"ciudad": "Nombre", "url": "URL", "selector": "CSS"},
            "condicion": "Texto libre resumiendo qué debe cumplirse para notificar (ej. 'llueve', 'temperatura > 20')",
            "frecuencia_minutos": 1
        }
        
        Reglas para frecuencia_minutos:
        - Si es un aviso de tiempo relativo corto (ej. "en 15 minutos", "a las 5"), usa 1.
        - Si es clima, usa 30 o 60 (no tiene sentido comprobar cada minuto).
        - Si es precio de tienda web o scraper general, usa 60 o 120 para no saturarla.
        
        Ejemplos:
        Orden: "Avisame si llueve en Madrid"
        {"herramienta": "clima", "parametros": {"ciudad": "Madrid"}, "condicion": "llueve", "frecuencia_minutos": 60}
        
        Orden: "Avisame en 15 minutos"
        {"herramienta": "ninguna", "parametros": {}, "condicion": "han pasado 15 minutos", "frecuencia_minutos": 1}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": orden}
                ],
                response_format={"type": "json_object"}
            )
            
            contenido = response.choices[0].message.content
            return json.loads(contenido)
            
        except Exception as e:
            print(f"Error al conectar con LLM: {e}")
            return None
