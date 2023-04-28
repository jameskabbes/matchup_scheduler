from kabbes_matchup_scheduler import BaseSingle

class Team( BaseSingle ):

    def __init__( self, parent, n: int ):
        BaseSingle.__init__( self, parent, n )
