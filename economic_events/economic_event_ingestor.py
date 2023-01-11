from typing import Any
import boto3
import csv
import logging
import economic_events.config as config
import json
from decimal import Decimal
import pandas as pd
from datetime import datetime, timezone
import numpy as np

logging.basicConfig(
    level=config.get_logging_level(), format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


class EconomicEentIngestor:
    def __init__(self) -> None:
        self._s3_client = boto3.client("s3")
        self._ddb_economic_events = boto3.resource("dynamodb").Table(
            config.get_ddb_economic_events()
        )

    def write_to_csv(self, event_data: list[dict[str, Any]], name: str) -> str:
        filename = f"/tmp/{name}"
        logger.info(f"Writing {name} to csv {filename}")
        with open(filename, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.__get_keys(event_data))
            writer.writeheader()
            writer.writerows(event_data)
        return filename

    def dedup(self, event_data: list[dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(event_data)
        df["date"] = df["date"].map(
            lambda x: datetime.fromisoformat(x).replace(tzinfo=timezone.utc).isoformat()
        )
        df["id"] = (
            df["country"]
            + ":"
            + df["type"]
            + ":"
            + df["comparison"]
            + "/"
            + df["period"]
        )
        return (
            df.replace(np.nan, None)
            .sort_values(
                ["type", "country", "date", "comparison", "period", "previous"]
            )
            .groupby(["type", "country", "date", "comparison", "period"])
            .first()
            .reset_index()
        )

    def ingest(self, event_data: list[dict[str, Any]]) -> None:

        event_data_df = self.dedup(event_data)

        with self._ddb_economic_events.batch_writer() as batch:
            for index, row in event_data_df.iterrows():

                batch.put_item(json.loads(row.to_json(), parse_float=Decimal))

    def __get_keys(self, response: list[dict[str, Any]]) -> list[str]:
        return list(response[0].keys())
