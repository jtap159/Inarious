from datetime import datetime

from inarious.pipelines.apollo import ApolloMongoGames
from inarious.pipelines.artemis import ArtemisCreate
from inarious.config import settings


years = ["2017", "2018", "2019", "2020", "2021", "2022"]


def _migrate_msf(data_type, year):
    amg = ApolloMongoGames()
    data_by_date = amg.get_msf_data(data=data_type, year=year)
    ac = ArtemisCreate(data_type=data_type)
    for date_data in data_by_date:
        assert ac.send_data(date_data) == 200
    return "Migration Complete"


def _migrate_msf_games():
    for year in years:
        val = _migrate_msf("games", year)
    return f"Games {val}"


def _migrate_msf_player_gamelogs():
    for year in years:
        val = _migrate_msf("player_gamelogs", year)
    return f"Player Gamelogs {val}"


def _migrate_msf_team_gamelogs():
    for year in years:
        val = _migrate_msf("team_gamelogs", year)
    return f"Team Gamelogs {val}"


def _migrate_msf_gamelines():
    for year in years:
        val = _migrate_msf("odds_gamelines", year)
    return f"GameLines {val}"


def _migrate_msf_futures():
    for year in years:
        val = _migrate_msf("odds_futures", year)
    return f"Futures {val}"


def _migrate_msf_player_stats_totals():
    for year in years:
        val = _migrate_msf("player_stats_totals", year)
    return f"Player Stats Totals {val}"


def _migrate_msf_team_stats_totals():
    for year in years:
        val = _migrate_msf("team_stats_totals", year)
    return f"Team Stats Totals {val}"


def _migrate_msf_dfs():
    for year in years:
        val = _migrate_msf("dfs", year)
    return f"DFS {val}"


def _check_artemis_data():
    return "Data safely made it to Artemis"


def run():
    _migrate_msf_games()
    _migrate_msf_player_gamelogs()
    _migrate_msf_team_gamelogs()
    _migrate_msf_gamelines()
    _migrate_msf_futures()
    _migrate_msf_player_stats_totals()
    _migrate_msf_team_stats_totals()
    _migrate_msf_dfs()
