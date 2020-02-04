from Generator import *
from time import time

SIZE = 10
OUTPUT_PATH = '../Generated-Pages/DSL/'

start = time()
if __name__ == '__main__':
    for i in range(SIZE):
        
        pageNo = str(i).zfill(5)
        file = open(OUTPUT_PATH + 'page_' + pageNo + '.dsl', 'w+')
        
        tree = Node2('root', None)
        generate(tree, 0)
        tree.render(file, -1)
        tokensCount[0] = 0
        
        file.flush()
        file.close()

print(time() - start)