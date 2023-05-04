from kabbes_matchup_scheduler import BaseSingle, Matchups, Teams

class Round( BaseSingle ):

    col = 'round'

    def __init__( self, Rounds ):

        BaseSingle.__init__( self )
        self.Rounds = Rounds
        self.Teams = Teams( self.Rounds.Scheduler.Teams.list )
        self.Matchups = Matchups()
        self.Matchups.Round = self

    def schedule( self ):
        
        self.Matchups.Teams = Teams( self.Teams.list )
        for i in range( self.Rounds.Scheduler.round_schedule_attempts ):

            if self.Matchups.schedule():
                return
            
            #Refresh Matchups and Teams
            self.Matchups.Teams = Teams( self.Teams.list )
            self.Matchups.shuffle()
            self.Matchups.list = []

        print ('ERROR: Max scheduling attempts reached')        

    def export( self ):
        return self.Matchups.export()

    def print( self ):

        print ('------------')
        self.Matchups.print_imp_atts()
