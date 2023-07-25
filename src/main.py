import asyncio
from playwright.async_api import async_playwright


capabilities = {
    "browserName": "Chrome",  # Browsers allowed: `Chrome`, `MicrosoftEdge`, `pw-chromium`, `pw-firefox` and `pw-webkit`
    "browserVersion": "latest",
    "LT:Options": {
        "platform": "Windows 10",
        "build": "E Commerce Scrape Build",
        "network": False,
        "video": True,
        "console": True,
        "tunnel": False,  # Add tunnel configuration if testing locally hosted webpage
        "tunnelName": "",  # Optional
        "geoLocation": "",  # country code can be fetched from https://www.lambdatest.com/capabilities-generator/
    },
}



async def main():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context() # Creates a new browser context 
    page = await context.new_page() # Open new page 
    await page.goto("https://www.metrocuadrado.com/") # Go to the chosen website
    await context.close()
    await browser.close()
    await playwright.stop()

if __name__ == "__main__":
    asyncio.run(main())

    