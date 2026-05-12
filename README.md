# Panel de Control Agéntico (Personal Notification Agent)

Un agente de notificaciones personal inteligente desarrollado en Python. Este proyecto actúa como un asistente automatizado en segundo plano capaz de entender órdenes en lenguaje natural (tanto escritas como dictadas por voz), interactuar con herramientas externas (APIs y Scraping) y notificarte cuando se cumplan las condiciones establecidas.

## Características Principales

- **Interfaz Gráfica (GUI)**: Panel oscuro moderno construido con `CustomTkinter` para gestionar tareas activas y finalizadas.
- **Dictado por Voz**: Integración de `SpeechRecognition` para introducir órdenes rápidamente usando el micrófono.
- **Inteligencia LLM**: Utiliza la API de OpenRouter (modelo Gemini-2.5-Pro u otros) para extraer intenciones estructuradas a partir de órdenes de texto libre (ej. *"Avísame en 15 minutos"* o *"Avisa si llueve en Madrid"*).
- **Herramientas (Tools)**:
  - `clima_api`: Lee la temperatura y estado actual de cualquier ciudad del mundo.
  - `web_scraper`: Extrae texto de cualquier página web usando selectores CSS.
- **Bucle de Ejecución en Segundo Plano (Background Scheduler)**: Un hilo silencioso que revisa periódicamente las tareas activas sin congelar la ventana.
- **Comprobaciones Dinámicas**: El agente deduce automáticamente la frecuencia óptima (cada 1, 30 o 60 min) con la que debe comprobar una tarea para ser eficiente, o puedes forzarla manualmente.
- **Múltiples Canales**: Notificaciones por Escritorio (Nativas de Windows), Correo Electrónico y Telegram.
- **Persistencia**: Base de datos SQLite local para guardar todo el estado.

## Estructura del Proyecto

- `core/`: Contiene la lógica central (Gestor de Tareas, Agente LLM, Notificador, Bucle Principal, Dictado por Voz).
- `gui/`: Contiene los elementos de la interfaz de usuario (`app.py`).
- `tools/`: Contiene los módulos de herramientas conectables (scrapers y APIs).

## Instalación y Uso

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuración de Variables de Entorno**:
   - Renombra o copia el archivo `.env.example` a `.env`.
   - Rellena el archivo con tus claves reales (OpenRouter, Email, Telegram).

3. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

## Historial de Desarrollo y Parches

El desarrollo de este proyecto se ha llevado de forma ágil con implementaciones iterativas:

- `chore: setup inicial y estructura de carpetas`
- `feat: implementacion de la interfaz grafica con CustomTkinter y persistencia` (GUI básica y SQLite).
- `feat: integración de dictado por voz asíncrono con hilos` (Botón 🎤 funcional sin congelar UI).
- `feat: implementacion de la inteligencia LLM y bucle de ejecucion principal` (Agente OpenRouter y Scheduler).
- `fix: añadir contexto de fecha y hora para evaluaciones de tiempo` (Inyección de `datetime` en el prompt para tareas de tiempo relativo).
- `patch: añadir boton para eliminar tareas con confirmacion` (Mejora UX/UI en las tarjetas de tareas).
- `patch: refresco automatico de la gui cuando finalizan tareas` (Callbacks entre el hilo de fondo y CustomTkinter).
- `feat: implementar comprobaciones dinamicas con frecuencia variable y tiempo relativo` (Actualización de Base de Datos para soportar frecuencias por tarea y evaluación de tiempos relativos correctos).
- `fix: aplicar realmente la actualizacion del esquema de la base de datos` (Resolución de conflictos de parámetros en SQL).
- `feat: panel de ajustes visual e integracion con whatsapp via callmebot` (Nueva ventana GUI para credenciales y canal de WhatsApp).
