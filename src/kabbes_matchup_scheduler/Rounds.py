from kabbes_matchup_scheduler import BasePlural
from kabbes_matchup_scheduler import Round

class Rounds( BasePlural ):

    Child = Round

    def __init__( self, scheduler, n ):
        BasePlural.__init__( self, scheduler, n )
