from typing import Union

import base64
import datetime
import requests

from artemis import ArtemisCreate
from inarious.config import settings


class Contests:
    """
    Class to pull Contests from Local MongoDB

    Args:
        data_type (`str`): One of the endpoints for Contest data
        year (`str`): in YYYY format.
    """

    def __init__(
        self,
        data_type: str,
        year: str,
    ):
        self.data_type = data_type
        self.year = year
        self.artemis = ArtemisCreate(data_type=self.data_type)

    @property
    def apollo_mongodb_api(self):
        return f"{settings.APOLLO_API}/mongodb/{self.data_type}"

    @property
    def collections(self):
        return requests.get(
            url=self.apollo_mongodb_api,
            params={"year": self.year},
        ).json()

    def get_documents(self, collection: str):
        return requests.get(
            url=f"{self.apollo_mongodb_api}",
            params={
                "year": self.year,
                "collection": collection,
            },
        )

    def move_contest_details(self, document: dict):
        _id = document.pop("_id")
        document[_id]["_id"] = _id
        for key in ["entry_fee", "prize_pool", "top_prize", "winning_score", "cash_line"]:
            if key in document[_id]:
                document[_id][key] = float(0) if document[_id][key] is None else document[_id][key]
                if key in ["entry_fee", "prize_pool", "top_prize"] and isinstance(document[_id][key], str):
                    document[_id][key] = float(document[_id][key].replace("$", "").replace(",", ""))
            else:
                document[_id][key] = float(0)

        document[_id]["number_of_games"] = 1 if document[_id]["number_of_games"].lower() == "mode" else document[_id]["number_of_games"]
        document[_id]["total_entries"] = 0 if document[_id]["total_entries"] is None else document[_id]["total_entries"]
        date_time = datetime.datetime.strptime(document[_id]["date_time"], "%Y-%m-%d_%H:%M")
        document[_id]["date"] = str(date_time.date())
        document[_id]["date_time"] = str(date_time)
        del document[_id]["contest_id"]
        document[_id]["sport"] = document[_id].pop("sport#")
        document[_id]["complete"] = True if document[_id]["complete"] == "complete" else False
        document[_id]["contest_id"] = str(_id)
        status_code = self.artemis.send_data(data=document[_id]).status_code
        if status_code != 200:
            raise ValueError("Sending data to mongo failed")

    def move_contest_winning_charts(self, documents: dict):
        _id = documents.pop("_contestId")
        for item in documents["winning_chart"]:
            send_item = dict()
            send_item["_contestId"] = _id
            if "value" in item:
                send_item["prize"] = float(item["value"])
            elif "cash" in item:
                send_item["prize"] = float(item["cash"])
            elif "prize" in item:
                send_item["prize"] = float(item["prize"])
            else:
                try:
                    send_item["prize"] = float(
                        item["tierPayoutDescriptions"]["Cash"].replace("$", "").replace(",", "").replace(" ", "")
                    )
                except KeyError:
                    raise KeyError("No prize found")
            send_item["minFinish"] = int(item["minFinish"])
            send_item["maxFinish"] = int(item["maxFinish"])
            status_code = self.artemis.send_data(data=send_item).status_code
            if status_code != 200:
                raise ValueError("Sending data to mongo failed")

    def move_contest_player_ownership(self, documents: dict):
        try:
            _id = documents.pop("_contestId")
            floats = [
                "actualFpts",
                "actualOwnership",
                "projectedOwnership",
                "projectedFpts",
            ]
            strings = [
                "name",
                "statId",
                "rgPlayerId",
                "siteSlatePlayerId",
                "team",
                "opponent",
                "slatePosition",
            ]
            dicts = ["ecr"]
            ints = ["salary", "teamId", "scheduleId"]
            double_check = ["altName", "dkName"]
            for item in documents["player_ownership"]:
                send_item = dict()
                send_item["_contestId"] = _id
                for key in [
                    "actualFpts",
                    "actualOwnership",
                    "ecr",
                    "projectedOwnership",
                    "projectedFpts",
                    "name",
                    "altName",
                    "dkName",
                    "statId",
                    "rgPlayerId",
                    "team",
                    "scheduleId",
                    "opponent",
                    "teamId",
                    "slatePosition",
                    "salary",
                ]:
                    if key in item and key in floats:
                        send_item[key] = float(
                            item[key]
                        ) if item[key] is not None else None

                    elif key in item and key in strings or key in item and key in dicts:
                        send_item[key] = item[key]

                    elif key in item and key in ints:
                        try:
                            send_item[key] = int(
                                item[key]
                            ) if item[key] is not None else None
                        except ValueError:
                            send_item[key] = None

                    elif key in item and key in double_check:
                        send_item["altName"] = item[key]

                    else:
                        pass

            rt = self.artemis.send_data(data=send_item)
            if rt.status_code != 200:
                breakpoint()
                raise ValueError("Sending data to mongo failed")
        except Exception as e:
            breakpoint()

    def get_and_send(self):
        for collection in self.collections:
            documents = self.get_documents(collection=collection)
            if documents.status_code == 200:
                for document in documents.json():
                    if self.data_type == "contest-details":
                        self.move_contest_details(document=document)

                    elif self.data_type == "contest-winning-charts":
                        document["_contestId"] = collection
                        self.move_contest_winning_charts(documents=document)

                    elif self.data_type == "contest-entries":
                        try:
                            for key in ["_id", "user", "rgUserId", "rgUserName"]:
                                if key in document and key != "lineup":
                                    del document[key]

                            if "lineup" in document and document["lineup"] == '':
                                del document["lineup"]

                            if "prize" in document:
                                document["prize"] = document["prize"]["cash"]
                            else:
                                document["prize"] = float(0)

                            if self.artemis.send_data(data=document).status_code != 200:
                                breakpoint()
                                raise ValueError("Sending data to mongo failed")
                        except:
                            breakpoint()

                    elif self.data_type == "contest-player-ownership":
                        document["_contestId"] = collection
                        self.move_contest_player_ownership(documents=document)
                    else:
                        raise ValueError("Data type not found")

        return "Success"
