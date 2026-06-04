from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Ticker(Base):
    __tablename__ = "tickers"

    ticker    = Column(String, primary_key=True)
    name      = Column(String, nullable=False)
    exchange  = Column(String)
    currency  = Column(String, nullable=False)
    sector    = Column(String)
    industry  = Column(String)
    watchlist = Column(Boolean, nullable=False, default=True)

    pe_ratios = relationship(
        "PERatios", 
        back_populates="stock", 
        cascade="all, delete-orphan", 
        order_by="PERatios.creation_date",
    )

    @property             
    def latest_pe(self):
        if not self.pe_ratios:
            return None
        return self.pe_ratios[-1]

    def __repr__(self) -> str:
        return f"<Ticker {self.ticker} ({self.name})>"


class PERatios(Base):
    __tablename__ = "peratios"

    id            = Column(Integer, primary_key=True)
    ticker        = Column(String, ForeignKey("tickers.ticker"), nullable=False, index=True)
    pe            = Column(Numeric(10, 4), nullable=False)
    creation_date = Column(Date, nullable=False)

    stock = relationship("Ticker", back_populates="pe_ratios")

    def __repr__(self) -> str:
        return f"<PERatios {self.ticker} {self.creation_date} pe={self.pe}>"
