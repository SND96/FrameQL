from antlr4 import *
if __name__ is not None and "." in __name__:
    from .frameQLParser import frameQLParser
else:
    from frameQLParser import frameQLParser
from frameQLParserListener import frameQLParserListener

from Expressions.ExpressionComparison import ExpressionComparison
from Expressions.ExpressionLogical import ExpressionLogical
from Expressions.ExpressionTuple import ExpressionTuple
from Expressions.ExpressionConstant import ExpressionConstant

from Nodes.NodeCondition import NodeCondition
from Nodes.NodeCross import NodeCross
from Nodes.NodeProjection import NodeProjection
from Expressions.ExpressionArithmetic import ExpressionArithmetic


class MyListener(frameQLParserListener):
    def __init__(self, data):
    
        #Attributes
        self.listAttributes=['CLASS','REDNESS']
        
        #Build the query plan tree
        # self.crossNode=NodeCross(None)
        self.crossNode=NodeCross(data)
        self.conditionNode=NodeCondition(self.crossNode,None)
        self.projectionNode=NodeProjection(self.conditionNode,[0,2])
        self.count = 0
        #Build the expression tree
        self.currentComparisonExpression=None
        self.currentLogicalExpression=None
        self.currentArithmeticExpression=None
    
        
    def enterExpressionAtomPredicate(self, ctx:frameQLParser.ExpressionAtomPredicateContext):
        self.count += 1
        self.listAttributes=['ID', 'CLASS', 'REDNESS']
        
        if(self.currentComparisonExpression!=None):
            if self.currentComparisonExpression.children[0]==None:
                if ctx.getText() in self.listAttributes:
                    self.currentComparisonExpression.children[0]=ExpressionTuple(ctx.getText())
                else:
                    self.currentComparisonExpression.children[0]=ExpressionConstant(ctx.getText())
            elif self.currentComparisonExpression.children[0]!=None and self.currentComparisonExpression.children[1]==None:
                if ctx.getText() in self.listAttributes:
                    self.currentComparisonExpression.children[1]=ExpressionTuple(ctx.getText())
                else:
                    self.currentComparisonExpression.children[1]=ExpressionConstant(ctx.getText())

    def exitExpressionAtomPredicate(self, ctx:frameQLParser.ExpressionAtomPredicateContext):
        self.count += 1
        
       
    def enterMathExpressionAtom(self, ctx:frameQLParser.MathExpressionAtomContext):
        operator = ctx.mathOperator().getText()
        left = ExpressionTuple(ctx.getText().split(operator)[0])
        right = ExpressionConstant(ctx.getText().split(operator)[1])
        
        if(self.currentComparisonExpression!=None):
            if self.currentComparisonExpression.children[0].data == (ctx.getText()):
                self.currentComparisonExpression.children[0] = ExpressionArithmetic([left, right], operator)
            elif self.currentComparisonExpression.children[0] != None and self.currentComparisonExpression.children[1].data==(ctx.getText()):
                self.currentComparisonExpression.children[1] = ExpressionArithmetic([left, right], operator)


    def enterPredicateExpression(self, ctx:frameQLParser.PredicateExpressionContext):
        self.count += 1
        self.currentComparisonExpression=ExpressionComparison([None,None],None)
    
    def exitPredicateExpression(self, ctx:frameQLParser.PredicateExpressionContext):
        self.count += 1
        if self.currentLogicalExpression.children[0]==None:
            self.currentLogicalExpression.children[0]=self.currentComparisonExpression
        elif self.currentLogicalExpression.children[0]!=None and self.currentLogicalExpression.children[1]==None:
            self.currentLogicalExpression.children[1]=self.currentComparisonExpression

    def enterLogicalExpression(self, ctx:frameQLParser.LogicalExpressionContext):
        self.count += 1
        self.currentLogicalExpression=ExpressionLogical([None,None],None)
        print(ctx.getText())

    def exitLogicalExpression(self, ctx:frameQLParser.LogicalExpressionContext):
        self.count += 1
        self.conditionNode.expression=self.currentLogicalExpression
        self.conditionNode.children=self.crossNode

    def enterLogicalOperator(self, ctx:frameQLParser.LogicalOperatorContext):
        self.count += 1
        self.currentLogicalExpression.operator=ctx.getText()

    def enterComparisonOperator(self, ctx:frameQLParser.ComparisonOperatorContext):
        self.count += 1
        self.currentComparisonExpression.operator=ctx.getText()

    # Enter a parse tree produced by frameQLParser#tableName.
    def enterTableName(self, ctx:frameQLParser.TableNameContext):
        self.tableName = ctx.getText()

    def enterFullColumnName(self, ctx:frameQLParser.FullColumnNameContext):
        if '.' in ctx.getText():
            self.tableName = ctx.getText().split('.')[0]
            self.columnName = ctx.getText().split('.')[1]
        else:
            self.columnName = ctx.getText()
        

    def enterInnerJoin(self, ctx:frameQLParser.InnerJoinContext):
        self.currentJoinExpression = ExpressionComparison([None,None], None)

    # Exit a parse tree produced by frameQLParser#innerJoin.
    def exitInnerJoin(self, ctx:frameQLParser.InnerJoinContext):
        self.conditionNode.expression=self.currentComparisonExpression
        self.conditionNode.children=self.crossNode




