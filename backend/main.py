# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from backend.scraper import YahooFinanceSeleniumDriver,YahooFinanceScraper
from backend.data_manager import DataManager
from pydantic import BaseModel

class TickerRequest(BaseModel):
    ticker: str
    name: str
    exchange: str | None = None
    currency: str
    sector: str | None = None
    watchlist: bool = True
    industry: str | None = None

dm = DataManager("backend/tickers.yaml")

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

@app.get("/companies")
async def get_companies():
    companies = dm.get_specific_values_yaml(["tickers", "ticker"])
    return {"companies": companies}

@app.get("/companies/{ticker}/pe")
async def get_pe_ratio(ticker, request: Request):
    scraper = YahooFinanceScraper(ticker,request.app.state.driver.driver)
    pe = scraper.get_pe_ratio()
    if pe == "null":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"pe": pe}
        )
    return {"pe": pe}

@app.post("/companies",status_code=status.HTTP_201_CREATED)
async def create_ticker(ticker: TickerRequest, request: Request):
    if dm.get_ticker(ticker.ticker, "tickers") is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Company with this ticker already exists."}
        )
    dm.add_ticker_yaml(ticker.model_dump(), "tickers")
    if dm.get_ticker(ticker.ticker, "tickers") is None:
        return {"message": "FAIL - data wasn't added"}
    return {"message": f"Ticker '{ticker.ticker}' created.", "url": f"{request.base_url}companies/{ticker.ticker}"}

@app.delete("/companies/{ticker}")
async def delete_ticker(ticker: str, request: Request):
    if dm.get_ticker(ticker, "tickers") is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Ticker '{ticker}' not found."}
        )
    dm.remove_ticker_yaml(ticker, "tickers")
    if dm.get_ticker(ticker, "tickers") is not None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "FAIL - data wasn't removed"}
        )
    return {"message": f"Ticker '{ticker}' was removed successfully."}
    

# fastapi dev backend/main.py
# http://127.0.0.1:8000