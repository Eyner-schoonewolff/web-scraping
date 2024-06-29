import requests
from bs4 import BeautifulSoup
from service.get_data_page import GetDataPage, ScrapingError
from service.page_process_auto import ProcessAutomation
import pandas as pd


try:
    # clase para automatizar las tareas 
    process_automation = ProcessAutomation()

    page_content = process_automation.get_url_page(
        "https://flordeliz.com/index.php?route=product/category&path=77&page=2"
    )

    soup = BeautifulSoup(page_content, "html.parser") #Uso del BeautifulSoup para parsear el contenido HTML obtenido

    service_get_data = GetDataPage(soup=soup)

    # encontramos los elementos que necesitamos cada uno obteniendolo por su class
    names_flowers = service_get_data.get_name_elements()
    price_flowers = service_get_data.get_prices()
    image_url_flowers = service_get_data.get_url_images()

    # pasamos la data obtenida a un dataframe usando la libreria de pandas
    df_data = pd.DataFrame(
        {"name": names_flowers, "price": price_flowers, "image_url": image_url_flowers}
    )

    print(df_data)

except requests.RequestException as e:
    raise ScrapingError(f"Error de solicitud: {str(e)}")

except ScrapingError as e:
    print(f"Error durante la ejecución: {e.message}")

except Exception as e:
    print(f"Error inesperado: {str(e)}")
