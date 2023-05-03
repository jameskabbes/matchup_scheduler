from kabbes_matchup_scheduler import BaseSingle

class Team( BaseSingle ):

    _ONE_LINE_ATTS = ['type','id']
    col = 'team'

    def __init__( self, id, Teams ):

        BaseSingle.__init__( self )

        self.id = id
        self.Teams = Teams
        self.byes = 0
        self.n_games = 0
        self.locales = {} #locale: frequency, home team, away team, etc
        self.opponents = {} #opponent: frequency

    def get_options( self ):

        ### returns number of options that would be acceptable 

        return []

    def log_Matchup( self, opposing_teams, locale ):

        if len(opposing_teams) == 0:
            self.byes += 1
        
        else:
            self.n_games += 1

            #locales
            if locale not in self.locales:
                self.locales[locale] = 1
            else:
                self.locales[locale] += 1

            #opponents
            for team in opposing_teams:
                if team.id not in self.opponents:
                    self.opponents[ team.id ] = 1
                else:
                    self.opponents[ team.id ] += 1
