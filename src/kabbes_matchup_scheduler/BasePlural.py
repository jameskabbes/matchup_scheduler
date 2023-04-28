from parent_class import ParentPluralDict

class BasePlural( ParentPluralDict ):

    Child = None

    def __init__( self, scheduler, n ):
        ParentPluralDict.__init__( self )

        self.scheduler = scheduler
        self.n = n
        for i in range(self.n):
            self.make_child( i )

    def make_child( self, n ):
        return self.Child( self, n )

    def add( self, child ):
        self._add( child.n, child )

