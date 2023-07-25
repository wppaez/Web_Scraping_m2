import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def click_filter_buttons(page, category, operation_type, location):
    await page.goto("https://www.metrocuadrado.com/")

    # Hacemos clic en el botón de categoría (Oficinas, Locales, Bodegas)
    await page.click(f'span:text("{category}")', timeout=5000)

    # Hacemos clic en el botón de tipo de operación (Comprar, Arrendar)
    await page.click(f'span:text("{operation_type}")', timeout=5000)

    # Hacemos clic en el botón de ubicación (Barranquilla, Puerto Colombia, Soledad)
    await page.click(f'span:text("{location}")', timeout=5000)

async def scrape_info(page):
    data = []

    titles = await page.query_selector_all(".title h2")
    prices = await page.query_selector_all(".price")
    areas = await page.query_selector_all(".m2")

    for title, price, area in zip(titles, prices, areas):
        data.append({
            "Title": await title.text_content(),
            "Price": await price.text_content(),
            "Area": await area.text_content(),
        })

    return data

async def main():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    categories = ["Oficinas", "Locales", "Bodegas"]
    operation_types = ["Comprar", "Arrendar"]
    locations = ["Barranquilla (Atlántico)", "Puerto Colombia (Atlántico)", "Soledad (Atlántico)"]

    all_data = []

    for category in categories:
        for operation_type in operation_types:
            for location in locations:
                await click_filter_buttons(page, category, operation_type, location)
                data = await scrape_info(page)
                all_data.extend(data)

    await context.close()
    await browser.close()
    await playwright.stop()

    # Convertimos los datos en un DataFrame usando pandas
    df = pd.DataFrame(all_data)

    # Creamos una carpeta "output" si no existe
    import os
    if not os.path.exists("output"):
        os.makedirs("output")

    # Guardamos el DataFrame en un archivo Excel
    df.to_excel("output/metrocuadrado_data.xlsx", index=False, engine="openpyxl")

if __name__ == "__main__":
    asyncio.run(main())
