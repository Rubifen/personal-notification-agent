from gui.app import NotificationAgentGUI
from core.bucle_principal import BucleEjecucion

def main():
    app = NotificationAgentGUI()
    
    def refrescar_gui():
        app.after(0, app.cargar_tareas)
        
    # Iniciar el bucle de ejecución en segundo plano
    bucle = BucleEjecucion(callback_actualizacion=refrescar_gui)
    bucle.iniciar()
    
    app.mainloop()

if __name__ == "__main__":
    main()
