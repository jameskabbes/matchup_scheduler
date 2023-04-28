from kabbes_matchup_scheduler import BaseSingle

class Venue( BaseSingle ):

    def __init__( self, parent, n: int ):
        BaseSingle.__init__( self, parent, n )
