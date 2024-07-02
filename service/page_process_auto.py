import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from service.get_data_page import GetDataPage
from bs4 import BeautifulSoup
from typing import List, Dict


class ProcessAutomation:

    def __init__(self, notifications_enabled: bool = False) -> None:
        self.chrome_options = self.get_chrome_options(notifications_enabled)
        self.service = self.get_service()

    def get_chrome_options(self, notifications_enabled: bool) -> Options:
        """
        Configura las opciones del navegador Chrome.

        :param notifications_enabled: Si True, permite notificaciones; si False, las deshabilita.
        :return: Un objeto de opciones de Chrome configurado.
        """
        chrome_options = Options()
        prefs = {
            "profile.default_content_setting_values.notifications": (
                1 if notifications_enabled else 2
            )
        }
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

    def get_service(self) -> Service:
        """
        Inicializa el servicio de ChromeDriver usando webdriver-manager.

        :return: Un objeto de servicio de ChromeDriver.
        """
        return Service(ChromeDriverManager().install())

    def get_url_page(self, page: str) -> List[Dict[str, str]]:
        """
        Abre la página especificada y devuelve el contenido HTML de la página.

        :param page: URL de la página que se quiere abrir.
        :return: El contenido HTML de la página.
        """
        try:
            driver = webdriver.Chrome(service=self.service, options=self.chrome_options)

            driver.get(page)

            all_itmes = self.pagination_web_action(driver)

            time.sleep(5)  # Ajustar el tiempo de espera según sea necesario

        except WebDriverException as e:
            print(f"Error al abrir la página: {e}")
        finally:

            driver.quit()

        return all_itmes

    def pagination_web_action(self, driver: webdriver.Chrome):
        # Lógica para ir pasando de página en página a través de la paginación
        all_items = []
        # el rango es la cantidad de paginas la cual se paginaran
        for _ in range(3):
            """
            Obtendremos la data de cada una de las paginas mientras se va paginando.

            :param driver: driver el cual cumplira la funcion de obtener la pagina.
            :return: una lista de objeto que tendra el nombre, precio y la url.
            """
            try:

                # Esperar a que la lista ul con clase pagination esté presente
                pagination_list = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination"))
                )

                # obtenemos el recurso de la pagina y la parseamos a un contenido HTML
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")

                # le mandamos a la clase la data de la pagina parseada
                getDataPage = GetDataPage(soup)

                names = getDataPage.get_name_elements()
                prices = getDataPage.get_prices()
                urls = getDataPage.get_url_images()
                
                # iteramos por cada una de la informacion obtenida el nombre precio y url vamos agrandola a una lis 
                for name, price, url in zip(names, prices, urls):
                    all_items.append(
                        {"name": name, "price": price, "url": url}
                    )  # Agregar los nombres de la página actual a la lista total

                # Buscar el elemento li que contiene el enlace <a> con el texto '>'
                next_page_link = pagination_list.find_element(
                    By.XPATH, './/li/a[text()=">"]'
                )

                # Desplazarse hasta el enlace antes de hacer clic
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);", next_page_link
                )
                WebDriverWait(driver, 10).until(EC.visibility_of(next_page_link))

                # Intentar hacer clic utilizando JavaScript para evitar posibles interceptaciones
                driver.execute_script("arguments[0].click();", next_page_link)

                time.sleep(5)

            except Exception as e:
                print(
                    f"Error al intentar hacer clic en el enlace de siguiente página: {e}"
                )
                break

        return all_items
