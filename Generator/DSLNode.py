import sys, os
from .DSL_GRAPH import graph

class DSLNode:

    def __init__(self, key, parent):
        self.key = key
        self.parent = parent
        self.children = []
        
    def addChild(self, child):
        self.children.append(child)

    def render(self, file, level):
        
        if self.key == 'root':
            for child in self.children:
                child.render(file, level + 1)
            return
        
        file.write(level * '\t')
        # Write end-token then return
        if not len(self.children) and self.key not in list(graph.keys()):
            file.write(self.key + '\n')
            return
        
        if not len(self.children) and self.key in list(graph.keys()):
            return
        
        file.write(self.key + '\n')
        
        file.seek(0, os.SEEK_END)
        file.seek(file.tell() - 2, os.SEEK_SET) # On Ubuntu: file.tell() - 1
        file.write('{\n')
        for child in self.children:
            child.render(file, level + 1)
        file.write(level * '\t' + '}\n')