import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ------------------------------
# Configuración
# ------------------------------
BASE_URL = "https://www.idealista.com/venta-viviendas/madrid/"
NUM_PAGES = 5  # Ajusta según cuántos anuncios quieres (~20 por página)
HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/16.6 Safari/605.1.15",
    # Puedes añadir más User-Agents
]
PROXIES = []  # Opcional: ["http://user:pass@proxy:port", ...]

# ------------------------------
# Función para delay aleatorio
# ------------------------------
def espera_aleatoria(min_s=1, max_s=3):
    time.sleep(random.uniform(min_s, max_s))

# ------------------------------
# Función para scrapear
# ------------------------------
def scrapear_idealista():
    datos = []

    for page in range(1, NUM_PAGES + 1):
        url = f"{BASE_URL}?pagina={page}"
        headers = {"User-Agent": random.choice(HEADERS_LIST)}
        proxy = {"http": random.choice(PROXIES)} if PROXIES else None

        print(f"Scrapeando página {page}…")
        response = requests.get(url, headers=headers, proxies=proxy)
        if response.status_code != 200:
            print(f"Error al obtener la página {page}, status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Cada anuncio
        anuncios = soup.select("article.item")  # Ajusta el selector si cambia la web
        for a in anuncios:
            try:
                precio = a.select_one(".item-price").get_text(strip=True)
                dormitorios = a.select_one(".item-detail").get_text(strip=True)
                metros = a.select_one(".item-meters").get_text(strip=True)
                barrio = a.select_one(".item-location").get_text(strip=True)

                datos.append({
                    "precio": precio,
                    "dormitorios": dormitorios,
                    "metros": metros,
                    "barrio": barrio
                })
            except:
                continue

        espera_aleatoria(1, 3)  # Delay aleatorio para no ser bloqueado

    return pd.DataFrame(datos)

# ------------------------------
# Uso
# ------------------------------
df = scrapear_idealista()
print(df.head())
print(f"Total anuncios scrapeados: {len(df)}")
