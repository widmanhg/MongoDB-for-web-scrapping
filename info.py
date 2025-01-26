from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

class MercadoLibreScraper:
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="scrapper", urls_collection="urls", info_collection="info"):
        """Inicializa la conexión a MongoDB y las colecciones necesarias."""
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.urls_collection = self.db[urls_collection]
        self.info_collection = self.db[info_collection]

    def scrape_product_info(self):
        """Obtiene la información del producto para cada URL almacenada y la guarda en MongoDB."""
        for document in self.urls_collection.find():
            url = document.get("url")
            if not url:
                continue

            producto = ProductoMercadoLibre(url)
            data = producto.extract_data()

            if data:
                self.info_collection.insert_one(data)
                print(f"Datos guardados para: {url}")

    def close_connection(self):
        """Cierra la conexión a MongoDB."""
        self.client.close()

class ProductoMercadoLibre:
    def __init__(self, url):
        """Inicializa la instancia con la URL del producto."""
        self.url = url

    def make_http_request(self):
        """Realiza una solicitud HTTP y devuelve el contenido HTML."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {self.url}: {e}")
            return None

    def extract_data(self):
        """Extrae los datos relevantes del producto desde el contenido HTML."""
        html_content = self.make_http_request()

        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        img_zoom_tags = soup.select('div.ui-pdp-gallery__column .ui-pdp-gallery__wrapper figure.ui-pdp-gallery__figure img[data-zoom]')
        img_zoom_values = [img_zoom['data-zoom'] for img_zoom in img_zoom_tags]

        titulo = self._extract_text(soup, 'h1', {'class': 'ui-pdp-title'})
        calificacion = self._extract_text(soup, 'span', {'class': 'ui-pdp-review__rating'})
        disponibilidad = self._extract_text(soup, 'span', {'class': 'ui-pdp-buybox__quantity__available'})
        precio = self._extract_text(soup, 'div', {'class': 'ui-pdp-price__second-line'}, sub_tag='span', sub_attrs={'class': 'andes-money-amount__fraction'})
        cantidad_resenas = self._extract_text(soup, 'span', {'class': 'ui-pdp-review__amount'})
        codigo_producto = self._extract_text(soup, 'span', {'class': 'ui-pdp-color--BLUE ui-pdp-family--REGULAR'})
        precio_descuento = self._extract_text(soup, 'div', {'class': 'ui-pdp-price__main-container'}, sub_tag='span', sub_attrs={'class': 'andes-money-amount__discount'})
        precio_original = self._extract_text(soup, 'span', class_contains='andes-money-amount__fraction')

        data = {
            "titulo": titulo,
            "calificacion": calificacion,
            "disponibilidad": disponibilidad,
            "precio": precio,
            "cantidad_resenas": cantidad_resenas,
            "codigo_producto": codigo_producto,
            "descuento": precio_descuento,
            "precio_original": precio_original,
            "imagenes": img_zoom_values
        }

        return data

    def _extract_text(self, soup, tag, attrs=None, sub_tag=None, sub_attrs=None, class_contains=None):
        """Helper para extraer texto de un elemento HTML opcionalmente anidado."""
        try:
            element = soup.find(tag, attrs=attrs)
            if sub_tag and element:
                element = element.find(sub_tag, attrs=sub_attrs)
            if class_contains and not element:
                element = soup.find(tag, class_=lambda x: x and class_contains in x)
            return element.text.strip() if element else None
        except AttributeError:
            return None

if __name__ == "__main__":
    scraper = MercadoLibreScraper()
    scraper.scrape_product_info()
    scraper.close_connection()
