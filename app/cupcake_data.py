import aiohttp
from bs4 import BeautifulSoup

async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def parse_text_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    text_content = soup.get_text(separator='\n', strip=True)
    return text_content

async def fetch_all_data():
    cupcake_html = await fetch_content("https://www.torontocupcake.com/cupcakes.html")
    faq_html = await fetch_content("https://www.torontocupcake.com/faqs.html")
    delivery_html = await fetch_content("https://www.torontocupcake.com/delivery.html")

    cupcake_info = await parse_text_content(cupcake_html)
    faq_info = await parse_text_content(faq_html)
    delivery_info = await parse_text_content(delivery_html)

    return {
        "cupcakes": cupcake_info,
        "faqs": faq_info,
        "delivery": delivery_info
    }