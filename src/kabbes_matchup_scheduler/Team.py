from kabbes_matchup_scheduler import types
from typing import TypedDict


class OpponentCount(TypedDict):
    count: int
    locale: dict[types.IDType, int]


class Team:

    n_matchups: int
    opponent_count: dict[types.IDType, OpponentCount]
    locale_count: dict[types.IDType, int]

    def __init__(self, n_teams: int, teams_per_matchup: int):

        self.n_matchups = 0

        self.opponent_count = {}
        for i in range(n_teams):
            self.opponent_count[i] = {
                'count': 0,
                'locale': {i: 0 for i in range(teams_per_matchup)}
            }

        self.locale_count = {}
        for i in range(teams_per_matchup):
            self.locale_count[i] = 0

    def log_matchup(self):
        pass

    def is_valid_matchup(self):
        pass
