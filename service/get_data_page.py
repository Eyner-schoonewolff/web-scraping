from bs4 import BeautifulSoup
from typing import List

class GetDataPage:
    
    def __init__(self,soup:BeautifulSoup) -> None:
        
        self.soup = soup
    
    def get_name_elements(self) -> List[str]:
        name_elements = self.soup.find_all(class_='name')
        return [name.find('a').get_text(strip=True) for name in name_elements if name.find('a')]
    
    def get_url_images(self) -> List[str]:
        image_elements = self.soup.find_all(class_='image')
        return [img_tag['src'] for element in image_elements if (img_tag := element.find('img')) and 'src' in img_tag.attrs]
    
    def get_prices(self) -> List[str]:
        price_elements = self.soup.find_all(class_='price')
        return [element.get_text(strip=True) for element in price_elements]
        