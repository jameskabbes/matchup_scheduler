from kabbes_matchup_scheduler import BasePlural, Matchup
import pandas as pd

class Matchups( BasePlural ):

    Child = Matchup

    def __init__( self, Round ):
        BasePlural.__init__( self )
        self.Round = Round

    def export( self ):

        dfs = []
        for i in range(len(self)):
            df = self.list[ i ].export()
            df.insert( 0, Matchup.col, i+1)
            dfs.append( df )

        df = pd.concat( dfs )
        return df