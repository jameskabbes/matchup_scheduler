from parent_class import ParentClass
from kabbes_matchup_scheduler import Rounds, Venues, Teams
import py_starter as ps

class Scheduler( ParentClass ):

    _IMP_ATTS = []
    _ONE_LINE_ATTS = []

    DEFAULT_KWARGS = {

        "n_teams": None,
        "n_rounds": None,
        "n_games": None,
        "n_venues": None,
        "n_teams_per_game": 2,
        "max_team_games_per_round": 1

    }

    def __init__( self, **kwargs ):
        ParentClass.__init__( self )

        dict = ps.merge_dicts( self.DEFAULT_KWARGS, kwargs )
        for key in dict:
            if dict[key] == None:
                dict[key] = ps.get_int_input( 1, 999999999, prompt=key+': ', show_range=False )

        print (dict)

        self.set_atts( dict)

        self.Teams = Teams( self, self.n_teams )
        self.Rounds = Rounds( self, self.n_rounds )
        self.Venues = Venues( self, self.n_venues )

    def run( self ):

        self.Teams.print_atts()
        self.Rounds.print_atts()
        self.Venues.print_atts()

        for Round in self.Rounds:
            Round.schedule()




