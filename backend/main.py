# main.py
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.scraper import YahooFinanceSeleniumDriver,YahooFinanceScraper
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.database import get_db, engine
from backend.models import Ticker, PERatios, Base
from datetime import date

class TickerRequest(BaseModel):
    ticker: str
    name: str
    exchange: str | None = None
    currency: str
    sector: str | None = None
    watchlist: bool = True
    industry: str | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    app.state.driver = None
    yield
    if app.state.driver:
        app.state.driver.close_driver()

app = FastAPI(lifespan=lifespan)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return RedirectResponse(url=FRONTEND_URL)

@app.get("/companies")
async def get_companies(db: Session = Depends(get_db)):
    return {"companies": db.query(Ticker).all()}

@app.get("/companies/{ticker}/pe")
async def get_pe_ratio(ticker: str, request: Request, db: Session = Depends(get_db)):
    if not db.query(Ticker).filter(Ticker.ticker == ticker).first():
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"pe": None})
    last_pe = db.query(PERatios).filter(PERatios.ticker == ticker).order_by(PERatios.creation_date.desc()).first()
    if last_pe is None or last_pe.creation_date < date.today():
        if request.app.state.driver is None:
            try:
                request.app.state.driver = YahooFinanceSeleniumDriver()
            except Exception as e:
                print(f"Failed to initialize Selenium driver: {e}")
                return JSONResponse(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    content={"message": "Scraper is unavailable."}
                )
        scraper = YahooFinanceScraper(ticker, request.app.state.driver.driver)
        pe = scraper.get_pe_ratio()
        if pe is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"pe": pe}
            )
        db.add(PERatios(ticker=ticker, pe=pe, creation_date=date.today()))
        db.commit()
    else:
        pe = last_pe.pe

    return {"pe": pe}
    
@app.post("/companies",status_code=status.HTTP_201_CREATED)
async def create_ticker(ticker: TickerRequest, request: Request, db: Session = Depends(get_db)):
    if db.query(Ticker).filter(Ticker.ticker == ticker.ticker).first():
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Company with this ticker already exists."}
        )
    db.add(Ticker(**ticker.model_dump()))
    db.commit()
    if db.query(Ticker).filter(Ticker.ticker == ticker.ticker).first():
        return {"message": f"Ticker '{ticker.ticker}' created.", "url": f"{request.base_url}companies/{ticker.ticker}"}
    return {"message": "FAIL - data wasn't added"}

@app.delete("/companies/{ticker}")
async def delete_ticker(ticker: str, request: Request, db: Session = Depends(get_db)):
    obj = db.query(Ticker).filter(Ticker.ticker == ticker).first()
    if not obj:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Ticker '{ticker}' not found."}
        )
    db.delete(obj)
    db.commit()
    if not db.query(Ticker).filter(Ticker.ticker == ticker).first():
        return {"message": f"Ticker '{ticker}' was removed successfully."}
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "FAIL - data wasn't removed"}
        )
