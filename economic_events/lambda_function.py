from typing import Any, Mapping
from economic_events.economic_event_fetcher import EconomicEventFetcher
from economic_events.economic_event_ingestor import EconomicEentIngestor
from datetime import date
from slack_bot_client.slack_client import SlackClient, SlackChannel


def slack_processed(result: dict[date, list[dict[str, Any]]]) -> None:
    message = "Econmoic Events Ingestion\n"
    for key, value in result.items():
        message += f"- {key.isoformat()}: {len(value)}"
    SlackClient().send(SlackChannel.MONITORING, message)


def lambda_handler(event: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    ingestor = EconomicEentIngestor()
    today = date.today()
    result = EconomicEventFetcher().fetch_days_to_process(today)
    for _, event_data in result.items():
        ingestor.ingest(event_data=event_data)

    slack_processed(result)
    return "OK"
