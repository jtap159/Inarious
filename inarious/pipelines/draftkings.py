import datetime
import pandas as pd  # type: ignore
import re
import requests  # type: ignore

from inarious.pipelines.artemis import ArtemisCreate
from inarious.config import settings


class DraftKings:
    """
    Class to pull DrafKings data and send it to new MongoDB

    Args:
        data_type (`str`): 2022 DraftKings data endpoints (/contests-payout)
    """

    def __init__(
        self,
        data_type: str,
    ):
        self.data_type = data_type
        self.cd_artemis = ArtemisCreate(data_type="contest-details")
        self.ce_artemis = ArtemisCreate(data_type="contest-entries")
        self.cpo_artemis = ArtemisCreate(data_type="contest-player-ownership")
        self.cwc_artemis = ArtemisCreate(data_type="contest-winning-charts")

    @property
    def apollo_mongodb_api(self):
        return f"{settings.APOLLO_API}/mongodb/{self.data_type}"

    @property
    def collections(self):
        return requests.get(url=self.apollo_mongodb_api).json()

    def get_documents(self, collection: str):
        return requests.get(url=f"{self.apollo_mongodb_api}/{collection}")

    def get_contest_file(self, contest_key: str):
        file = str(
            settings.MLB_CONTEST_FILES /
            f"contest-standings-{contest_key}.csv"
        )
        df = pd.read_csv(file)
        df_entries = df[
            [
                "Rank",
                "EntryId",
                "EntryName",
                "TimeRemaining",
                "Points",
                "Lineup",
            ]
        ].copy()
        df_entries = df_entries.dropna(thresh=3)
        df_entries.rename(
            columns={
                "Rank": "rank",
                "EntryId": "siteEntryId",
                "EntryName": "siteScreenName",
                "TimeRemaining": "timeRenaining",
                "Points": "points",
                "Lineup": "lineup",
            },
            inplace=True,
        )
        df_entries["lineup"] = df_entries["lineup"].fillna("null")
        df_entries["userEntryCount"] = df_entries["siteScreenName"].apply(
            lambda string: string.replace(")", "").split("/")[-1]
            if len(string.split("/")) > 1
            else 1
        )
        df_entries["siteScreenName"] = (
            df_entries["siteScreenName"].str.rsplit(" ", n=1).str[0]
        )
        df_player_ownership = df[
            ["Player", "Roster Position", "%Drafted", "FPTS"]
        ].copy()
        df_player_ownership.rename(
            columns={
                "Player": "name",
                "Roster Position": "slatePosition",
                "%Drafted": "actualOwnership",
                "FPTS": "actualFpts",
            },
            inplace=True,
        )
        df_player_ownership["actualOwnership"] = df_player_ownership[
            "actualOwnership"
        ].str.replace("%", "")
        df_player_ownership = df_player_ownership.dropna(thresh=3)
        return df_entries, df_player_ownership

    def get_and_send(self):
        for collection in self.collections:
            documents = self.get_documents(collection=collection)
            if documents.status_code == 200:
                for document in documents.json():
                    contest_details_send = dict()
                    contest_details = document["contestDetail"]
                    if contest_details["sport"] != "MLB":
                        continue
                    contest_details_send["date"] = contest_details[
                        "contestStartTime"
                    ].split("T")[0]
                    contest_details_send["contest_name"] = contest_details["name"]
                    contest_details_send["max_entries"] = contest_details[
                        "maximumEntriesPerUser"
                    ]
                    contest_details_send["entry_fee"] = float(
                        contest_details["entryFee"]
                    )
                    contest_details_send["total_entries"] = contest_details[
                        "maximumEntries"
                    ]
                    contest_details_send["sport"] = 2
                    contest_details_send["date_time"] = str(
                        datetime.datetime.fromisoformat(
                            contest_details["contestStartTime"][:-5] + "+00:00"
                        ).replace(tzinfo=None)
                    )
                    if contest_details["contestState"] == "Completed":
                        contest_details_send["complete"] = True
                    else:
                        contest_details_send["complete"] = False
                    try:
                        if "prizePool" in contest_details:
                            prize_pool = contest_details["prizePool"]
                        elif "PayoutDescription" in contest_details:
                            prize_pool = contest_details["PayoutDescription"]
                        elif (
                            "payoutDescriptions" in contest_details
                            and "Cash" in contest_details
                        ):
                            prize_pool = contest_details["payoutDescriptions"]["Cash"]
                        elif "payoutDescriptionMetadata" in contest_details:
                            prize_pool = contest_details["payoutDescriptionMetadata"][
                                "value"
                            ]
                        prize_pool = float(
                            prize_pool.rsplit(" ", 1)[-1]
                            .replace("$", "")
                            .replace(",", "")
                        )
                        contest_details_send["prize_pool"] = prize_pool
                    except KeyError:
                        prize_pool = contest_details["PayoutDescription"]
                    except ValueError:
                        continue
                    if (
                        "Cash"
                        in contest_details["payoutSummary"][0]["tierPayoutDescriptions"]
                    ):
                        contest_details_send["top_prize"] = float(
                            contest_details["payoutSummary"][0][
                                "tierPayoutDescriptions"
                            ]["Cash"]
                            .replace("$", "")
                            .replace(",", "")
                        )
                    elif (
                        "payoutDescriptions" in contest_details["payoutSummary"][0]
                        and "value"
                        in contest_details["payoutSummary"][0]["payoutDescriptions"]
                    ):
                        contest_details_send["top_prize"] = float(
                            contest_details["payoutSummary"][0]["payoutDescriptions"][
                                0
                            ]["value"]
                        )
                    else:
                        continue
                    contest_key = contest_details["contestKey"]
                    try:
                        contest_details_send["number_of_games"] = requests.get(
                            url=f"{self.apollo_mongodb_api}/{contest_details_send['date']}/{contest_key}"
                        ).json()
                    except requests.exceptions.JSONDecodeError:
                        contest_details_send["number_of_games"] = 1
                    try:
                        df_entries, df_player_ownership = self.get_contest_file(
                            contest_key
                        )
                    except FileNotFoundError:
                        continue
                    df_entries["_contestId"] = str(contest_key)
                    df_player_ownership["_contestId"] = str(contest_key)
                    contest_details_send["_contestId"] = str(contest_key)
                    contest_details_send["winning_score"] = float(
                        df_entries["points"].max()
                    )
                    if (
                        len(df_entries["rank"])
                        >= contest_details["payoutSummary"][-1]["maxPosition"] - 1
                    ):
                        cash_line_index = df_entries["rank"][
                            contest_details["payoutSummary"][-1]["maxPosition"] - 1
                        ]
                    else:
                        cash_line_index = df_entries["rank"][
                            len(df_entries["rank"]) - 1
                        ]
                    contest_details_send["cash_line"] = float(
                        df_entries["points"][cash_line_index]
                    )
                    contest_winning_charts = contest_details["payoutSummary"]
                    if (
                        self.cd_artemis.send_data(contest_details_send).status_code
                        != 200
                    ):
                        raise ValueError(
                            f"Failed to send contest details for {contest_key} in {collection}"
                        )
                    entries = df_entries.to_dict("records")
                    for entry in entries:
                        if entry["lineup"] == "null":
                            del entry["lineup"]
                        else:
                            res = {}
                            match = re.findall(
                                "P | P |OF | OF |3B | 3B |2B | 2B |SS | SS |C | C |1B | 1B",
                                entry["lineup"],
                            )
                            regex = re.split(
                                "P | P |OF | OF |3B | 3B |2B | 2B |SS | SS |C | C |1B | 1B",
                                entry["lineup"],
                            )[1:]
                            for i in range(len(match)):
                                res[i] = {match[i]: regex[i]}
                            entry["lineup"] = res
                        if self.ce_artemis.send_data(entry).status_code != 200:
                            raise ValueError(
                                f"Failed to send contest entries for {contest_key} in {collection}"
                            )
                    player_ownership_docs = df_player_ownership.to_dict("records")
                    for po in player_ownership_docs:
                        if self.cpo_artemis.send_data(po).status_code != 200:
                            raise ValueError(
                                f"Failed to send contest player ownership for {contest_key} in {collection}"
                            )
                    for chart in contest_winning_charts:
                        if "Cash" in chart["tierPayoutDescriptions"]:
                            chart["prize"] = float(
                                chart["tierPayoutDescriptions"]["Cash"]
                                .replace("$", "")
                                .replace(",", "")
                            )
                        else:
                            try:
                                chart["prize"] = float(
                                    chart["payoutDescriptions"][0]["value"]
                                )
                                del chart["payoutDescriptions"]
                            except KeyError:
                                chart["prize"] = 0
                        chart["_contestId"] = contest_key
                        if "tierPayoutDescriptions" in chart:
                            del chart["tierPayoutDescriptions"]
                        if "minFinish" not in chart:
                            chart["minFinish"] = chart.pop("minPosition")
                        if "maxFinish" not in chart:
                            chart["maxFinish"] = chart.pop("maxPosition")
                        if self.cwc_artemis.send_data(data=chart).status_code != 200:
                            raise Exception(
                                f"Failed to send {chart} for {contest_key} in {collection}"
                            )

        return "Success"
