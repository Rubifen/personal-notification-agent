from gui.app import run_app
from core.bucle_principal import BucleEjecucion

def main():
    # Iniciar el bucle de ejecución en segundo plano
    bucle = BucleEjecucion()
    bucle.iniciar()
    
    run_app()

if __name__ == "__main__":
    main()
