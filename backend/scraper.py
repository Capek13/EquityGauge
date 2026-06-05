# scraper.py
from bs4 import BeautifulSoup
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class YahooFinanceSeleniumDriver:
    """Manages the Selenium WebDriver instance for Yahoo Finance scraping."""

    PAGE_LOAD_TIMEOUT = 5  # seconds
    TARGETED_URL = "https://finance.yahoo.com/quote/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    def __init__(self):
        self.driver = self._init_driver()
        self.accept_cookies()

    def _init_driver(self) -> webdriver.Chrome | None:
        """Initializes the Chrome WebDriver with headless options."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")           # required in Docker
        options.add_argument("--disable-dev-shm-usage") # required in Docker
        options.add_argument("--disable-gpu")
        options.add_argument(f"user-agent={self.USER_AGENT}")

        for binary in ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"]:
            if os.path.exists(binary):
                options.binary_location = binary
                break

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(15)
        return driver

    def accept_cookies(self):
        """Attempts to find and click the 'Accept all' cookies button on Yahoo Finance."""
        try:
            # Open the URL
            self.driver.get(self.TARGETED_URL)
            accept_button = WebDriverWait(self.driver, self.PAGE_LOAD_TIMEOUT).until(
                # //button//span catches both <button> and nested <span> variants
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept all')]"))
            )
            accept_button.click()
            print(f"Clicked 'Accept all' button for {self.TARGETED_URL}")
        except Exception as e:
            print(f"No 'Accept all' button found or not clickable: {e}")

    def close_driver(self):
        """Closes the Selenium WebDriver."""
        if self.driver:
            self.driver.quit()
            print("Selenium WebDriver closed.")
        else:
            print("No Selenium WebDriver to close.")


class YahooFinanceScraper:
    TARGETED_URL = "https://finance.yahoo.com/quote/"
    HEADER = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9', # Can help with language-specific content
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection': 'keep-alive',
        }
    REQUESTS_TIMEOUT = 2  # seconds
    
    def __init__(self, ticker: str, selenium_driver: webdriver.Chrome):
        """
        Initializes the YahooFinanceScraper with a stock ticker.

        :param ticker: Stock ticker symbol (e.g. 'AAPL').
        :param selenium_driver: An active Selenium Chrome WebDriver instance.
        """
        if not ticker:
            raise ValueError("Ticker cannot be empty.")
        self.ticker = ticker.upper() # Convert ticker to uppercase for consistency
        self.ticker_targeted_url = f"{self.TARGETED_URL}{self.ticker}/" 
        self.soup = None # Will hold the BeautifulSoup object after fetching the page
        self.selenium_driver = selenium_driver  # Will hold the Selenium WebDriver instance; webdriver.Chrome() will be used to initialize it
        self.connection_attempts = 3  # Number of attempts to connect to the page

    def _retry_fetch_page_selenium(self, url: str) -> BeautifulSoup | None:
        if self.connection_attempts > 0:
            print(f"Retrying fetch for {self.ticker}. Attempts left: {self.connection_attempts}")
            self.connection_attempts -= 1
            return self._fetch_with_selenium(url)
        print(f"Failed to fetch page for {self.ticker} after multiple attempts.")
        return None

    def _fetch_with_selenium(self, url: str) -> BeautifulSoup | None:
        """
        Fetches a page using Selenium and returns a BeautifulSoup object, or None on failure.

        :param url: URL to fetch.
        :return: Parsed BeautifulSoup object or None.
        """
        try:
            # Open the URL
            self.selenium_driver.get(url)

            # Wait for the page to load completely
            time.sleep(self.REQUESTS_TIMEOUT) 
            # Get the page source
            page_content = self.selenium_driver.page_source
            # Check for common HTTP error messages in the page title or content
            if "400" in self.selenium_driver.title or "Bad Request" in self.selenium_driver.page_source:
                print(f"Bad request (400) for {self.ticker}.")
                return None  # Return None for bad requests
            elif "401" in self.selenium_driver.title or "Unauthorized" in self.selenium_driver.page_source:
                print(f"Unauthorized access (401) for {self.ticker}.")
                return None  # Return None for unauthorized access
            elif "403" in self.selenium_driver.title or "Forbidden" in self.selenium_driver.page_source:
                print(f"Access forbidden (403) for {self.ticker}.")
                return None
            elif "404" in self.selenium_driver.title or "Not Found" in self.selenium_driver.page_source:
                print(f"Page not found (404) for {self.ticker}.")
                return None
            elif "408" in self.selenium_driver.title or "Request Timeout" in self.selenium_driver.page_source:
                print(f"Request timeout (408) for {self.ticker}.")
                return self._retry_fetch_page_selenium(url)
            elif "429" in self.selenium_driver.title or "Too Many Requests" in self.selenium_driver.page_source:
                print(f"Too many requests (429) for {self.ticker}.")
                return self._retry_fetch_page_selenium(url)
            elif "500" in self.selenium_driver.title or "Internal Server Error" in self.selenium_driver.page_source:
                print(f"Internal server error (500) for {self.ticker}.")
                return self._retry_fetch_page_selenium(url)
            elif "502" in self.selenium_driver.title or "Bad Gateway" in self.selenium_driver.page_source:
                print(f"Bad gateway (502) for {self.ticker}.")
                return self._retry_fetch_page_selenium(url)
            elif "503" in self.selenium_driver.title or "Service Unavailable" in self.selenium_driver.page_source:
                print(f"Service unavailable (503) for {self.ticker}.")
                return self._retry_fetch_page_selenium(url)
            elif "504" in self.selenium_driver.title or "Gateway Timeout" in self.selenium_driver.page_source:
                print(f"Gateway timeout (504) for {self.ticker}.")
                return self._retry_fetch_page_selenium(url)
            
            print(f"Successfully fetched page for {self.ticker} from {url}")
            return BeautifulSoup(page_content, 'html.parser')
        except Exception as e:
            print(f"Unexpected error during page fetch for {self.ticker}: {e}")
            return None

    def get_pe_ratio(self) -> str | None:
        """
        Fetches and returns the Trailing P/E ratio for the ticker.

        :return: P/E ratio as a string, or None if not found.
        """
        if not self.soup:
            # Fetch the page content if not already done
            print(f"Fetching P/E ratio for {self.ticker} from {self.ticker_targeted_url}")
            self.soup = self._fetch_with_selenium(self.ticker_targeted_url)
            if not self.soup:
                print(f"Failed to fetch page for {self.ticker}.")
                return None
        try:
            pe_row_header = self.soup.find('p', string=re.compile(r'Trailing P/E', re.IGNORECASE))
            if pe_row_header:
                # Find the next sibling <p> element which contains the P/E value
                pe_value_element = pe_row_header.find_next_sibling('p')
                if pe_value_element:
                    return pe_value_element.get_text(strip=True)
            print(f"P/E ratio for {self.ticker} not found using current selectors.")
            return None
        except Exception as e:
            print(f"Error parsing P/E ratio for {self.ticker}: {e}")
            return None


if __name__ == "__main__":
    # Tickers example for testing YahooFinanceScraper
    # You can replace these tickers with any valid stock ticker symbols

    # for testing use "?err=404", "?err=500" with TARGETED_URL without quote , in test change REQUESTS_TIMEOUT"
    # tickers_to_scrape = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMC", "META", "XYZ_NON_EXISTENT"]
    # tickers_to_scrape = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMC", "META"]
    tickers_to_scrape = ["META"]
    # dm = DataManager("backend/tickers.yaml")
    # tickers_to_scrape = dm.get_specific_values_yaml(["tickers","ticker"])

    # Initialize the Selenium driver
    selenium_driver = YahooFinanceSeleniumDriver()
    if not selenium_driver.driver:
        print("Failed to initialize Selenium WebDriver. Exiting.")
        exit(1)
    # Loop through the tickers and scrape the P/E ratio
    for ticker in tickers_to_scrape:
        scraper = YahooFinanceScraper(ticker, selenium_driver.driver)
        pe = scraper.get_pe_ratio()

        if pe is not None:
            print(f"Ticker: {ticker}, P/E Ratio: {pe}")
        else:
            print(f"Could not retrieve P/E Ratio for {ticker}.")
        print("-" * 30) 
    
    # Close the Selenium driver
    selenium_driver.close_driver()
    print("Scraping completed.")
