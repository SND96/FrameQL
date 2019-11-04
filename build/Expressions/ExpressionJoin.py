from .Expression import Expression

class ExpressionJoin(Expression):
    def __init__(self, children, joinType, onClause):
        self.joinType = joinType
        self.children=children
        self.onClause = onClause

    def evaluate(self,Tuple):
        return Tuple
    
