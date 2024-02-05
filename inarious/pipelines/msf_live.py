from datetime import datetime
import requests  # type: ignore

from inarious.pipelines.artemis import ArtemisCreate
from inarious.config import settings


class MsfLive:

    def __init__(self, data_type: str, year: int):
        self.data_type = data_type
        self.year = year
        self.games_artemis_create = ArtemisCreate(data_type="msf-live-games")

    @property
    def apollo_mongodb_api(self):
        return f"{settings.APOLLO_API}/mongodb/msf-live"

    def get_documents(self):
        return requests.get(
            url=f"{self.apollo_mongodb_api}/year/{self.year}/{self.data_type}"
        )

    def get_and_send(self):
        docs = self.get_documents()
        documents = docs.json()
        for doc in documents:
            document_dict = {}
            if self.data_type == "games":
                document_dict["games"] = doc["games"]
                document_dict["date"] = datetime.strftime(
                    datetime.strptime(doc["date"], "%Y%m%d"), "%Y-%m-%d"
                )
                if self.games_artemis_create.send_data(data=document_dict).status_code != 200:
                    raise Exception(
                        f"Failed to send {self.data_type} data for {document_dict['date']} to Artemis"
                    )

            elif self.data_type == "dfs":
                breakpoint()
                pass

            elif self.data_type == "lineups":
                breakpoint()
                pass

        return "complete"


