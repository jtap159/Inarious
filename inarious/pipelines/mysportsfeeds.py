from typing import Union

import base64
import datetime
import requests

from inarious.pipelines.artemis import ArtemisCreate
from inarious.config import settings


class MySportsFeeds:
    """
    Class to pull MySportsFeeds Public API data

    Args:
        msf_url (`str`): The public API URL for MySportsFeeds.
        data_type (`str`): Choose from:
            (games, player_gamelogs, team_gamelogs, odds_gamelines,
             odds_futures, player_stats_totals, team_stats_totals, dfs, venues)
        pull_date (`str`): in YYYY-MM-DD format.
        season (`str`): Choose from: regular, playoff, pre.
        pull_season (`bool`): If False, pulls date, if True, pulls season data.
    """

    def __init__(
        self,
        msf_url: str,
        data_type: str,
        pull_date: Union[datetime.date, str] = datetime.date.today(),
        season: str = "regular",
        pull_season: bool = False
    ):
        self.msf_url = msf_url
        self.data_type = data_type
        self.pull_date = pull_date
        self.season = season
        self.pull_season = pull_season

    @property
    def date(self):
        return self.pull_date.replace("-", "")

    @property
    def year(self):
        return self.pull_date.split("-")[0]

    @property
    def msf_season_api(self):
        return f"{self.msf_url}/{self.year}-{self.season}"

    @property
    def msf_date_api(self):
        return f"{self.msf_season_api}/date/{self.date}"

    @property
    def pull_date_urls(self):
        return {
            "games": f"{self.msf_date_api}/games.json",
            "player_gamelogs": f"{self.msf_date_api}/player_gamelogs.json",
            "team_gamelogs": f"{self.msf_date_api}/team_gamelogs.json",
            "odds_gamelines": f"{self.msf_date_api}/odds_gamelines.json",
            "odds_futures": f"{self.msf_date_api}/odds_futures.json",
            "player_stats_totals":
            f"{self.msf_date_api}/player_stats_totals.json",
            "team_stats_totals": f"{self.msf_date_api}/team_stats_totals.json",
            "dfs": f"{self.msf_date_api}/dfs.json",
        }

    @property
    def pull_season_urls(self):
        return {
            "games": f"{self.msf_season_api}/games.json",
            "player_stats_totals":
            f"{self.msf_season_api}/player_stats_totals.json",
            "team_stats_totals":
            f"{self.msf_season_api}/team_stats_totals.json",
            "venues": f"{self.msf_season_api}/venues.json",
        }

    @property
    def pull_url(self):
        if self.pull_season:
            return self.pull_season_urls[self.data_type]

        else:
            return self.pull_date_urls[self.data_type]

    def pull_msf_data(self):
        r = requests.get(
            url=self.pull_url,
            params={"fordate": self.date},
            headers={
                "Authorization": "Basic "
                + base64.b64encode(
                    "{api_key}:{password}".format(
                        api_key=settings.MSF_MLB_API_KEY,
                        password="MYSPORTSFEEDS"
                    ).encode("utf-8")
                ).decode("ascii")
            },
        )
        return r.json()

    def get_and_send(self):
        msf_data = self.pull_msf_data()
        ac = ArtemisCreate(data_type=self.data_type)
        status_code = ac.send_data(
            data={"date": self.pull_date, self.data_type: msf_data}
        )
        if status_code != 200:
            raise ValueError("Sending data to mongo failed")

        return status_code
