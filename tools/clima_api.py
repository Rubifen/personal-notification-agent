import requests

def obtener_clima(ciudad):
    """
    Obtiene el clima de una ciudad usando Open-Meteo.
    """
    try:
        # 1. Geocodificación
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1&language=es&format=json"
        geo_res = requests.get(geo_url)
        geo_res.raise_for_status()
        geo_data = geo_res.json()
        
        if not geo_data.get("results"):
            return f"No se encontró la ciudad: {ciudad}"
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        
        # 2. Clima actual
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(weather_url)
        w_res.raise_for_status()
        w_data = w_res.json()
        
        current = w_data["current_weather"]
        temp = current["temperature"]
        code = current["weathercode"]
        
        estado = "Despejado"
        if code in [1, 2, 3]: estado = "Nublado"
        elif code in [45, 48]: estado = "Niebla"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: estado = "Lluvia"
        elif code in [71, 73, 75, 85, 86]: estado = "Nieve"
        elif code in [95, 96, 99]: estado = "Tormenta"

        return f"Temperatura: {temp}°C, Estado: {estado}"
        
    except Exception as e:
        return f"Error obteniendo clima: {e}"
