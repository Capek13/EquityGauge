import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
from backend.scraper import YahooFinanceSeleniumDriver,YahooFinanceScraper

FAKE_PE_HTML = "<p>Trailing P/E</p><p>28.5</p>"

class TestYahooFinanceScraperInit(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()

    def test_ticker_is_uppercased(self):
        scraper = YahooFinanceScraper("aapl", self.mock_driver)
        self.assertEqual(scraper.ticker, "AAPL")
    
    def test_empty_ticker_raises_value_error(self):
        with self.assertRaises(ValueError):
            YahooFinanceScraper("", self.mock_driver)

    def test_soup_is_none_on_init(self):
        scraper = YahooFinanceScraper("AAPL", self.mock_driver)
        self.assertEqual(scraper.ticker_targeted_url, f"{scraper.TARGETED_URL}AAPL/")

class TestFetchWithSelenium(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_driver.title = "AAPL - Yahoo Finance"
        self.mock_driver.page_source = FAKE_PE_HTML 
        self.scraper = YahooFinanceScraper("AAPL",self.mock_driver)
    
    def test_success_returns_beautifulsoup(self):
        result = self.scraper._fetch_with_selenium("https://...")
        self.assertIsInstance(result, BeautifulSoup)
    
    def test_404_returns_none(self):
        self.mock_driver.title = "404"
        self.mock_driver.page_source = "Not Found"
        result = self.scraper._fetch_with_selenium("https://...")
        self.assertIsNone(result)

    def test_408_triggers_retry(self):
        self.mock_driver.title = "408"
        self.mock_driver.page_source = "Request Timeout"
        with patch.object(self.scraper, "_retry_fetch_page_selenium", return_value=None) as mock_retry:
            self.scraper._fetch_with_selenium("https://...")
        mock_retry.assert_called_once()

    def test_exception_returns_none(self):
        self.mock_driver.get.side_effect = Exception("network error")
        result = self.scraper._fetch_with_selenium("https://...")
        self.assertIsNone(result)

class TestGetPeRatio(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.scraper = YahooFinanceScraper("AAPL", self.mock_driver)

    def test_soup_is_none(self):
        self.mock_driver.soup = None
        with patch.object(self.scraper, "_fetch_with_selenium", return_value=None) as mock_fetch:
            result = self.scraper.get_pe_ratio()
        self.assertIsNone(result)

    def test_get_pe_ratio(self):
        self.scraper.soup = BeautifulSoup(FAKE_PE_HTML, "html.parser")
        result = self.scraper.get_pe_ratio()
        self.assertEqual(result, '28.5')

    def test_returns_none_if_element_missing(self):
        self.scraper.soup = BeautifulSoup("<html></html>", "html.parser")
        self.assertIsNone(self.scraper.get_pe_ratio())
    
    def test_parsing_error(self):
        self.scraper.soup = "not_a_soup_object"
        with patch("builtins.print") as mock_print:
            result = self.scraper.get_pe_ratio()
        last_print_msg = mock_print.call_args[0][0]
        self.assertIn("Error parsing", last_print_msg)
        self.assertIsNone(result)  

    def test_does_not_refetch_if_soup_exists(self):
        self.scraper.soup = BeautifulSoup(FAKE_PE_HTML, "html.parser")
        with patch.object(self.scraper, "_fetch_with_selenium") as mock_fetch:
            result = self.scraper.get_pe_ratio()
        mock_fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()