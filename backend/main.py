# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from scraper import YahooFinanceSeleniumDriver,YahooFinanceScraper
from data_manager import DataManager
from pydantic import BaseModel

class TickerModel(BaseModel):
    ticker: str
    name: str
    exchange: str | None = None
    currency: str
    sector: str | None = None
    watchlist: bool = True
    industry: str | None = None

# Create an instance of the FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — runs on application start
    try:
        app.state.driver = YahooFinanceSeleniumDriver()
    except Exception as e:
        print(f"Failed to initialize Selenium driver: {e}")
        app.state.driver = None
    yield
    # Shutdown — runs on application stop
    if app.state.driver:
        app.state.driver.close_driver()

app = FastAPI(lifespan=lifespan)

# Define a path operation (or "route")
@app.get("/")
async def read_root():
    """
    This is the first endpoint of our FastAPI application.
    It returns a simple "Hello, World!" message.
    """

    return {"message": "Hello, World!"}

## Propojit scraper s FastAPI (`main.py`)

@app.get("/companies")
async def get_companies():
    dm = DataManager("backend/tickers.yaml")
    companies = dm.get_specific_values_yaml(["tickers", "ticker"])
    return {"companies": companies}

@app.get("/companies/{ticker}/pe")
async def get_PE(ticker, request: Request):
    scraper = YahooFinanceScraper(ticker,request.app.state.driver.driver)
    pe = scraper.get_pe_ratio()
    return {"pe": pe}

@app.post("/companies")
async def add_new_ticker(ticker: TickerModel, request: Request):
    dm = DataManager("backend/tickers.yaml")
    if dm.get_ticker(ticker.ticker, "tickers") is not None:
        return {"message": "FAIL - company with this ticker exists"}
    dm.add_ticker_yaml(ticker.model_dump(), "tickers")
    if dm.get_ticker(ticker.ticker, "tickers") is None:
        return {"message": "FAIL - data wasn't added"}
    return {"message": f"Data was added successfully. {request.base_url}companies/{ticker.ticker}"}

@app.delete("/companies/{ticker}")
async def delete_ticker(ticker: str, request: Request):
    dm = DataManager("backend/tickers.yaml")
    if dm.get_ticker(ticker, "tickers") is None:
        return {"message": "FAIL - company with this ticker doesn't exist"}
    dm.remove_ticker_yaml(ticker, "tickers")
    if dm.get_ticker(ticker, "tickers") is not None:
        return {"message": "FAIL - data wasn't removed"}
    return {"message": f"Ticker '{ticker}' was removed successfully."}
    


# fastapi dev backend/main.py
# http://127.0.0.1:8000