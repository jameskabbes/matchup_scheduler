from kabbes_matchup_scheduler import types
from typing import TypedDict, Self, Literal


class OpponentHistory(TypedDict):
    count: int
    locale: dict[types.LocaleIndex, int]


class Team:

    id: types.TeamID
    n_matchups: int
    locale_count: dict[types.LocaleIndex, int]
    opponent_history: dict[types.TeamID, OpponentHistory]

    def __init__(self, id: types.IDType, n_teams: int, teams_per_matchup: int):

        self.id = id

        self.n_matchups = 0

        self.opponent_history = {}
        for i in range(n_teams):
            self.opponent_history[i] = {
                'count': 0,
                'locale': {i: 0 for i in range(teams_per_matchup)}
            }

        self.locale_count = {}
        for i in range(teams_per_matchup):
            self.locale_count[i] = 0

    def add_or_remove_matchup(self, opponents: list[Self], option: Literal['add', 'remove']):

        modifier: int = 0
        if option == 'add':
            modifier = 1
        elif option == 'remove':
            modifier = -1

        self_locale: types.LocaleIndex = len(opponents)

        # 1. Modify self's matchup count
        self.n_matchups += modifier

        # 2. Modify locale count
        self.locale_count[self_locale] += modifier

        # 3. Modify all self/opponent matchup histories
        for opponent_locale in range(len(opponents)):
            opponent_locale: types.LocaleIndex
            opponent = opponents[opponent_locale]

            # modify self history
            self.opponent_history[opponent.id]['count'] += modifier
            self.opponent_history[opponent.id]['locale'][self_locale] += modifier

            # modify opponent history
            opponent.opponent_history[self.id]['count'] += modifier
            opponent.opponent_history[self.id]['locale'][opponent_locale] += modifier

    def add_to_matchup(self, opponents: list[Self]):
        self.add_or_remove_matchup(opponents, 'add')

    def remove_from_matchup(self, opponents: list[Self]):
        self.add_or_remove_matchup(opponents, 'remove')

    def is_valid_matchup(self, opponents: list[Self], constraints: types.ConstraintsConfig):

        self_locale: types.LocaleIndex = len(opponents)

        # 1. check if they are already at their max matchups
        if self.n_matchups == constraints['n_matchups']['max']:
            return False

        # 2. check if they can't play at this locale again
        if self.locale_count[self_locale] == constraints['locale_count']['max']:
            return False

        # 3. check their opponent history
        for opponent_locale in range(len(opponents)):
            opponent_locale: types.LocaleIndex
            opponent = opponents[opponent_locale]

            # for the count
            if self.opponent_history[opponent.id]['count'] == constraints['opponent_history']['count']['max']:
                return False

            # and the locale
            if self.opponent_history[opponent.id]['locale'][self_locale] == constraints['opponent_history']['locale']['max']:
                return False

            if opponent.opponent_history[self.id]['locale'][opponent_locale] == constraints['opponent_history']['locale']['max']:
                return False

        return True

    def is_valid_schedule(self, constraints: types.ConstraintsConfig):

        # 1. make sure we hit min number of matchups
        if self.n_matchups < constraints['n_matchups']['min']:
            return False

        # 2. make sure we hit min number at each locale
        for locale_index in self.locale_count:
            locale_index: types.LocaleIndex

            if self.locale_count[locale_index] < constraints['locale_count']['min']:
                return False

        # 3. check opponent history
        for opponent_id in self.opponent_history:

            opponent_id: types.TeamID
            if self.opponent_history[opponent_id]['count'] < constraints['opponent_history']['count']['min']:
                return False

            for locale_index in self.opponent_history[opponent_id]['locale']:
                if self.opponent_history[opponent_id]['locale'][locale_index] < constraints['opponent_history']['locale']['min']:
                    return False

        return True
