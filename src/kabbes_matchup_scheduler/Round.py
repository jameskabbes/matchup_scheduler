from kabbes_matchup_scheduler import BaseSingle, Matchups, Matchup, Teams
import pandas as pd

class Round( BaseSingle ):

    col = 'round'

    def __init__( self, Rounds ):

        BaseSingle.__init__( self )
        self.Rounds = Rounds
        self.Matchups = Matchups( self )

    def schedule( self ):

        teams = self.Rounds.Scheduler.Teams.get_random_list()

        while len(teams) >= self.Rounds.Scheduler.teams_per_game:
            matchup_Teams = Teams( self.Rounds.Scheduler )
            for i in range(self.Rounds.Scheduler.teams_per_game):
                matchup_Teams._add( teams.pop() )

            new_matchup = self.Matchups.make_child( self, matchup_Teams )
            self.Matchups._add( new_matchup )

        self.Matchups.shuffle()

    def export( self ):
        return self.Matchups.export()

    def print( self ):

        print ('------------')
        self.Matchups.print_imp_atts()
