from .Node import Node

class NodeCross(Node):
    def __init__(self,data):
        self.data = data

    def processing(self):
        return self.data
