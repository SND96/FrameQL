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
        self.crossNode=NodeCross(data)
        self.conditionNode=NodeCondition(self.crossNode,None)
        self.projectionNode=NodeProjection(self.conditionNode,[0,2])
        self.count = 0
        self.root=None

        self.currentComparisonExpression=None
        self.currentLogicalExpression=None
        self.currentArithmeticExpression=None
    
    # Enter a parse tree produced by frameQLParser#ExpressionAtomPredicate
    def enterExpressionAtomPredicate(self, ctx:frameQLParser.ExpressionAtomPredicateContext):
        self.count += 1
        self.listAttributes=['ID', 'CLASS', 'REDNESS', 'SPEED']
        
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
    
    # Exit a parse tree produced by frameQLParser#ExpressionAtomPredicate
    def exitExpressionAtomPredicate(self, ctx:frameQLParser.ExpressionAtomPredicateContext):
        self.count += 1
        
    # Enter a parse tree produced by frameQLParser#mathExpression.
    def enterMathExpressionAtom(self, ctx:frameQLParser.MathExpressionAtomContext):
        operator = ctx.mathOperator().getText()
        left = ExpressionTuple(ctx.getText().split(operator)[0])
        right = ExpressionConstant(ctx.getText().split(operator)[1])
        
        if(self.currentComparisonExpression!=None):
            if self.currentComparisonExpression.children[0].data == (ctx.getText()):
                self.currentComparisonExpression.children[0] = ExpressionArithmetic([left, right], operator)
            elif self.currentComparisonExpression.children[0] != None and self.currentComparisonExpression.children[1].data==(ctx.getText()):
                self.currentComparisonExpression.children[1] = ExpressionArithmetic([left, right], operator)

    # Enter a parse tree produced by frameQLParser#predicateExpression.
    def enterPredicateExpression(self, ctx:frameQLParser.PredicateExpressionContext):
        self.count += 1
        self.currentComparisonExpression=ExpressionComparison([None,None],None)

    # Exit a parse tree produced by frameQLParser#predicateExpression.    
    def exitPredicateExpression(self, ctx:frameQLParser.PredicateExpressionContext):
        self.count += 1     
        if self.currentLogicalExpression != None:
            if self.currentLogicalExpression.children[0]==None:
                self.currentLogicalExpression.children[0]=self.currentComparisonExpression
            elif self.currentLogicalExpression.children[0]!=None and self.currentLogicalExpression.children[1]==None:
                self.currentLogicalExpression.children[1]=self.currentComparisonExpression

    # Enter a parse tree produced by frameQLParser#logicalExpression.
    def enterLogicalExpression(self, ctx:frameQLParser.LogicalExpressionContext):
        self.count += 1
        if self.root == None:
            self.currentLogicalExpression=ExpressionLogical([None, None],None, None)
            self.root = self.currentLogicalExpression
        else:
            if self.currentLogicalExpression.children[0]==None:
                self.currentLogicalExpression.children[0]=ExpressionLogical([None, None], None, self.currentLogicalExpression)
                self.currentLogicalExpression = self.currentLogicalExpression.children[0]
            elif self.currentLogicalExpression.children[0]!=None and self.currentLogicalExpression.children[1]==None:
                self.currentLogicalExpression.children[1]=ExpressionLogical([None, None], None, self.currentLogicalExpression)
                self.currentLogicalExpression = self.currentLogicalExpression.children[1]

     # Exit a parse tree produced by frameQLParser#logicalExpression.              
    def exitLogicalExpression(self, ctx:frameQLParser.LogicalExpressionContext):
        self.count += 1
        self.conditionNode.expression=self.currentLogicalExpression
        self.conditionNode.children=self.crossNode
        if self.currentLogicalExpression.children[0]!=None and self.currentLogicalExpression.children[1]!=None:
            self.currentLogicalExpression = self.currentLogicalExpression.parent

    # Enter a parse tree produced by frameQLParser#logicalOperator.
    def enterLogicalOperator(self, ctx:frameQLParser.LogicalOperatorContext):
        self.count += 1
        self.currentLogicalExpression.operator=ctx.getText()

    # Enter a parse tree produced by frameQLParser#comparisonOperator.
    def enterComparisonOperator(self, ctx:frameQLParser.ComparisonOperatorContext):
        self.count += 1
        self.currentComparisonExpression.operator=ctx.getText()
        if self.root == None:
            self.root = self.currentComparisonExpression

    # Enter a parse tree produced by frameQLParser#tableName.
    def enterTableName(self, ctx:frameQLParser.TableNameContext):
        self.tableName = ctx.getText()

    # Enter a parse tree produced by frameQLParser#fullColumnName.
    def enterFullColumnName(self, ctx:frameQLParser.FullColumnNameContext):
        if '.' in ctx.getText():
            self.tableName = ctx.getText().split('.')[0]
            self.columnName = ctx.getText().split('.')[1]
        else:
            self.columnName = ctx.getText()
        
     # Enter a parse tree produced by frameQLParser#innerJoin.
    def enterInnerJoin(self, ctx:frameQLParser.InnerJoinContext):
        self.currentJoinExpression = ExpressionComparison([None,None], None)

    # Exit a parse tree produced by frameQLParser#innerJoin.
    def exitInnerJoin(self, ctx:frameQLParser.InnerJoinContext):
        self.conditionNode.expression=self.currentComparisonExpression
        self.conditionNode.children=self.crossNode




