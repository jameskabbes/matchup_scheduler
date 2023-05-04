import dir_ops as do
import os

_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
_src_Dir = _Dir.ascend()                                  #src Dir that is one above
_repo_Dir = _src_Dir.ascend()                    

from .BasePlural import BasePlural
from .BaseSingle import BaseSingle

from .Team import Team, Teams, Matchup, Matchups

from .Round import Round
from .Rounds import Rounds

from .Scheduler import Scheduler
from .Client import Client
