from typing import TypedDict, Union
import pathlib
from dataclasses import dataclass, field
import pandas as pd
from kabbes_matchup_scheduler import team, types
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


class Scheduler:

    config: SchedulerConfig
    schedule: types.ScheduleType
    teams: list[team.Team]
    constraints: types.ConstraintsConfig
    available_team_ids_by_round: list[set[types.IDType]]

    def __init__(self, config: SchedulerConfig = {}, **default_config_overwrite):

        # load config
        self.config = config
        if self.config == {}:
            self.config = DEFAULT_SCHEDULER_CONFIG

        for key in default_config_overwrite:
            self.config[key] = default_config_overwrite[key]

        # fill in None values for matchups per round
        if self.config['matchups_per_round'] == None:
            self.config['matchups_per_round'] = self.config['n_teams'] // self.config['teams_per_matchup']

        # each team can only play at most 1 time
        else:
            self.config['matchups_per_round'] = max(
                self.config['matchups_per_round'], self.config['n_teams'] // self.config['teams_per_matchup'])

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
            self.teams.append(team.Team(i,
                                        self.config['n_teams'], self.config['teams_per_matchup']))

        # load available teams
        self.available_team_ids_by_round: list[set[types.IDType]] = []
        for i in range(self.config['n_rounds']):
            self.available_team_ids_by_round.append(
                set(list(range(self.config['n_teams']))))

        print(self.config)
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

        min_matchups_per_team: int = math.floor(avg_matchups_per_team)
        max_matchups_per_team: int = math.ceil(avg_matchups_per_team)

        # 1.728, each team should play either 1 or 2 games as home/away/other
        min_locales_per_team: int = math.floor(
            min_matchups_per_team / self.config['teams_per_matchup'])
        max_locales_per_team: int = math.ceil(
            max_matchups_per_team / self.config['teams_per_matchup'])

        # 0.857, each team should play either 0 or 1 games against each opponent
        opponent_matchup_frequency = (
            self.config['teams_per_matchup'] - 1) / (self.config['n_teams'] - 1)

        min_matchups_per_opponent: int = math.floor(
            min_matchups_per_team * opponent_matchup_frequency)
        max_matchups_per_opponent: int = math.ceil(
            max_matchups_per_team * opponent_matchup_frequency)

        # 0.285, each team should play either 0 or 1 games against each opponent as home/away/other
        min_locales_per_matchups_per_opponent: int = math.floor(
            min_matchups_per_opponent / self.config['teams_per_matchup'])
        max_locales_per_matchups_per_opponent: int = math.ceil(
            max_matchups_per_opponent / self.config['teams_per_matchup'])

        self.constraints: types.ConstraintsConfig = {
            'n_matchups': {
                'min': min_matchups_per_team,
                'max': max_matchups_per_team,
            },
            'opponent_history': {
                'count': {
                    'min': min_matchups_per_opponent,
                    'max': max_matchups_per_opponent,
                },
                'locale': {
                    'min': min_locales_per_matchups_per_opponent,
                    'max': max_locales_per_matchups_per_opponent,
                },
            },
            'locale_count': {
                'min': min_locales_per_team,
                'max': max_locales_per_team,
            }
        }

    def run(self):

        if self.backtrack(0, 0, 0):
            print('Found a solution!')
            self.print()

        else:
            print('No solution found')

    def process_addition(self, team_id: types.IDType, round_index: int, matchup_index: int, team_index: int):

        self.available_team_ids_by_round[round_index].remove(team_id)
        self.schedule[round_index][matchup_index][team_index] = team_id

        self.teams[team_id].add_to_matchup(
            [self.teams[team_id] for team_id in self.schedule[round_index][matchup_index][:team_index]])

    def process_removal(self, team_id: types.IDType, round_index: int, matchup_index: int, team_index: int):

        self.teams[team_id].remove_from_matchup(
            [self.teams[team_id] for team_id in self.schedule[round_index][matchup_index][:team_index]])

        self.schedule[round_index][matchup_index][team_index] = None
        self.available_team_ids_by_round[round_index].add(team_id)

    def backtrack(self, round_index: int, matchup_index: int, team_index: int):

        if round_index == self.config['n_rounds']:
            return True
        if matchup_index == self.config['matchups_per_round']:
            return self.backtrack(round_index+1, 0, 0)
        if team_index == self.config['teams_per_matchup']:
            return self.backtrack(round_index, matchup_index+1, 0)

        for team_id in self.available_team_ids_by_round[round_index]:

            # if is_valid_move
            if self.teams[team_id].is_valid_matchup([self.teams[team_id] for team_id in self.schedule[round_index][matchup_index][:team_index]], self.constraints):

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

    def print(self):

        for team_id in range(self.config['n_teams']):
            print('Team ', team_id)
            print(self.teams[team_id].n_matchups)
            print(self.teams[team_id].opponent_history)
            print(self.teams[team_id].locale_count)

        for i in range(self.config['n_rounds']):
            self.print_round(i)

    def print_round(self, round):

        print('------------------')
        print('Round ', round+1)
        print('------------------')

        for i in range(self.config['matchups_per_round']):
            print(self.schedule[round][i])
        print()
