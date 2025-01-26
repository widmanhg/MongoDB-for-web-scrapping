import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

class MercadoLibreScraper:
    def __init__(self, palabras_clave, base_url, num_paginas, mongo_uri="mongodb://localhost:27017/", db_name="scrapper", collection_name="urls"):
        self.palabras_clave = palabras_clave
        self.base_url = base_url
        self.num_paginas = num_paginas

        # Conexión a MongoDB
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def _get_page_urls(self, palabra_clave, pagina):
        """Obtiene las URLs de una página específica para una palabra clave."""
        url = f"{self.base_url}{palabra_clave}#D[A:{palabra_clave}]&page={pagina}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            elementos_a = soup.find_all('a', class_='poly-component__title')
            return [elemento_a.get('href', '') for elemento_a in elementos_a]
        except requests.exceptions.RequestException as e:
            print(f"Error while scraping {url}: {e}")
            return []

    def scrape_urls(self):
        """Realiza el scraping de URLs para todas las palabras clave y las almacena en MongoDB."""
        for palabra in self.palabras_clave:
            urls_set = set()
            print(f"Scraping palabra clave: {palabra}")

            for pagina in range(1, self.num_paginas + 1):
                urls = self._get_page_urls(palabra, pagina)
                for url in urls:
                    if url and url not in urls_set:
                        urls_set.add(url)
                        self._save_url_to_db(url)

    def _save_url_to_db(self, url):
        """Guarda una URL en MongoDB si no existe ya."""
        if not self.collection.find_one({"url": url}):
            self.collection.insert_one({"url": url})
            print(f"URL guardada en MongoDB: {url}")
        else:
            print(f"URL ya existente: {url}")

    def show_saved_urls(self):
        """Muestra todas las URLs almacenadas en la base de datos."""
        print("\nURLs almacenadas en MongoDB:")
        for document in self.collection.find():
            print(document)

    def close_connection(self):
        """Cierra la conexión con MongoDB."""
        self.client.close()

if __name__ == "__main__":
    palabras_clave = ['abrigos', 'laptop', 'zapato']
    base_url = 'https://listado.mercadolibre.com.mx/'
    num_paginas = 10

    scraper = MercadoLibreScraper(palabras_clave, base_url, num_paginas)
    scraper.scrape_urls()
    scraper.show_saved_urls()
    scraper.close_connection()
