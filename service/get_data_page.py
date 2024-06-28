from bs4 import BeautifulSoup
from typing import List

class GetDataPage:
    
    def __init__(self,soup:BeautifulSoup) -> None:
        
        self.soup = soup
    
    def get_name_elemnts(self)->List[str]:
        
        name_elements = self.soup.find_all(class_='name')

        names = []
        
        for name in name_elements:
            name_tag = name.find('a')
            if name_tag:
                names.append(name_tag.get_text(strip=True))

        
        return names
    
    def get_url_images(self)->List[str]:
        
        image_elements = self.soup.find_all(class_='image')
        # Extraemos las URLs de las imágenes dentro de los elementos con la clase 'image'
        images = []
        
        for element in image_elements:
                img_tag = element.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    images.append(img_tag['src'])
        
        return images
          

    def get_prices(self)->List[str]:
        
        price_elements = self.soup.find_all(class_='price')
        # Guardamos en un arreglo la data para obtener el texto que contiene el div
        prices = [element.get_text(strip=True) for element in price_elements]
        
        return prices
        