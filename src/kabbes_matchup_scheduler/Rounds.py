from kabbes_matchup_scheduler import BasePlural, Round
import pandas as pd

class Rounds( BasePlural ):

    Child = Round

    def __init__( self, Scheduler ):
        BasePlural.__init__( self )
        self.Scheduler = Scheduler

    def init_n_rounds( self, n: int ):
        
        """generates n number of random rounds"""

        for i in range(n):
            new_round = self.make_child( self )
            self._add( new_round )

    def schedule( self ):

        for Round in self:
            Round.schedule()

    def export( self ):

        dfs = []
        for i in range(len(self)):
            df = self.list[ i ].export()
            df.insert( 0, Round.col, i+1)
            dfs.append( df )

        return pd.concat( dfs )
