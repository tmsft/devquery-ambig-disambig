from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def bing_search_headless(query, num_results=10):
    options = Options()
    
    # Headless but disguised as normal Chrome
    options.add_argument("--headless=new")  # New headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Spoof the User Agent so sites treat us like a real Chrome browser
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.5790.171 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    # Remove Selenium "automation" fingerprint
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """
        },
    )

    # Load Bing search page
    driver.get(f"https://www.bing.com/search?q={query.replace(' ', '+')}&count={num_results}")
    time.sleep(3)  # Let the page fully render

    page_source = driver.page_source
    driver.quit()

    # Parse results
    soup = BeautifulSoup(page_source, 'html.parser')

    titles, snippets, urls, web_results = [], [], [], []

    for item in soup.find_all('li', {'class': 'b_algo'})[:num_results]:
        title_tag = item.find('h2')
        link_tag = item.find('a')
        snippet_tag = item.find('p')

        if title_tag and link_tag:
            title = title_tag.text.strip()
            url = link_tag['href']
            snippet = snippet_tag.text.strip() if snippet_tag else "No snippet available"

            titles.append(title)
            snippets.append(snippet)
            urls.append(url)
            web_results.append({
                'title': title,
                'url': url,
                'snippet': snippet
            })

    return {
        "Top_10_Titles": "#SEP#".join(titles),
        "Top_10_Snippets": "#SEP#".join(snippets),
        "Top_10_Urls": "#SEP#".join(urls),
        "WebResults": web_results
    }
