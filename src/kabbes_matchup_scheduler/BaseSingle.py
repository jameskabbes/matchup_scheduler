from parent_class import ParentClass

class BaseSingle( ParentClass ):

    _IMP_ATTS = ['n']
    _ONE_LINE_ATTS = ['type','n']

    def __init__( self, parent, n: int ):

        ParentClass.__init__( self )
        self.parent = parent
        self.n = n

    def __str__( self ):
        return str(self.type).lower() + '_' + str(self.n)
