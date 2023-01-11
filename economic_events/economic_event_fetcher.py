from typing import Any
from eod import EodHistoricalData
import economic_events.config as config
from datetime import date, timedelta
import calendar
from pydantic import BaseModel
import logging

logging.basicConfig(
    level=config.get_logging_level(), format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


class DatesRangeToProcess(BaseModel):
    fromDate: date
    toDate: date


class EconomicEventFetcher:
    def __init__(self) -> None:
        self._client = EodHistoricalData(config.get_api_eod())

    def monthly_date_range(self, target_date: date) -> DatesRangeToProcess:
        start = target_date.replace(day=1)
        end = self.get_end_of_month(target_date)
        return DatesRangeToProcess(fromDate=start, toDate=end)

    def get_previous_month(self, target_date: date) -> DatesRangeToProcess:
        start = (target_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        end = self.get_end_of_month(start)
        return DatesRangeToProcess(fromDate=start, toDate=end)

    def dates_to_process(self, source_date: date) -> list[DatesRangeToProcess]:
        return [
            self.get_previous_month(source_date),
            self.monthly_date_range(source_date),
        ]

    def fetch_days_to_process(
        self, source_date: date
    ) -> dict[date, list[dict[str, Any]]]:
        results: dict[date, list[dict[str, Any]]] = {}
        days_to_process = self.dates_to_process(source_date)
        logger.info(f"Dates to process: {days_to_process}")
        for date_to_process in days_to_process:
            results[
                date_to_process.fromDate
            ] = self.fetch_econmic_events_for_date_range(
                date_to_process.fromDate, date_to_process.toDate
            )
        return results

    def fetch_econmic_events_for_date_range(
        self, fromDate: date, toDate: date
    ) -> list[dict[str, Any]]:
        logger.info(f"Fetching from {fromDate} to {toDate}")
        result: list[dict[str, Any]] = []
        count = 1000
        offset = 0
        while count >= 1000:
            response = self._client.get_economic_events(
                from_=fromDate.isoformat(),
                to=toDate.isoformat(),
                country="US",
                limit=1000,
                offset=offset,
            )
            result = result + response
            count = len(response)
            offset += count
        return result

    def get_end_of_month(self, for_date: date) -> date:
        range = calendar.monthrange(for_date.year, for_date.month)[1]
        return date(for_date.year, for_date.month, range)

    def fetch_all_econmic_events(
        self, since: date = date(2020, 1, 1)
    ) -> list[dict[str, Any]]:
        today = date.today()
        current_from = since
        current_to = self.get_end_of_month(current_from)
        result = []
        while current_from < today:
            result += self.fetch_econmic_events_for_date_range(
                fromDate=current_from, toDate=current_to
            )
            current_from = current_to + timedelta(days=1)
            current_to = self.get_end_of_month(current_from)
        return result
