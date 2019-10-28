from .Expression import Expression
from .ExpressionConstant import ExpressionConstant
from .ExpressionTuple import ExpressionTuple

class ExpressionComparison(Expression):
    def __init__(self,children,operator):
        self.operator = operator
        self.children=children

    def evaluate(self,Tuple):
        dataleft=self.children[0].evaluate(Tuple)
        dataright=self.children[1].evaluate(Tuple)

        if(isinstance(self.children[0].value(dataleft), str)):
            leftComparator = self.children[0].value(dataleft).replace('\'','')
        else:
            leftComparator = self.children[0].value(dataleft)
        if(isinstance(self.children[1].value(dataright), str)):
            rightComparator = self.children[1].value(dataright).replace('\'','')
        else:
            rightComparator = self.children[1].value(dataright)
        if self.operator=='=':
            # print(str(self.children[0].value(dataleft)))
            # print(str(self.children[1].value(dataright)))

            if (leftComparator==rightComparator):
                return True
            else:
                return False
        if self.operator=='>':
            # print(self.children[0].value(dataleft))
            if leftComparator > rightComparator:
                return True
            else:
                return False
        if self.operator=='<':
            if leftComparator < rightComparator:
                return True
            else:
                return False
        if self.operator=='!=':
            if leftComparator != rightComparator:
                return True
            else:
                return False
        if self.operator=='<=':
            if leftComparator <= rightComparator:
                return True
            else:
                return False
        if self.operator=='>=':
            if leftComparator >= rightComparator:
                return True
            else:
                return False
        
