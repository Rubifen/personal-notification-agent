import requests
from bs4 import BeautifulSoup

def obtener_dato_web(url, selector):
    """
    Descarga la URL, parsea con BeautifulSoup y devuelve el texto del primer elemento que coincida con el selector CSS.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, 'html.parser')
        elemento = soup.select_one(selector)
        
        if elemento:
            return elemento.get_text(strip=True)
        else:
            return f"No se encontró ningún elemento con el selector: {selector}"
            
    except Exception as e:
        return f"Error al hacer scraping: {e}"
