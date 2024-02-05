from typing import Union

import requests

from inarious.config import settings


class ApolloDates:

    def get_all_dates(self, year: Union[int, str]):
        r = requests.get(
            url=f"{settings.APOLLO_API}/postgresdb/dates/year",
            params={"year": year}
        )
        return r.json()


class ApolloMongoGames:

    @property
    def pull_date_urls(self):
        return {
            "games": f"{settings.APOLLO_API}/mongodb/games",
            "player_gamelogs": f"{settings.APOLLO_API}/mongodb/gamelogs",
            "team_gamelogs": f"{settings.APOLLO_API}/mongodb/team-gamelogs",
            "odds_gamelines": f"{settings.APOLLO_API}/mongodb/gamelines",
            "odds_futures": f"{settings.APOLLO_API}/mongodb/futures",
            "player_stats_totals": f"{settings.APOLLO_API}/mongodb/player-stats",
            "team_stats_totals": f"{settings.APOLLO_API}/mongodb/team-stats",
            "dfs": f"{settings.APOLLO_API}/mongodb/dfs",
        }

    def get_msf_data(self, data: str, year: Union[int, str]):
        if data in self.pull_date_urls:
            url = self.pull_date_urls[data]
            r = requests.get(
                url=url,
                params={"year": year}
            )
            return r.json()

        raise KeyError(
            f"{data}: Key does not exist in {self.pull_date_urls.keys()}"
        )
