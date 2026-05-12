import os
import json
from openai import OpenAI
from dotenv import load_dotenv

class AgenteLLM:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        # Configuramos el cliente OpenAI para usar OpenRouter
        if self.api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
            # Modelo rápido y avanzado en OpenRouter
            self.modelo = "google/gemini-2.5-pro"
        else:
            self.client = None

    def extraer_intencion(self, orden):
        """
        Llama al LLM para extraer la herramienta, parámetros y condición de la orden.
        Devuelve un diccionario estructurado.
        """
        if not self.client:
            print("No hay API Key de OpenRouter configurada.")
            return None

        prompt_sistema = """
        Eres un asistente de automatización. El usuario te dará una orden.
        Debes extraer la intención y devolver un JSON estricto con el siguiente formato, sin ningún otro texto:
        {
            "herramienta": "clima|scraper|ninguna",
            "parametros": {"ciudad": "Nombre", "url": "URL", "selector": "CSS"},
            "condicion": "Texto libre resumiendo qué debe cumplirse para notificar (ej. 'llueve', 'temperatura > 20', 'precio < 10')"
        }
        
        Ejemplos:
        Orden: "Avisame si llueve en Madrid"
        {"herramienta": "clima", "parametros": {"ciudad": "Madrid"}, "condicion": "llueve"}
        
        Orden: "Mira el precio en https://ejemplo.com/producto en el h1.price y avisa si baja de 10"
        {"herramienta": "scraper", "parametros": {"url": "https://ejemplo.com/producto", "selector": "h1.price"}, "condicion": "baja de 10"}
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
