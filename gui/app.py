import customtkinter as ctk
import threading
import json
from tkinter import messagebox
from core.gestor_tareas import GestorTareas
from core.voz import escuchar_y_transcribir
from core.agente_llm import AgenteLLM
from gui.ajustes import VentanaAjustes
from core.agente_llm import AgenteLLM

class NotificationAgentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Inicializar base de datos y agente
        self.gestor = GestorTareas()
        self.agente = AgenteLLM()

        # Configuración básica de la ventana
        self.title("Panel de Control Agéntico")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Dark Mode por defecto
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")

        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=7)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)

        self._create_header()
        self._create_task_viewer()
        self._create_controls()

        # Cargar tareas reales al iniciar
        self.cargar_tareas()

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="nsew")
        header_frame.grid_rowconfigure(0, weight=1)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Panel de Control Agéntico", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0)

        btn_ajustes = ctk.CTkButton(
            header_frame,
            text="⚙️",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#333333",
            font=ctk.CTkFont(size=24),
            command=self.abrir_ajustes
        )
        btn_ajustes.grid(row=0, column=1, padx=20)

    def _create_task_viewer(self):
        viewer_frame = ctk.CTkFrame(self, fg_color="transparent")
        viewer_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        viewer_frame.grid_rowconfigure(0, weight=1)
        viewer_frame.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(viewer_frame)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        
        tab_activas = self.tabview.add("Activas")
        tab_finalizadas = self.tabview.add("Finalizadas")

        self.scroll_activas = ctk.CTkScrollableFrame(tab_activas, fg_color="transparent")
        self.scroll_activas.pack(expand=True, fill="both")

        self.scroll_finalizadas = ctk.CTkScrollableFrame(tab_finalizadas, fg_color="transparent")
        self.scroll_finalizadas.pack(expand=True, fill="both")

    def cargar_tareas(self):
        # Limpiar frames actuales
        for widget in self.scroll_activas.winfo_children():
            widget.destroy()
        for widget in self.scroll_finalizadas.winfo_children():
            widget.destroy()

        # Obtener tareas desde BD
        activas = self.gestor.obtener_tareas('activa')
        finalizadas = self.gestor.obtener_tareas('finalizada')

        self._renderizar_lista(activas, self.scroll_activas)
        self._renderizar_lista(finalizadas, self.scroll_finalizadas)

    def _renderizar_lista(self, tareas, parent_frame):
        for tarea in tareas:
            card = ctk.CTkFrame(parent_frame, corner_radius=20, fg_color="#2b2b2b")
            card.pack(fill="x", padx=10, pady=15)
            
            # Header de la tarjeta
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=(20, 5))
            
            title = ctk.CTkLabel(
                header, 
                text=f"Orden #{tarea['id']} - [{tarea['canal']}]", 
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title.pack(side="left")
            
            # Botón de eliminar alineado a la derecha (aparecerá a la derecha del checkbox)
            btn_eliminar = ctk.CTkButton(
                header,
                text="🗑️",
                width=30,
                height=24,
                corner_radius=4,
                fg_color="#8d1f1f",
                hover_color="#5e1414",
                command=lambda t_id=tarea['id']: self._eliminar_tarea(t_id)
            )
            btn_eliminar.pack(side="right", padx=(10, 0))

            # Checkbox de recurrencia alineado a la derecha
            var_recurrencia = ctk.BooleanVar(value=tarea['recurrencia'])
            chk_recurrencia = ctk.CTkCheckBox(
                header, 
                text="Recurrente",
                variable=var_recurrencia,
                command=lambda t_id=tarea['id'], var=var_recurrencia: self._toggle_recurrencia(t_id, var)
            )
            chk_recurrencia.pack(side="right")
            
            desc = ctk.CTkLabel(
                card, 
                text=tarea['orden'], 
                text_color="#aaaaaa",
                wraplength=600,
                justify="left"
            )
            desc.pack(anchor="w", padx=20, pady=(0, 20))

    def _toggle_recurrencia(self, tarea_id, var):
        self.gestor.actualizar_recurrencia(tarea_id, var.get())

    def _eliminar_tarea(self, tarea_id):
        confirmar = messagebox.askyesno("Eliminar Tarea", f"¿Estás seguro de que quieres eliminar la tarea #{tarea_id}?")
        if confirmar:
            self.gestor.eliminar_tarea(tarea_id)
            self.cargar_tareas()

    def _create_controls(self):
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        controls_frame.grid_columnconfigure(0, weight=0)
        controls_frame.grid_columnconfigure(1, weight=0)
        controls_frame.grid_columnconfigure(2, weight=1)
        controls_frame.grid_columnconfigure(3, weight=0)
        controls_frame.grid_rowconfigure(0, weight=1)

        self.combo_canal = ctk.CTkComboBox(
            controls_frame, 
            values=["Telegram", "WhatsApp", "Email", "Escritorio"],
            width=110,
            height=40
        )
        self.combo_canal.grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.combo_canal.set("Telegram")

        self.entry_freq = ctk.CTkEntry(
            controls_frame,
            placeholder_text="Frecuencia min",
            width=110,
            height=40
        )
        self.entry_freq.grid(row=0, column=1, padx=(0, 10), sticky="w")

        self.entry_orden = ctk.CTkEntry(
            controls_frame, 
            placeholder_text="Escribe tu orden aquí...",
            height=40
        )
        self.entry_orden.grid(row=0, column=2, padx=5, sticky="ew")
        self.entry_orden.bind("<Return>", lambda event: self.enviar_orden()) # Permitir pulsar Enter

        buttons_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=3, padx=(15, 0), sticky="e")
        
        self.btn_mic = ctk.CTkButton(
            buttons_frame, 
            text="🎤", 
            width=40, 
            height=40, 
            corner_radius=8,
            fg_color="#444444",
            hover_color="#555555",
            font=ctk.CTkFont(size=18),
            command=self.iniciar_grabacion
        )
        self.btn_mic.pack(side="left", padx=(0, 10))

        btn_send = ctk.CTkButton(
            buttons_frame, 
            text="Enviar", 
            width=100, 
            height=40, 
            corner_radius=8,
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(weight="bold"),
            command=self.enviar_orden
        )
        btn_send.pack(side="left")

    def iniciar_grabacion(self):
        # Cambiar apariencia a grabando
        self.btn_mic.configure(fg_color="red", hover_color="darkred", state="disabled")
        self.entry_orden.delete(0, 'end')
        self.entry_orden.configure(placeholder_text="Escuchando (5s)...")
        
        # Iniciar hilo para no congelar la GUI
        threading.Thread(target=self._hilo_escucha, daemon=True).start()

    def _hilo_escucha(self):
        escuchar_y_transcribir(self._on_listen_success, self._on_listen_error)

    def _on_listen_success(self, texto):
        # Usamos .after para volver al hilo principal de forma segura
        self.after(0, self._actualizar_ui_voz, texto, False)

    def _on_listen_error(self, error):
        self.after(0, self._actualizar_ui_voz, error, True)

    def _actualizar_ui_voz(self, texto, es_error):
        # Restaurar botón
        self.btn_mic.configure(fg_color="#444444", hover_color="#555555", state="normal")
        self.entry_orden.configure(placeholder_text="Escribe tu orden aquí...")
        
        if not es_error:
            self.entry_orden.delete(0, 'end')
            self.entry_orden.insert(0, texto)
        else:
            # Mostrar error temporalmente en el entry
            self.entry_orden.delete(0, 'end')
            self.entry_orden.configure(placeholder_text=f"Error: {texto}")

    def enviar_orden(self):
        orden = self.entry_orden.get().strip()
        canal = self.combo_canal.get()
        frec_texto = self.entry_freq.get().strip()
        
        if orden:
            self.entry_orden.delete(0, 'end')
            self.entry_orden.configure(placeholder_text="Procesando con la IA...")
            
            frecuencia_usuario = None
            if frec_texto.isdigit():
                frecuencia_usuario = int(frec_texto)
                
            threading.Thread(target=self._hilo_procesar_orden, args=(orden, canal, frecuencia_usuario), daemon=True).start()

    def _hilo_procesar_orden(self, orden, canal, frecuencia_usuario):
        intencion = self.agente.extraer_intencion(orden)
        
        if intencion:
            if frecuencia_usuario is not None:
                intencion['frecuencia_minutos'] = frecuencia_usuario
            frec_final = intencion.get('frecuencia_minutos', 1)
            
            # Guardamos la orden
            self.gestor.agregar_tarea(orden, canal, json.dumps(intencion), frec_final, recurrencia=False)
            
        # Volvemos al hilo principal para actualizar GUI
        self.after(0, self._on_orden_procesada)

    def _on_orden_procesada(self):
        self.entry_orden.configure(placeholder_text="Escribe tu orden aquí...")
        self.entry_freq.delete(0, 'end')
        self.cargar_tareas()
        self.tabview.set("Activas")

    def abrir_ajustes(self):
        VentanaAjustes(self, on_save_callback=self.recargar_credenciales_app)

    def recargar_credenciales_app(self):
        self.agente.recargar_credenciales()

def run_app():
    app = NotificationAgentGUI()
    app.mainloop()
