import customtkinter as ctk

class NotificationAgentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.title("Panel de Control Agéntico")
        self.geometry("800x600")
        self.resizable(False, False) # Tamaño fijo
        
        # Dark Mode por defecto
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")

        # Configurar grid de la ventana principal
        # Usamos pesos proporcionales para lograr 10% / 70% / 20%
        self.grid_rowconfigure(0, weight=1)  # Header (10%)
        self.grid_rowconfigure(1, weight=7)  # Visor de Tareas (70%)
        self.grid_rowconfigure(2, weight=2)  # Controles (20%)
        self.grid_columnconfigure(0, weight=1)

        self._create_header()
        self._create_task_viewer()
        self._create_controls()

    def _create_header(self):
        # Header (10% superior) con fondo gris muy oscuro
        header_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="nsew")
        
        # Centrar el texto en el header
        header_frame.grid_rowconfigure(0, weight=1)
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Panel de Control Agéntico", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0)

    def _create_task_viewer(self):
        # Visor de Tareas (70% central)
        viewer_frame = ctk.CTkFrame(self, fg_color="transparent")
        viewer_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        viewer_frame.grid_rowconfigure(0, weight=1)
        viewer_frame.grid_columnconfigure(0, weight=1)

        # Componente CTkTabview
        tabview = ctk.CTkTabview(viewer_frame)
        tabview.grid(row=0, column=0, sticky="nsew")
        
        tab_activas = tabview.add("Activas")
        tab_finalizadas = tabview.add("Finalizadas")

        # CTkScrollableFrame para Activas
        scroll_activas = ctk.CTkScrollableFrame(tab_activas, fg_color="transparent")
        scroll_activas.pack(expand=True, fill="both")
        self._add_fake_cards(scroll_activas)

        # CTkScrollableFrame para Finalizadas
        scroll_finalizadas = ctk.CTkScrollableFrame(tab_finalizadas, fg_color="transparent")
        scroll_finalizadas.pack(expand=True, fill="both")
        self._add_fake_cards(scroll_finalizadas)

    def _add_fake_cards(self, parent_frame):
        # Añadir 3 tarjetas falsas con esquinas muy redondeadas y margen
        for i in range(1, 4):
            card = ctk.CTkFrame(parent_frame, corner_radius=20, fg_color="#2b2b2b")
            card.pack(fill="x", padx=10, pady=15) # Bastante margen entre tarjetas
            
            title = ctk.CTkLabel(
                card, 
                text=f"Tarea de Ejemplo #{i}", 
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title.pack(anchor="w", padx=20, pady=(20, 5))
            
            desc = ctk.CTkLabel(
                card, 
                text="Descripción breve de la tarea simulada para ver el diseño estático.", 
                text_color="#aaaaaa"
            )
            desc.pack(anchor="w", padx=20, pady=(0, 20))

    def _create_controls(self):
        # Controles (20% inferior)
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Grid para distribuir izquierda, centro y derecha
        controls_frame.grid_columnconfigure(0, weight=0) # Izquierda
        controls_frame.grid_columnconfigure(1, weight=1) # Centro (Entry ancho)
        controls_frame.grid_columnconfigure(2, weight=0) # Derecha
        controls_frame.grid_rowconfigure(0, weight=1)

        # Izquierda: CTkComboBox
        combo = ctk.CTkComboBox(
            controls_frame, 
            values=["Telegram", "Email", "Escritorio"],
            width=140,
            height=40
        )
        combo.grid(row=0, column=0, padx=(0, 15), sticky="w")
        combo.set("Telegram") # Valor por defecto

        # Centro: CTkEntry ancho
        entry = ctk.CTkEntry(
            controls_frame, 
            placeholder_text="Escribe tu orden aquí...",
            height=40
        )
        entry.grid(row=0, column=1, padx=5, sticky="ew")

        # Derecha: Botón Cuadrado (Micrófono) y Botón Azul (Enviar)
        buttons_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, padx=(15, 0), sticky="e")
        
        # Botón Micrófono
        btn_mic = ctk.CTkButton(
            buttons_frame, 
            text="🎤", 
            width=40, 
            height=40, 
            corner_radius=8,
            fg_color="#444444",
            hover_color="#555555",
            font=ctk.CTkFont(size=18)
        )
        btn_mic.pack(side="left", padx=(0, 10))

        # Botón Enviar (Azul)
        btn_send = ctk.CTkButton(
            buttons_frame, 
            text="Enviar", 
            width=100, 
            height=40, 
            corner_radius=8,
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(weight="bold")
        )
        btn_send.pack(side="left")

def run_app():
    app = NotificationAgentGUI()
    app.mainloop()
