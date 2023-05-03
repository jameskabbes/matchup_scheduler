from kabbes_matchup_scheduler import BasePlural, Team

class Teams( BasePlural ):

    Child = Team

    def __init__( self, Scheduler, list_of_Teams=[] ):
        BasePlural.__init__( self )
        self.Scheduler = Scheduler

        for team in list_of_Teams:
            self._add( team )

    def init_n_teams( self, n: int ):
        
        """generates n number of random teams"""

        for i in range(n):
            new_team = self.make_child( i, self )
            self._add( new_team )

    def log_Matchup( self ):

        for locale in range(len( self )):
            team = self.list[ locale ] 
            opposing_teams = self.list[:locale] + self.list[locale+1:]

            team.log_Matchup( opposing_teams, locale )
    