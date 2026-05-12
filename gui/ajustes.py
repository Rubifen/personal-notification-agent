import customtkinter as ctk
import os
import dotenv

class VentanaAjustes(ctk.CTkToplevel):
    def __init__(self, master, on_save_callback=None):
        super().__init__(master)
        
        self.title("Ajustes de Integración")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Mantener la ventana siempre encima de la principal
        self.transient(master)
        self.grab_set()

        self.on_save_callback = on_save_callback
        self.env_path = os.path.join(os.getcwd(), ".env")

        self._crear_ui()
        self._cargar_datos()

    def _crear_ui(self):
        # Frame principal con scroll
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)

        # Sección OpenRouter
        self._crear_seccion("🧠 Inteligencia Artificial (OpenRouter)")
        self.entry_openrouter = self._crear_campo("API Key de OpenRouter:", show="*")

        # Sección Email
        self._crear_seccion("📧 Correo Electrónico (Gmail)")
        self.entry_email_user = self._crear_campo("Dirección de Email:")
        self.entry_email_pass = self._crear_campo("Contraseña de Aplicación:", show="*")

        # Sección Telegram
        self._crear_seccion("✈️ Telegram")
        self.entry_telegram_token = self._crear_campo("Token del Bot:", show="*")
        self.entry_telegram_chat = self._crear_campo("Chat ID:")

        # Sección WhatsApp (CallMeBot)
        self._crear_seccion("📱 WhatsApp (CallMeBot)")
        self.entry_wa_phone = self._crear_campo("Teléfono (ej. +34123456789):")
        self.entry_wa_api = self._crear_campo("API Key de CallMeBot:", show="*")

        # Botón Guardar
        self.btn_guardar = ctk.CTkButton(
            self, 
            text="Guardar Cambios", 
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(weight="bold"),
            command=self._guardar_datos
        )
        self.btn_guardar.pack(pady=10)

    def _crear_seccion(self, titulo):
        lbl = ctk.CTkLabel(self.scroll, text=titulo, font=ctk.CTkFont(size=16, weight="bold"))
        lbl.pack(anchor="w", pady=(20, 5))

    def _crear_campo(self, texto, show=""):
        lbl = ctk.CTkLabel(self.scroll, text=texto)
        lbl.pack(anchor="w")
        entry = ctk.CTkEntry(self.scroll, width=400, show=show)
        entry.pack(anchor="w", pady=(0, 10))
        return entry

    def _cargar_datos(self):
        # Cargamos explícitamente el archivo .env actual
        valores = dotenv.dotenv_values(self.env_path)
        
        if "OPENROUTER_API_KEY" in valores:
            self.entry_openrouter.insert(0, valores["OPENROUTER_API_KEY"] or "")
        if "EMAIL_USER" in valores:
            self.entry_email_user.insert(0, valores["EMAIL_USER"] or "")
        if "EMAIL_PASS" in valores:
            self.entry_email_pass.insert(0, valores["EMAIL_PASS"] or "")
        if "TELEGRAM_TOKEN" in valores:
            self.entry_telegram_token.insert(0, valores["TELEGRAM_TOKEN"] or "")
        if "TELEGRAM_CHAT_ID" in valores:
            self.entry_telegram_chat.insert(0, valores["TELEGRAM_CHAT_ID"] or "")
        if "WHATSAPP_PHONE" in valores:
            self.entry_wa_phone.insert(0, valores["WHATSAPP_PHONE"] or "")
        if "WHATSAPP_API_KEY" in valores:
            self.entry_wa_api.insert(0, valores["WHATSAPP_API_KEY"] or "")

    def _guardar_datos(self):
        # Crear archivo .env si no existe
        if not os.path.exists(self.env_path):
            open(self.env_path, "w").close()

        # Guardar cada clave en el archivo .env sin borrar las demás
        dotenv.set_key(self.env_path, "OPENROUTER_API_KEY", self.entry_openrouter.get().strip())
        dotenv.set_key(self.env_path, "EMAIL_USER", self.entry_email_user.get().strip())
        dotenv.set_key(self.env_path, "EMAIL_PASS", self.entry_email_pass.get().strip())
        dotenv.set_key(self.env_path, "TELEGRAM_TOKEN", self.entry_telegram_token.get().strip())
        dotenv.set_key(self.env_path, "TELEGRAM_CHAT_ID", self.entry_telegram_chat.get().strip())
        dotenv.set_key(self.env_path, "WHATSAPP_PHONE", self.entry_wa_phone.get().strip())
        dotenv.set_key(self.env_path, "WHATSAPP_API_KEY", self.entry_wa_api.get().strip())

        # Ejecutar callback para recargar en la app principal
        if self.on_save_callback:
            self.on_save_callback()

        self.destroy()
