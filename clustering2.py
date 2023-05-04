class Node:
    def __init__(self, leader) -> None:
        self.leader = leader # integer value of bits
        self.rank = 0 

def createGraphDict(filename):
    with open (filename, 'r') as f:
        # k: # clusters, b: # bits
        k,b = [int(s) for s in f.readline().strip().split()]
        graph = {}
        for line in f:
            bitKey = int(''.join(line.strip().split()), 2)
            if bitKey in graph:
                k -= 1
            else:
                graph[bitKey] = Node(bitKey)
    return (graph, k, b)

def createXors(b):
    xors = []
    xors.append(0)
    for i in range(b):
        x = 1 << i
        xors.append(x)
        for j in range(i+1,b):
            y = 1 << j
            xors.append(x^y)
    return xors

def printBinary(nums):
    for num in nums:
        print(f'{num:024b}')

def clustering(G):
    graph, k, b = G
    xors = createXors(b)
    for node in graph: # node is the integer key
        for x in xors:
            other = node^x
            if other in graph and find(graph, node) != find(graph, other):
                union(graph, node, other)
                k -= 1
    return k

def find(graph, node):
    update = []
    while True:
        leader = graph[node].leader
        if node == leader:
            for u in update:
                graph[u].leader = node
            break
        else:
            update.append(node)
            node = leader
    return leader

def union(graph, node1, node2):
    leader1 = find(graph, node1)
    leader2 = find(graph, node2)
    if graph[leader1].rank < graph[leader2].rank:
        graph[leader1].leader = leader2
    else:
        if graph[leader1].rank == graph[leader2].rank:
            graph[leader1].rank += 1
        graph[leader2].leader = leader1
    return

testFile = 'test2.txt'
fullInput = 'clustering_big.txt'
G = createGraphDict(fullInput)
k = clustering(G)
print(f'Need a maximum of {k} clusters for spacing to be at least 3.')