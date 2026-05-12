import os
import smtplib
from email.mime.text import MIMEText
import requests
from plyer import notification
from dotenv import load_dotenv

class Notificador:
    def __init__(self):
        self.recargar_credenciales()

    def recargar_credenciales(self):
        load_dotenv(override=True)
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASS")
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.whatsapp_phone = os.getenv("WHATSAPP_PHONE")
        self.whatsapp_api_key = os.getenv("WHATSAPP_API_KEY")

    def notificar_escritorio(self, mensaje):
        try:
            notification.notify(
                title="Agente de Notificaciones",
                message=mensaje,
                app_name="Personal Notification Agent",
                timeout=10
            )
        except Exception as e:
            print(f"Error al notificar por escritorio: {e}")

    def notificar_email(self, mensaje, destinatario=None):
        if not self.email_user or not self.email_pass:
            print("Credenciales de email no configuradas.")
            return

        if not destinatario:
            destinatario = self.email_user

        try:
            msg = MIMEText(mensaje)
            msg['Subject'] = 'Aviso de Agente Personal'
            msg['From'] = self.email_user
            msg['To'] = destinatario

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
        except Exception as e:
            print(f"Error al enviar email: {e}")

    def notificar_telegram(self, mensaje):
        if not self.telegram_token or not self.telegram_chat_id:
            print("Credenciales de Telegram no configuradas.")
            return

        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": mensaje
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"Error al enviar por Telegram: {e}")

    def notificar_whatsapp(self, mensaje):
        if not self.whatsapp_phone or not self.whatsapp_api_key:
            print("Credenciales de WhatsApp no configuradas.")
            return

        try:
            import urllib.parse
            texto_codificado = urllib.parse.quote(mensaje)
            url = f"https://api.callmebot.com/whatsapp.php?phone={self.whatsapp_phone}&text={texto_codificado}&apikey={self.whatsapp_api_key}"
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print(f"Error al enviar por WhatsApp: {e}")
