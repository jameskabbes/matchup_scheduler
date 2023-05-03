from parent_class import ParentClass
from kabbes_matchup_scheduler import Teams, Rounds
import py_starter as ps

class Scheduler( ParentClass ):

    _IMP_ATTS = []
    _ONE_LINE_ATTS = []

    DEFAULT_SETTINGS_NODE = "default_settings"

    def __init__( self, **kwargs ):
        ParentClass.__init__( self )

        default_settings = self.cfg.get_node( self.DEFAULT_SETTINGS_NODE ).get_eval_dict()
        dict = ps.merge_dicts( default_settings , kwargs )
        self.set_atts( dict)

        print ('Settings: ')
        print (dict)

    def run( self ):

        self.Teams = Teams( self )
        self.Teams.init_n_teams( self.n_teams )
        self.Rounds = Rounds( self )
        self.Rounds.init_n_rounds( self.n_rounds )

        self.Rounds.schedule()
        self.Rounds.shuffle()
        self.export()

    def export( self, export_path = '' ):

        if export_path == '':
            export_path = self.export_Path.path

        df = self.Rounds.export()
        df.reset_index(inplace=True,drop=True)
        df.to_csv( export_path )
        print (df)
