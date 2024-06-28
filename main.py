import requests
from bs4 import BeautifulSoup
from service.get_data_page import GetDataPage
import pandas as pd

page = requests.get('https://flordeliz.com/index.php?route=product/category&path=77&page=2')

try:

    # verifiamos que el request tenga una respuesta http 200
    if page.status_code == 200:
        
        soup = BeautifulSoup(page.content,'html.parser')
        
        service_get_data = GetDataPage(soup = soup)
        # encontramos los elementos del HTML que contienen la clase Price
        names_flowers = service_get_data.get_name_elements()
        price_flowers = service_get_data.get_prices()
        image_url_flowers = service_get_data.get_url_images()

        # data en object
        data = {'name':names_flowers,'price': price_flowers, 'image_url': image_url_flowers}
        # pasamos la data obtenida a un dataframe usando la libreria de pandas
        df_data = pd.DataFrame(data)
        
        print(df_data)
                  
except requests.RequestException as e:
        raise Exception(status_code=500, detail=str(e))