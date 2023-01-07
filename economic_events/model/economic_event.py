from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class EconomicEvent(BaseModel):
    type: str
    comparison: str
    period: str
    country: str
    date: date
    actual: Decimal
    previous: Decimal
    estimate: Decimal
    change: Decimal
    change_percentage: Decimal


class EconomicEvents(BaseModel):
    events: list[EconomicEvent]
