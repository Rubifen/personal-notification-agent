Informe del Projecte: Personal Notification Agent

Descripción del proyecto:
El proyecto consiste en un agente de notificaciones personales inteligente desarrollado en Python que se ejecuta en segundo plano. Resuelve el problema del seguimiento manual de datos (como el tiempo, el contenido de una página web, etc…) al permitir a los usuarios configurar alertas utilizando lenguaje natural, ya sea escrito o hablado. Su principal ventaja es su capacidad para comprender la intención y automatizar la comprobación y la notificación a través de canales como el escritorio, Telegram, el correo electrónico y WhatsApp.

URL del repositorio:
https://github.com/Rubifen/personal-notification-agent/

Uso de la IA:
Los modelos LLM se utilizan a través de la API de OpenRouter , integrados gracias a la biblioteca oficial de OpenAI. El objetivo principal es la comprensión del lenguaje natural y el razonamiento: el usuario introduce un comando de formato libre (por ejemplo, “Avísame si llueve en Manacor dentro de una hora”) y la IA se encarga de analizar el texto, extraer los parámetros, seleccionar qué herramienta debe utilizar y determinar con qué frecuencia debe comprobarlo. También se utiliza «Speech to Text» con SpeechRecognition para el dictado por voz.

Flujos de trabajo:
1. Crear un plan con todos los detalles sobre el programa.
2. Con ese plan creamos un prompt completo dividido por fases y tareas atómicas para que la IA las vaya haciendo.
3. Cada vez que termina una tarea automáticamente la sube al repositorio.
4. Al final una vez ha terminado se prueba la aplicación y se hace debug y añaden características.

Explicación del código:
La arquitectura se divide en módulos especializados:
core/: Contiene el núcleo de la aplicación. El Agent, que se comunica con la IA, el Task Manager, que interactúa con SQLite para guardar tareas, y el Background Scheduler, que se ejecuta en un hilo en segundo plano y evalúa cada x tiempo si se ha cumplido una condición.
gui/: Interfaz de usuario desarrollada con CustomTkinter, dividida en las partes visual y de configuración. Utiliza métodos de llamada entre subprocesos seguros para evitar que la aplicación se cuelgue.
tools/: Archivos y scripts que proporcionan capacidades al agente, como clima_api para el tiempo.
main.py: El punto de entrada de la aplicación que conecta la interfaz con el motor.

Tecnologías utilizadas:
- Agente: Antigravity de Google.
- Lenguaje principal: Python 3.
- Interfaz gráfica: customtkinter.
- Herramientas de IA y datos: API de OpenRouter, SpeechRecognition, sounddevice, numpy y soundfile para el audio.
- Redes y análisis sintáctico: requests, beautifulsoup4 (scraping).
- Notificaciones: plyer para notificaciones nativas, protocolos de correo electrónico y solicitudes HTTP para Telegram o WhatsApp (CallMeBot).
- Otros: python-dotenv (variables de entorno), base de datos local SQLite3
.
Retos y lecciones aprendidas:
- Tiempo relativo: un reto fue conseguir que la IA entendiera «dentro de una hora». Esto se resolvió inyectando siempre el contexto de la hora local del ordenador como un mensaje del sistema oculto.
- Hilos y interfaz de usuario: Actualizar una interfaz CustomTkinter desde un hilo secundario (como el programador o la grabadora de audio) provocaba el bloqueo de la aplicación. La solución fue utilizar mecanismos específicos o devoluciones de llamada dentro del bucle principal de la interfaz gráfica de usuario.
- Configuración y base de datos: Modificar las tablas para añadir nuevas funcionalidades requirió adaptar cuidadosamente el código SQL para evitar conflictos

Limitaciones y mejoras futuras:
- Limitaciones: El rastreador web actual depende en gran medida del uso de selectores CSS exactos que debe definir el usuario. No tiene capacidad nativa para sortear captchas ni para navegar como un navegador completo.
- Mejoras futuras: Añadir la capacidad de realizar acciones reales (escritura, modificación) y no solo lectura y notificación. Desarrollar subagentes más interactivos, un bot de respuesta automática.
Reflexión sobre el uso de la IA:
Ha ido muy bien para la planificación del programa en base a una idea genérica para hacerla más específica. También con Antigravity prácticamente el proceso es automatizado gran parte del proceso, aunque hay que ser muy específicos para asegurarse de que no interpreta a su antojo cada cosa.

Instrucciones de instalación y uso:
1. Clona este repositorio en tu equipo.
2. Abre un terminal y ve a la carpeta raíz.
3. Instala los requisitos ejecutando: pip install -r requirements.txt.
4. Copia el archivo .env.example o cámbiale el nombre a .env.
5. Edita el archivo .env e incluye tus claves API: la de OpenRouter (obligatoria) y las claves del canal de notificaciones (bot de Telegram, credenciales de correo electrónico o la API de CallMeBot para WhatsApp).
6. Ejecuta la aplicación con el comando: python main.py.
7. Haz clic en el botón del micrófono y dicta tu primera regla, o escríbela en el cuadro de texto de abajo y pulsa «Añadir tarea».


