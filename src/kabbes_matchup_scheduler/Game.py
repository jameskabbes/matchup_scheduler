from kabbes_matchup_scheduler import BaseSingle

class Game( BaseSingle ):

    def __init__( self, parent, n: int ):
        BaseSingle.__init__( self, parent, n )
