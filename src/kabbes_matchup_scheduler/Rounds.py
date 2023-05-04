from kabbes_matchup_scheduler import BasePlural, Round
import pandas as pd

class Rounds( BasePlural ):

    Child = Round

    def __init__( self ):
        BasePlural.__init__( self )

    def init( self, n: int ):
        
        for i in range(n):
            new_round = self.make_child( self )
            self._add( new_round )

    def matchup_shuffle( self ):
        for Round in self:
            Round.Matchups.shuffle()

    def schedule( self ):
        
        for i in range(len(self)):
            print ()
            print ('---------------------')
            print ('ROUND: ' + str(i))
            print ('---------------------')
            print ()
            self.list[i].schedule()
            self.list[i].print()

    def export( self ):

        dfs = []
        for i in range(len(self)):
            df = self.list[ i ].export()
            df.insert( 0, Round.col, i+1)
            dfs.append( df )

        return pd.concat( dfs )
