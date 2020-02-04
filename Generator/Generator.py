import random
import os

if __package__ is None or __package__ == '':
    from DSL_GRAPH import graph
    from Rules import rules
    from DSLNode import DSLNode
else:
    from .DSL_GRAPH import graph
    from .Rules import rules
    from .DSLNode import DSLNode

MAX_LEVELS = 7
MAX_TOKENS = 45
tokensCount = [0]


def generate(node, level):

    global rules, graph, tokensCount

    if (level > MAX_LEVELS or
        (node.key in list(graph.keys()) and level + 2 > MAX_LEVELS) or
        tokensCount[0] >= MAX_TOKENS):
        return False

    # END-TOKEN
    adjList = graph.get(node.key)
    if adjList is None:
        ''' write in file '''
        return True

    rule = rules.get(node.key)

    if rule.get('inOrder'):
        for element in adjList:
            if random.randrange(0, 3) or element == 'container':
                child = DSLNode(element, node)
                result = generate(child, level+1)
                if result:
                    node.addChild(child)
                    tokensCount[0] += 1
        return True

    if node.key == 'row':
        combination = random.choice(rule.get('combinations'))
        for n in combination:
            div = 'div-'+str(n)
            child = DSLNode(div, node)
            result = generate(child, level+1)
            if result:
                node.addChild(child)
                tokensCount[0] += 1
        return True

    a = rule.get('min')
    b = rule.get('max')
    if b:
        r = random.randrange(a, b+1)
        while r:
            element = random.choice(adjList)
            child = DSLNode(element, node)
            result = generate(child, level+1)
            if result:
                node.addChild(child)
                tokensCount[0] += 1
                r -= 1
            elif level + 1 > MAX_LEVELS or tokensCount[0] >= MAX_TOKENS:
                break
        return True

    return False
