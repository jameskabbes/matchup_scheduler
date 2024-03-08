from typing import TypedDict, Union
import pathlib
from dataclasses import dataclass, field
import pandas as pd
from kabbes_matchup_scheduler import types, Team
import math


class SchedulerConfig(TypedDict):
    n_teams: int
    n_rounds: int
    teams_per_matchup: int
    matchups_per_round: Union[int, None]
    round_schedule_attempts: int
    shuffle: bool
    export_Path: Union[pathlib.Path, None]


DEFAULT_SCHEDULER_CONFIG: SchedulerConfig = {
    'n_teams': 8,
    'n_rounds': 7,
    'teams_per_matchup': 2,
    'matchups_per_round': None,
    'shuffle': True,
    'export_Path': pathlib.Path('schedule.csv')
}

ConstraintConfig = TypedDict('ConstraintConfig', {
    'min': int,
    'max': int
})

OpponentCountConfig = TypedDict('OpponentCountConfig', {
    'count': ConstraintConfig,
    'locale': ConstraintConfig
})


class ConstraintsConfig(TypedDict):
    n_matchups: ConstraintConfig
    opponent_count: OpponentCountConfig
    locale_count: ConstraintConfig


class Scheduler:

    config: SchedulerConfig
    schedule: types.ScheduleType
    teams: list[Team.Team]

    def __init__(self, config: SchedulerConfig = {}, **default_config_overwrite):

        if config == {}:
            config = DEFAULT_SCHEDULER_CONFIG

        for key in default_config_overwrite:
            config[key] = default_config_overwrite[key]

        self.config = config

        # fill in None values for matchups per round
        if self.config['matchups_per_round'] == None:
            self.config['matchups_per_round'] = self.config['n_teams'] // self.config['teams_per_matchup']

        # load schedule with empty matchups
        self.schedule: types.Schedule = []
        for round_num in range(self.config['n_rounds']):
            round = []
            for matchup_num in range(self.config['matchups_per_round']):
                matchup = [None,]*self.config['teams_per_matchup']
                round.append(matchup)
            self.schedule.append(round)

        # load teams
        self.teams = []
        for i in range(self.config['n_teams']):
            self.teams.append(Team.Team(
                self.config['n_teams'], self.config['teams_per_matchup']))

        self.load_constraints()
        print(self.constraints)

    def load_constraints(self):

        # 6 rounds, 7 teams, 3 teams per matchup, 2 matchups per round

        # 12 matchups
        total_matchups: int = self.config['n_rounds'] * \
            self.config['matchups_per_round']

        # 36 matchups*teams
        total_matchups_times_teams: int = total_matchups * \
            self.config['teams_per_matchup']

        # 6 byes
        n_byes: int = self.config['n_teams'] * \
            self.config['n_rounds'] - total_matchups_times_teams

        # 5.1428, each team should play either 5 or 6 games
        avg_matchups_per_team: float = self.config['n_rounds'] - \
            (n_byes/self.config['n_teams'])

        # 1.728, each team should play either 1 or 2 games as home/away/etc
        avg_locales_per_team: float = avg_matchups_per_team / \
            self.config['teams_per_matchup']

        # 0.857, each team should play either 0 or 1 games against each opponent
        avg_matchups_per_opponent: float = avg_matchups_per_team / \
            (self.config['n_teams'] - 1)

        # 0.428, each team should play either 0 or 1 games against each opponent as home/away/etc
        avg_locales_per_matchups_per_opponent: float = avg_matchups_per_opponent / \
            self.config['teams_per_matchup']

        self.constraints: ConstraintsConfig = {
            'n_matchups': {
                'min': math.floor(avg_matchups_per_team),
                'max': math.ceil(avg_matchups_per_team),
            },
            'opponent_count': {
                'count': {
                    'min': math.floor(avg_matchups_per_opponent),
                    'max': math.ceil(avg_matchups_per_opponent),
                },
                'locale': {
                    'min': math.floor(avg_locales_per_matchups_per_opponent),
                    'max': math.ceil(avg_locales_per_matchups_per_opponent),
                },
            },
            'locale_count': {
                'min': math.floor(avg_locales_per_team),
                'max': math.ceil(avg_locales_per_team),
            }
        }

    def run(self):

        self.available_team_ids_by_round: list[set[types.IDType]] = []
        for i in range(len(self.rounds.n)):
            self.available_team_ids_by_round.append(
                set(self.teams.get_ids_list()))

        if self.backtrack(0, 0, 0):
            print('Found a solution!')
            print(self.schedule)
        else:
            print('No solution found')

    def is_valid_matchup_add(self, team_id, round_index, matchup_index, team_index):

        team = self.teams[team_id]

        # make sure they haven't played too many games
        if team.n_matchups > self.constraints['n_matchups']['max']:
            return False

        # make sure they haven't played these teams too many times
        for team_index_before in range(team_index):
            other_team = self.teams[self.schedule[round_index]
                                    [matchup_index][team_index_before]]

        return True

    def backtrack(self, round_index, matchup_index, team_index):

        if round_index == self.rounds.n:
            return True
        if matchup_index == self.config['matchups_per_round']:
            return self.backtrack(round_index+1, 0, 0)
        if team_index == self.config['n_teams']:
            return self.backtrack(round_index, matchup_index+1, 0)

        for team_id in self.available_teams_by_round[round_index]:

            # if is_valid_move
            if self.is_valid_matchup_add(team_id, round_index, matchup_index, team_index):

                # add to matchup
                self.process_addition(
                    team_id, round_index, matchup_index, team_index)

                # proceed down this branch, it is works return true
                if self.backtrack(round_index, matchup_index, team_index+1):
                    return True

                # this branch is a dead end, try other teams in the for loop
                self.process_removal(team_id, round_index,
                                     matchup_index, team_index)

        # none of the remaining teams can be placed there
        return False
