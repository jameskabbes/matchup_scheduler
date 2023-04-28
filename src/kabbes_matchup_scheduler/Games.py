from kabbes_matchup_scheduler import BasePlural
from kabbes_matchup_scheduler import Game

class Games( BasePlural ):

    Child = Game

    def __init__( self, scheduler, n ):
        BasePlural.__init__( self, scheduler, n )
