import yaml
from backend.database import SessionLocal, engine
from backend.models import Base, Ticker

Base.metadata.create_all(engine)

with open("backend/tickers.yaml") as f:
    data = yaml.safe_load(f)

db = SessionLocal()
try:
    for row in data["tickers"]:
        if not db.query(Ticker).filter(Ticker.ticker == row["ticker"]).first():
            db.add(Ticker(**row))
    db.commit()
    print(f"Seeded {len(data['tickers'])} tickers.")
finally:
    db.close()
