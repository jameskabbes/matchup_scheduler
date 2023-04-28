from kabbes_matchup_scheduler import BaseSingle, Games

class Round( BaseSingle ):

    def __init__( self, parent, n: int ):
        BaseSingle.__init__( self, parent, n )
        self.Games = Games( self.parent.scheduler, self.parent.scheduler.n_games )

    def schedule( self ):
        pass
