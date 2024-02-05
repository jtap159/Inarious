from typing import Dict

import requests

from inarious.config import settings


class ArtemisCreate:

    def __init__(self, data_type: str):
        self.data_type = data_type

    @property
    def endpoint(self):
        return self.endpoints[self.data_type]

    @property
    def endpoints(self):
        return {
            "games": f"{settings.ARTEMIS_API}/games",
            "player_gamelogs": f"{settings.ARTEMIS_API}/gamelogs",
            "team_gamelogs": f"{settings.ARTEMIS_API}/team-gamelogs",
            "odds_gamelines": f"{settings.ARTEMIS_API}/gamelines",
            "odds_futures": f"{settings.ARTEMIS_API}/futures",
            "player_stats_totals": f"{settings.ARTEMIS_API}/player-stats-totals",
            "team_stats_totals": f"{settings.ARTEMIS_API}/team-stats-totals",
            "dfs": f"{settings.ARTEMIS_API}/dfs",
            "contest-details": f"{settings.ARTEMIS_API}/contest-details",
            "contest-entries": f"{settings.ARTEMIS_API}/contest-entries",
            "contest-player-ownership": f"{settings.ARTEMIS_API}/contest-player-ownership",
            "contest-winning-charts": f"{settings.ARTEMIS_API}/contest-winning-charts",
            "dfn-export-files": f"{settings.ARTEMIS_API}/dfn-export-files",
            "msf-live-games": f"{settings.ARTEMIS_API}/msf-live-games",
        }

    def send_data(self, data: Dict):
        return requests.post(url=self.endpoint, json=data)
