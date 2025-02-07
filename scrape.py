from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup

SBR_WEBDRIVER = "https://brd-customer-hl_69a265fa-zone-ai_web_scraper:rdrq1ojgv04e@brd.superproxy.io:9515"

def scrape_website(website):
    print("Launching chrome browser...")

    try:
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            print('Connected! Navigating...')
            driver.get(website)
            print("Waiting for captcha to solve...")

            try:
                solve_res = driver.execute(
                    "executeCdpCommand",
                    {
                        "cmd": "Captcha.waitForSolve",
                        "params": {"detectTimeout": 10000},
                    },
                )
                print("Captcha solve status:", solve_res.get("value", {}).get("status", "Unknown"))
            except Exception as e:
                print("Captcha solving failed:", str(e))

            print("Navigated! Scraping page content...")
            html = driver.page_source
            if not html.strip():
                raise ValueError("Empty HTML content received!")

            return html  # Ensure the function returns the scraped content

    except Exception as e:
        print(f"Error occurred: {e}")
        return None  # Return None in case of an error

# Extracts body content safely
def extract_body_content(html_content):
    if not html_content:
        raise ValueError("extract_body_content received None or empty HTML!")

    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

# Cleans extracted content
def clean_body_content(body_content):
    if not body_content:
        return ""

    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

# Splits content into chunks for better readability
def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)]
