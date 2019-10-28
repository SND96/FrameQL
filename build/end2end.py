import sys
from antlr4 import *
from frameQLParser import frameQLParser 
from frameQLLexer import frameQLLexer
from frameQLParserListener import frameQLParserListener
from MyListener import MyListener
from Nodes.NodeProjection import NodeProjection
from Nodes.NodeCondition import NodeCondition
from Nodes.NodeCross import NodeCross

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

def convert_query(query):
    new_query=query.split(' FROM')[0]+'\r\nFROM'+query.split('FROM')[1]
    new_query=new_query.split(' WHERE')[0]+'\r\nWHERE'+new_query.split('WHERE')[1]
    new_query=new_query+'\r\n'
    return new_query

def main(argv):
    input_stream = FileStream(argv)
    #query=convert_query('SELECT CLASS , REDNESS FROM TAIPAI WHERE CLASS = \'BUS\' AND REDNESS > 200')
    #input_stream.strdata=query
    lexer = frameQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = frameQLParser(stream)
    tree = parser.root()
    listener = MyListener()
    walker = ParseTreeWalker()
    walker.walk(listener,tree)
    

    ExpressionTree=listener.currentLogicalExpression
    PlanTree=listener.projectionNode
    Data_inp = listener.crossNode
    print(PlanTree.processing())

 
if __name__ == '__main__':
    main('test.txt')

