from kabbes_matchup_scheduler import BaseSingle, Team
import pandas as pd

class Matchup( BaseSingle ):

    col = 'matchup'
    _ONE_LINE_ATTS = ['string']

    def __init__( self, Matchups, Teams ):

        BaseSingle.__init__( self )
        self.Matchups = Matchups
        self.Teams = Teams
        self.Teams.log_Matchup()
        self.string = ' v '.join( [ str(team) for team in self.Teams ] ) 

    def export( self ):

        dict = {}
        for i in range(len(self.Teams)):
            dict[ Team.col + str(i+1) ] = [ self.Teams.list[i].id ]
        
        return pd.DataFrame( dict )

