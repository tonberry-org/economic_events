from economic_events.economic_event_fetcher import EconomicEventFetcher
from economic_events.economic_event_ingestor import EconomicEentIngestor


def main(argv: list[str]) -> None:
    ingestor = EconomicEentIngestor()
    result = EconomicEventFetcher().fetch_all_econmic_events()

    ingestor.ingest(event_data=result)


if __name__ == "__main__":
    main(["hellow"])
