from kabbes_matchup_scheduler import BasePlural
from kabbes_matchup_scheduler import Team

class Teams( BasePlural ):

    Child = Team

    def __init__( self, scheduler, n ):
        BasePlural.__init__( self, scheduler, n )





