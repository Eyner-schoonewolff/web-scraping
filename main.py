from service.get_data_page import ScrapingError
from service.page_process_auto import ProcessAutomation
import pandas as pd


def main():
    try:
        # clase para automatizar las tareas
        process_automation = ProcessAutomation()

        page_content = process_automation.get_url_page(
            "https://flordeliz.com/index.php?route=product/category&path=77&page=1"
        )

        # pasamos la data obtenida a un dataframe usando la libreria de pandas
        df_data = pd.DataFrame(page_content)

        # se exporta la informacion del dataFrame a un excel en formato xlsx
        df_data.to_excel("informacion_flores_naturales.xlsx", index=False)

    except ScrapingError as e:
        print(f"Error durante la ejecución: {e.message}")

    except Exception as e:
        print(f"Error inesperado: {str(e)}")


if __name__ == "__main__":
    main()
