from kabbes_matchup_scheduler import BasePlural
from kabbes_matchup_scheduler import Venue

class Venues( BasePlural ):

    Child = Venue

    def __init__( self, scheduler, n ):
        BasePlural.__init__( self, scheduler, n )


