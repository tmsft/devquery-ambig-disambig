from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import tempfile

# import win32gui, win32con

# def minimize_chrome_blocking(timeout=5):
#     start = time.time()
#     while time.time() - start < timeout:
#         def enumHandler(hwnd, lParam):
#             if win32gui.IsWindowVisible(hwnd) and "Chrome" in win32gui.GetWindowText(hwnd):
#                 win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
#                 raise StopIteration  # break out early

#         try:
#             win32gui.EnumWindows(enumHandler, None)
#         except StopIteration:
#             return  # minimized successfully
#         time.sleep(0.05)  # poll every 50ms

def bing_search_headless(query, num_results=10):
    options = Options()
    # options.add_argument("--headless=new") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=1200,800") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    import shutil

    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.binary_location = "/usr/bin/google-chrome"
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    # minimize_chrome_blocking() 
    driver.get(f"https://www.bing.com/search?q={query.replace(' ', '+')}&count={num_results}")

    # time.sleep(0.1)
    # minimize_chrome()   # <-- Force minimize after opening
    
    time.sleep(3)
    page_source = driver.page_source
    driver.quit()
    shutil.rmtree(temp_dir)
    soup = BeautifulSoup(page_source, 'html.parser')
    
    titles = []
    snippets = []
    urls = []
    web_results = []

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



