from typing import Any
import boto3
import csv
import logging
import economic_events.config as config


logging.basicConfig(
    level=config.get_logging_level(), format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


class EconomicEentIngestor:
    def __init__(self) -> None:
        self._s3_client = boto3.client("s3")
        self._s3_bucket_name = "tonberry-economic-events"

    def write_to_csv(self, event_data: list[dict[str, Any]], name: str) -> str:
        filename = f"/tmp/{name}"
        logger.info(f"Writing {name} to csv {filename}")
        with open(filename, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.__get_keys(event_data))
            writer.writeheader()
            writer.writerows(event_data)
        return filename

    def ingest(self, event_data: list[dict[str, Any]], name: str) -> None:
        logger.info(f"Writing {name} to s3 {self._s3_bucket_name}")
        filename = self.write_to_csv(event_data, name)
        with open(filename, "rb") as csvfile:
            self._s3_client.put_object(
                Bucket=self._s3_bucket_name,
                Key=name,
                Body=csvfile,
            )

    def __get_keys(self, response: list[dict[str, Any]]) -> list[str]:
        return list(response[0].keys())
