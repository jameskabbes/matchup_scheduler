from kabbes_matchup_scheduler import BaseSingle, BasePlural
import pandas as pd
import itertools 

class Team( BaseSingle ):

    _ONE_LINE_ATTS = ['type','id']
    col = 'team'

    def __init__( self, Teams, id ):

        BaseSingle.__init__( self )

        self.Teams = Teams
        self.Matchups = Matchups()
        self.id = id
        self.n_games = 0
        self.byes = 0
        self.options = {}

    def load_opponents( self, list_of_opposing_teams ):

        for team in list_of_opposing_teams:
            self.opponents[ team ] = []

    def get_byes( self ):

        byes = 0
        for Matchup in self.Matchups:
            if len(Matchup.Teams) == 1:
                byes += 1
        return byes

    def load_options( self, teams ):

        # find the minimum number of matchups against an opponent
        opp_locale_counts = {} # opposing_team: { 0: 2, 1: 3, 2: 1 }
        locale_counts = {}
        for locale in range( self.Teams.Scheduler.teams_per_matchup ):
            locale_counts[ locale ] = 0

        # init dict
        for team in teams:
            if team != self:
                opp_locale_counts[ team ] = locale_counts.copy()

        # fill in opponent matchups
        for Matchup in self.Matchups:
            for locale in range(len(Matchup.Teams)):
                team = Matchup.Teams.list[ locale ]
                if team != self:
                    self_locale = Matchup.Teams.list.index( self )
                    if team in opp_locale_counts:
                        opp_locale_counts[ team ][ self_locale ] += 1
                    locale_counts[ self_locale ] += 1            

        # find which opponents we have played the least number of times
        opponents_count_matchups = { team:sum(list( opp_locale_counts[team].values() )) for team in teams if team != self }
        min_matchups = min( opponents_count_matchups.values() )

        # find which locale(s) we have played at the least number of times 
        min_locale_freq = min( locale_counts.values() )
        min_locales = set([ locale for locale in locale_counts if locale_counts[locale] == min_locale_freq ])

        options = {}
        for team in opp_locale_counts:
            if opponents_count_matchups[ team ] == min_matchups:
                options[ team ] = min_locales.intersection( set( opp_locale_counts[team].keys() ) )

        self.options = options 

        count = 0
        for team in self.options:
            count += len(self.options[team])
        self.options_count = count

class Teams( BasePlural ):

    Child = Team

    def __init__( self, list_of_Teams=[] ):
        BasePlural.__init__( self )

        for team in list_of_Teams:
            self._add( team )

    def init( self, n: int ):
        
        """generates n number of random teams"""

        for i in range(n):
            new_team = self.make_child( self, i )
            self._add( new_team )

    def get_opposing_teams( self, team ):

        """given a Team instance, return a new Teams instance that doens't contain the Team"""

        teams = self.list.copy()
        del teams[ teams.index( team ) ]
        return Teams( teams )

    def load_options( self ):

        for team in self.list:
            team.load_options( self )

        option_counts = { team:team.options_count for team in self }

        #sort the list from lower to most amount of options
        self.list = list(dict(sorted(option_counts.items(), key=lambda item: item[1])).keys())

class Matchup( BaseSingle ):

    col = 'matchup'
    _ONE_LINE_ATTS = ['string']

    def __init__( self, Matchups, Teams ):

        BaseSingle.__init__( self )
        self.Matchups = Matchups
        self.Teams = Teams
        self.gen_string()

    def gen_string( self ):
        self.string = ' v '.join( [ str(team) for team in self.Teams ] ) 

    def export( self ):

        dict = {}
        for i in range(len(self.Teams)):
            dict[ Team.col + str(i+1) ] = [ self.Teams.list[i].id ]
        
        return pd.DataFrame( dict )

    def log( self ):
        for team in self.Teams:
            team.Matchups._add( self )

    def is_valid( self ) -> bool:

        perms = itertools.permutations( self.Teams.list )
        
        for perm in perms:
            perm_teams = Teams( perm )

            valid = True
            for locale in range(len(perm_teams)):
                team = perm_teams.list[ locale ]
                opposing_teams = perm_teams.get_opposing_teams( team )

                for opposing_team in opposing_teams:
                    
                    #opposing team is not an option for team
                    if opposing_team in team.options:
                        
                        #this current locale doesn't work for team
                        if locale not in team.options[ opposing_team ]:
                            valid = False
                            break
                    else:
                        valid = False
                        break

                #next permutation
                if not valid:
                    break
            
            if valid:
                self.Teams = perm_teams
                self.gen_string()
                return True

        return False


class Matchups( BasePlural ):

    Child = Matchup

    def __init__( self ):
        BasePlural.__init__( self )

    def export( self ):

        dfs = []
        for i in range(len(self)):
            df = self.list[ i ].export()
            df.insert( 0, Matchup.col, i+1)
            dfs.append( df )

        return pd.concat( dfs )

    def schedule( self ):

        self.schedule_byes()
        return self.schedule_matchups()

    def schedule_byes( self ):

        """schedule bye games"""

        if self.Round.Rounds.Scheduler.matchups_per_round != None:
            #schedule matchups until every team has played
            byes_needed = len(self.Teams) % self.Round.Rounds.Scheduler.teams_per_matchup

        else:
            byes_needed = len(self.Teams) - (self.Round.Rounds.Scheduler.teams_per_matchup * self.Rounds.Scheduler.matchups_per_round)

        while byes_needed > 0:
            team_byes = { team:team.get_byes() for team in self.Teams }
            min_byes = min( team_byes.values() )
            min_bye_teams = [ team for team in team_byes if team_byes[team] == min_byes ]

            bye_team = min_bye_teams[0]
            self.Teams._remove( bye_team )

            byes_needed -= 1
            
            new_matchup = self.make_child( self, Teams( [bye_team] ) )
            self._add( new_matchup )
            new_matchup.log()

    def schedule_matchups( self ):

        while len(self.Teams) > 0:

            self.Teams.load_options()            
            found = False
            for team_combination in itertools.combinations( self.Teams.list, self.Round.Rounds.Scheduler.teams_per_matchup ):
                Teams_combination = Teams( team_combination )
                matchup = self.make_child( self, Teams_combination )

                #found a good candidate
                if matchup.is_valid():
                    found = True
                    matchup.log()
                    for team in team_combination:
                        self.Teams._remove( team )

                    self._add( matchup )

                    #stop looking through the combinations
                    break
                else:
                    pass

            if not found:
                return False

        return True