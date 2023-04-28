import kabbes_matchup_scheduler
import kabbes_client

class Client( kabbes_matchup_scheduler.Scheduler ):

    _BASE_DICT = {}

    def __init__( self, dict={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( kabbes_matchup_scheduler._Dir, dict=d )
        self.cfg = self.Package.cfg

        kabbes_matchup_scheduler.Scheduler.__init__( self )