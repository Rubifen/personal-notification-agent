import time
import threading
import schedule
import datetime
import json
from core.gestor_tareas import GestorTareas
from core.agente_llm import AgenteLLM
from core.notificador import Notificador
from tools.clima_api import obtener_clima
from tools.web_scraper import obtener_dato_web

class BucleEjecucion:
    def __init__(self, callback_actualizacion=None):
        self.gestor = GestorTareas()
        self.agente = AgenteLLM()
        self.notificador = Notificador()
        self.hilo = None
        self.corriendo = False
        self.callback_actualizacion = callback_actualizacion

    def _evaluar_condicion(self, json_intencion, resultado_herramienta, fecha_creacion):
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
        Contexto importante: Esta tarea fue pedida originalmente por el usuario en la siguiente fecha y hora: {fecha_creacion}
        
        ¿Se cumple la condición basándonos estrictamente en el resultado actual y el contexto de cuándo se pidió? 
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
        # Refrescar credenciales en caliente por si se cambiaron en los ajustes
        self.agente.recargar_credenciales()
        self.notificador.recargar_credenciales()

        print("Bucle Principal: Revisando tareas activas...")
        activas = self.gestor.obtener_tareas('activa')
        hubo_cambios = False
        ahora = datetime.datetime.now()
        
        for tarea in activas:
            ultima_ejecucion_str = tarea.get('ultima_ejecucion')
            frecuencia = tarea.get('frecuencia_minutos', 1)
            
            # Filtro de frecuencia
            if ultima_ejecucion_str:
                ultima_ejecucion = datetime.datetime.fromisoformat(ultima_ejecucion_str)
                minutos_pasados = (ahora - ultima_ejecucion).total_seconds() / 60
                if minutos_pasados < frecuencia:
                    # Aún no toca revisar esta tarea
                    continue

            orden = tarea['orden']
            print(f"Procesando Tarea #{tarea['id']}: {orden} (Frecuencia: {frecuencia} min)")
            
            # 1. Leer intención extraída previamente
            intencion_str = tarea.get('intencion_json')
            if not intencion_str:
                print("No se encontró intención JSON en la base de datos.")
                continue
                
            try:
                intencion = json.loads(intencion_str)
            except:
                print("Error parseando intención JSON")
                continue
                
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
                ahora_str = ahora.strftime("%Y-%m-%d %H:%M:%S")
                resultado = f"Información de sistema: La fecha y hora actual del equipo es {ahora_str}."

            if resultado is None:
                continue
            
            # 3. Evaluar Condición con contexto temporal relativo
            se_cumple = self._evaluar_condicion(intencion, resultado, tarea['fecha_creacion'])
            
            # 4. Actualizar última ejecución
            self.gestor.actualizar_ultima_ejecucion(tarea['id'])
            
            if se_cumple:
                print(f"¡Condición cumplida para Tarea #{tarea['id']}!")
                # Notificar
                mensaje = f"¡Aviso del Agente!\nOrden: '{orden}'\nDato actual: {resultado}"
                canal = tarea['canal'].lower()
                
                if 'escritorio' in canal:
                    self.notificador.notificar_escritorio(mensaje)
                elif 'email' in canal:
                    self.notificador.notificar_email(mensaje)
                elif 'telegram' in canal:
                    self.notificador.notificar_telegram(mensaje)
                elif 'whatsapp' in canal:
                    self.notificador.notificar_whatsapp(mensaje)

                # Cambiar estado si no es recurrente
                if not tarea['recurrencia']:
                    self.gestor.actualizar_estado(tarea['id'], 'finalizada')
                    print(f"Tarea #{tarea['id']} marcada como finalizada.")
                    hubo_cambios = True

        if hubo_cambios and self.callback_actualizacion:
            self.callback_actualizacion()

    def iniciar(self):
        self.corriendo = True
        # Programar ejecución cada 1 minuto
        schedule.every(1).minutes.do(self.procesar_tareas)
        
        self.hilo = threading.Thread(target=self._run_loop, daemon=True)
        self.hilo.start()
        print("Bucle principal iniciado en segundo plano (cada 1 minuto).")

    def _run_loop(self):
        while self.corriendo:
            schedule.run_pending()
            time.sleep(1)
