import requests  # type: ignore

from inarious.pipelines.artemis import ArtemisCreate
from inarious.config import settings


class DailyFantasyNerd:

    def __init__(self, data_type: str, year: int):
        self.data_type = data_type
        self.year = year
        self.artemis_create = ArtemisCreate(data_type=self.data_type)

    @property
    def apollo_mongodb_api(self):
        return f"{settings.APOLLO_API}/mongodb/{self.data_type}"

    def get_documents(self, year):
        return requests.get(url=f"{self.apollo_mongodb_api}/year/{year}")

    def get_and_send(self):
        docs = self.get_documents(year=self.year)
        documents = docs.json()
        document_dict = {}
        for doc in documents:
            if doc["_id"].split("_", 1)[1] in document_dict:
                document_dict[doc["_id"].split("_", 1)[1]].append(doc)
            else:
                document_dict[doc["_id"].split("_", 1)[1]] = [doc]
        for k, v in document_dict.items():
            if len(v) != 2:
                breakpoint()
            send_doc = {}
            date = k.split("_", 1)[0]
            time = k.split("_", 1)[1]
            data_type_1 = v[0]["file_type"]
            data_type_2 = v[1]["file_type"]
            data_1 = v[0]["data"]
            data_2 = v[1]["data"]
            send_doc["date"] = date
            send_doc["time"] = time
            send_doc[data_type_1.lower()] = data_1
            send_doc[data_type_2.lower()] = data_2
            if self.artemis_create.send_data(data=send_doc).status_code != 200:
                breakpoint()
                raise Exception(
                    f"Failed to send {self.data_type} data for {date} {time} to Artemis"
                )
