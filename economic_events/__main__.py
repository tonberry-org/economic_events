from economic_events.economic_event_fetcher import EconomicEventFetcher
from economic_events.economic_event_ingestor import EconomicEentIngestor
from datetime import date


def main(argv: list[str]) -> None:
    ingestor = EconomicEentIngestor()
    result = EconomicEventFetcher().fetch_days_to_process(date.today())
    for start_date, event_data in result.items():
        ingestor.ingest(event_data=event_data, name=start_date.isoformat())


if __name__ == "__main__":
    main(["hellow"])
