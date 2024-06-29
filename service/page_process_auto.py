import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException


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

    def get_url_page(self, page: str) -> str:
        """
        Abre la página especificada y devuelve el contenido HTML de la página.

        :param page: URL de la página que se quiere abrir.
        :return: El contenido HTML de la página.
        """
        try:
            driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
            driver.get(page)
            time.sleep(5)  # Ajustar el tiempo de espera según sea necesario
            page_source = driver.page_source
        except WebDriverException as e:
            print(f"Error al abrir la página: {e}")
            page_source = ""
        finally:
            driver.quit()

        return page_source
