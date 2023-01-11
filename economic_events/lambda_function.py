from typing import Any, Mapping
from economic_events.economic_event_fetcher import EconomicEventFetcher
from economic_events.economic_event_ingestor import EconomicEentIngestor
from datetime import date


def lambda_handler(event: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    ingestor = EconomicEentIngestor()
    result = EconomicEventFetcher().fetch_days_to_process(date.today())
    for _, event_data in result.items():
        ingestor.ingest(event_data=event_data)

    return "OK"
