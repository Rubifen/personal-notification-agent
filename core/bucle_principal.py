import time
import threading
import schedule
from core.gestor_tareas import GestorTareas
from core.agente_llm import AgenteLLM
from core.notificador import Notificador
from tools.clima_api import obtener_clima
from tools.web_scraper import obtener_dato_web

class BucleEjecucion:
    def __init__(self):
        self.gestor = GestorTareas()
        self.agente = AgenteLLM()
        self.notificador = Notificador()
        self.hilo = None
        self.corriendo = False

    def _evaluar_condicion(self, json_intencion, resultado_herramienta):
        """
        Usa el LLM para evaluar si se cumple la condición dada la salida de la herramienta.
        Devuelve True o False.
        """
        condicion = json_intencion.get("condicion")
        if not condicion or condicion.lower() in ['ninguna', '']:
            return True
            
        prompt = f"""
        El usuario estableció la siguiente condición para notificarle: "{condicion}"
        La herramienta ha devuelto el siguiente resultado actual: "{resultado_herramienta}"
        
        ¿Se cumple la condición basándonos estrictamente en el resultado actual? 
        Responde solo con la palabra "SI" o "NO".
        """
        
        try:
            if not self.agente.client:
                return False
                
            response = self.agente.client.chat.completions.create(
                model=self.agente.modelo,
                messages=[{"role": "user", "content": prompt}]
            )
            respuesta = response.choices[0].message.content.strip().upper()
            return "SI" in respuesta
        except Exception as e:
            print(f"Error evaluando condición: {e}")
            return False

    def procesar_tareas(self):
        print("Bucle Principal: Revisando tareas activas...")
        activas = self.gestor.obtener_tareas('activa')
        
        for tarea in activas:
            orden = tarea['orden']
            print(f"Procesando Tarea #{tarea['id']}: {orden}")
            
            # 1. Extraer intención
            intencion = self.agente.extraer_intencion(orden)
            if not intencion:
                continue
                
            print(f"Intención extraída: {intencion}")
            herramienta = intencion.get('herramienta', 'ninguna').lower()
            parametros = intencion.get('parametros', {})
            
            # 2. Ejecutar herramienta
            resultado = None
            if herramienta == 'clima':
                ciudad = parametros.get('ciudad')
                if ciudad:
                    resultado = obtener_clima(ciudad)
            elif herramienta == 'scraper':
                url = parametros.get('url')
                selector = parametros.get('selector')
                if url and selector:
                    resultado = obtener_dato_web(url, selector)
            else:
                resultado = "Condición de tiempo u otro tipo de tarea general."

            if resultado is None:
                continue
            
            print(f"Resultado herramienta: {resultado}")

            # 3. Evaluar Condición
            se_cumple = self._evaluar_condicion(intencion, resultado)
            
            if se_cumple:
                print(f"¡Condición cumplida para Tarea #{tarea['id']}!")
                # 4. Notificar
                mensaje = f"¡Aviso del Agente!\nOrden: '{orden}'\nDato actual: {resultado}"
                canal = tarea['canal'].lower()
                
                if 'escritorio' in canal:
                    self.notificador.notificar_escritorio(mensaje)
                elif 'email' in canal:
                    self.notificador.notificar_email(mensaje)
                elif 'telegram' in canal:
                    self.notificador.notificar_telegram(mensaje)

                # 5. Cambiar estado
                if not tarea['recurrencia']:
                    self.gestor.actualizar_estado(tarea['id'], 'finalizada')
                    print(f"Tarea #{tarea['id']} marcada como finalizada.")

    def iniciar(self):
        self.corriendo = True
        # Programar ejecución cada 1 minuto
        schedule.every(1).minutes.do(self.procesar_tareas)
        
        self.hilo = threading.Thread(target=self._run_loop, daemon=True)
        self.hilo.start()
        print("Bucle principal iniciado en segundo plano (cada 1 minuto).")

    def _run_loop(self):
        # Ejecutar inmediatamente la primera vez (opcional, pero útil para testing)
        # self.procesar_tareas() 
        while self.corriendo:
            schedule.run_pending()
            time.sleep(1)
