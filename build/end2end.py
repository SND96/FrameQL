import sys
from antlr4 import *
from frameQLParser import frameQLParser 
from frameQLLexer import frameQLLexer
from frameQLParserListener import frameQLParserListener
from MyListener import MyListener
from Nodes.NodeProjection import NodeProjection
from Nodes.NodeCondition import NodeCondition
from Nodes.NodeCross import NodeCross

from Expressions.ExpressionComparison import ExpressionComparison
from Expressions.ExpressionLogical import ExpressionLogical
from Expressions.ExpressionTuple import ExpressionTuple
from Expressions.ExpressionConstant import ExpressionConstant
from Expressions.ExpressionJoin import ExpressionJoin
from Expressions.ExpressionArithmetic import ExpressionArithmetic

#convert the query so that frameQLLexer can read it


def traverse(tree, rule_names, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        print("{0}TOKEN='{1}'".format("  " * indent, tree.getText()))
    else:
        print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))
        for child in tree.children:

            traverse(child, rule_names, indent + 1)

def main(input):
    input_stream = FileStream(input)
    data=[[0,50,'bus'],[1,100,'car'],[2,50,'van'],[3,150,'bus'],[4,120,'bus'],[5,130,'car'],[6,250,'bus'],[7,70,'van'],[8,110,'bus']]

    lexer = frameQLLexer(input_stream)

    print("Raw SQL Query: ")
    print(input_stream, '\n')

    stream = CommonTokenStream(lexer)
    parser = frameQLParser(stream)
    tree = parser.root()
    listener = MyListener(data)

    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    print("Parse Tree: \n")
    print(tree.toStringTree(recog=parser))
    print('\n')

    ExpressionTree=listener.root
    PlanTree=listener.projectionNode
    Data_inp = listener.crossNode
   

    def traverseExpTree(node, children=[]):

        if hasattr(node, 'children'): 
            if len(node.children) == 0:
                return
            for child in node.children:
                traverseExpTree(child, children)
        if hasattr(node, 'attribute'):
            children.append(ExpressionConstant(node.attribute))
            print(node.attribute, end = ', ')
        elif hasattr(node, 'data'):
            children.append(ExpressionConstant(node.data))
            print(node.data, end = ', ')
        elif hasattr(node, 'operator'):
            if node.operator in ['+', '-', '*', '/']:
                ExpressionArithmetic(children, node.operator)
            elif node.operator in ['AND', 'OR', 'NOT']:
                ExpressionLogical(children, node.operator, node.parent)
            else:
                ExpressionComparison(children, node.operator)
            children = []
            print(node.operator, end = ', ')
        else:
            print(node, end = ', ')


    print("PostFix Traversal of Expression Tree: \n")
    traverseExpTree(ExpressionTree)
    print('\n')
   
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--input', metavar='path', required=True,
                        help='the path to raw input file with SQL Query')
    args = parser.parse_args()
    main(input=args.input)

