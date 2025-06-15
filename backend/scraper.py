# scraper.py
from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class YahooFinanceScraper:
    TARGETED_URL = "https://finance.yahoo.com/quote/"
    HEADER = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9', # Can help with language-specific content
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection': 'keep-alive',
        }
    REQUESTS_TIMEOUT = 5  # seconds
    
    def __init__(self, ticker: str):
        """
        Inializated the YahooFinanceScraper with a stock ticker.
        :param ticker: Stock ticker symbol (e.g., 'AAPL' for Apple Inc.)
        """
        if not ticker:
            raise ValueError("Ticker cannot be empty.")
        self.ticker = ticker.upper() # Convert ticker to uppercase for consistency
        self.ticker_targeted_url = f"{self.TARGETED_URL}{self.ticker}/" 
        self.soup = None # Will hold the BeautifulSoup object after fetching the page

    def _fetch_page_request(self, url: str)-> BeautifulSoup | None:
        """
        Fetches the content of a given URL and returns a BeautifulSoup object or None if an error occurs.
        """
        try:
            response = requests.get(url, headers=self.HEADER, timeout=self.REQUESTS_TIMEOUT)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            print(f"Successfully fetched page for {self.ticker} from {url}")
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {self.ticker} ({url}): {e.response.status_code} - {e.response.reason}")
            if e.response.status_code == 404:
                print(f"Ticker {self.ticker} or page not found.")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error for {self.ticker} ({url}): {e}")
            return None
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error for {self.ticker} ({url}): {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching {self.ticker} ({url}): {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during page fetch for {self.ticker}: {e}")
            return None
    
    def _fetch_page_selenium(self, url: str)-> BeautifulSoup | None:
        """
        Fetches the content of a given URL using Selenium and returns a BeautifulSoup object or None if an error occurs.
        """
         # Set up Selenium WebDriver with Chrome options
        options = Options()
        options.add_argument("--headless")  # Run in headless mode (no GUI)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
         # Initialize the WebDriver 
        driver = webdriver.Chrome(options=options)

        try:
            # Open the URL
            driver.get(self.ticker_targeted_url)
            try:
                accept_button = WebDriverWait(driver, self.REQUESTS_TIMEOUT).until(
                    # Wait for the "Accept All" button to be clickable
                    # By.XPATH is used to locate the button by its text, // is for find elements anywhere on page
                    # sometimes is in button tag, sometimes in a div or span -> //button//span[contains(text(), 'Accept All')]
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept all')]"))
                )
                accept_button.click()  # Click the "Accept All" button if it appears
                print(f"Clicked 'Accept All' button for {self.TARGETED_URL}")
            except Exception as e:
                print(f"No 'Accept All' button found for {self.TARGETED_URL} or it was not clickable: {e}")

            # Wait for the page to load completely
            time.sleep(self.REQUESTS_TIMEOUT) 
            # Get the page source
            page_content = driver.page_source
            print(f"Successfully fetched page for {self.ticker} from {url}")
            return BeautifulSoup(page_content, 'html.parser')
        except Exception as e:
            print(f"An unexpected error occurred during page fetch for {self.ticker}: {e}")
            return None
        
    def get_pe_ratio(self) -> str | None:
        """
        Fetches the P/E ratio for the stock ticker.
        Returns the P/E ratio as a string or None if not found.
        """
        if not self.soup:
            # Fetch the page content if not already done
            print(f"Fetching P/E ratio for {self.ticker} from {self.ticker_targeted_url}")
            self.soup = self._fetch_page_selenium(self.ticker_targeted_url)
            if not self.soup:
                print(f"Failed to fetch page for {self.ticker}.")
                return None
        try:
            pe_row_header = self.soup.find('p', string=re.compile(r'Trailing P/E', re.IGNORECASE))
            print(pe_row_header)
            if pe_row_header:
                # Find the next sibling <p> element which contains the P/E value
                pe_value_element = pe_row_header.find_next_sibling('p')
                if pe_value_element:
                    return pe_value_element.get_text(strip=True) # strip= True removes leading/trailing whitespace

                print(f"P/E Ratio for {self.ticker} not found on the page using current selectors.")
                return None
            
        except Exception as e:
            print(f"Error parsing P/E Ratio for {self.ticker}: {e}")
            return None
    

if __name__ == "__main__":
    # Tickers example for testing YahooFinanceScraper
    # You can replace these tickers with any valid stock ticker symbols
    tickers_to_scrape = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMC", "META", "XYZ_NON_EXISTENT"]
    tickers_to_scrape = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMC", "META"]
    tickers_to_scrape = ["META"]

    # Loop through the tickers and scrape the P/E ratio
    for ticker in tickers_to_scrape:
        scraper = YahooFinanceScraper(ticker)
        pe = scraper.get_pe_ratio()

        if pe is not None:
            print(f"Ticker: {ticker}, P/E Ratio: {pe}")
        else:
            print(f"Could not retrieve P/E Ratio for {ticker}.")
        print("-" * 30) 
    