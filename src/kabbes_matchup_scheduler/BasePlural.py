from parent_class import ParentPluralList
import random

class BasePlural( ParentPluralList ):

    Child = None

    def __init__( self ):
        ParentPluralList.__init__( self )

    def make_child( self, *args, **kwargs ):
        return self.Child( *args, **kwargs )

    def shuffle( self ):
        random.shuffle( self.list )

    def get_random_list( self ):
        self.shuffle()
        return self.list.copy()

