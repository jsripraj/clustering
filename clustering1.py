class Vertex:
    def __init__(self, id) -> None:
        self.id = id
        self.parentIndex = id-1
        self.rank = 0

class Edge:
    def __init__(self, v1, v2, cost) -> None:
        self.v1 = v1
        self.v2 = v2
        self.cost = cost

def createGraph(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        V = [Vertex(i+1) for i in range(n)]
        E = []
        for line in f:
            u, w, cost = [int(x) for x in line.strip().split()]
            E.append(Edge(V[u-1], V[w-1], cost))
    return (V, E)

def printEdges(E):
    for e in E:
        print(f'Node {e.v1.id} <=> Node {e.v2.id} with cost {e.cost}')
    print('\n')

def maxSpacingOfKCluster(G, k):
    V, E = G     
    numOfClusters = len(V) 
    E = sorted(E, key=lambda e: e.cost)
    i = 0
    while numOfClusters > k and i < len(E):
        vrtx1, vrtx2 = E[i].v1, E[i].v2
        if find(V, vrtx1) != find(V, vrtx2):
            union(V, vrtx1, vrtx2)
            numOfClusters -= 1
        i += 1
    """ The spacing of the k cluster is the cost of the next
    edge that crosses clusters. Increment i until that edge
    is found, then return that edge."""
    while find(V, E[i].v1) == find(V, E[i].v2):
        i += 1
    return E[i].cost

def find(V, vertex): # returns union rank index of v's leader
    toUpdate = []
    currentIndex = vertex.id-1
    parentIndex = V[currentIndex].parentIndex
    while True:
        if currentIndex == parentIndex: # element is leader of cluster
            for v in toUpdate: # path compression
                v.parentIndex = currentIndex 
            break
        else:
            toUpdate.append(V[currentIndex])
            currentIndex = parentIndex
            parentIndex = V[currentIndex].parentIndex
    return V[currentIndex]

def union(V, vrt1, vrt2):
    leader1 = find(V, vrt1)
    leader2 = find(V, vrt2)
    if leader1.rank < leader2.rank:
        leader1.parentIndex = leader2.parentIndex
    else:  # leader2.rank <= leader1.rank
        leader2.parentIndex = leader1.parentIndex
        if leader2.rank == leader1.rank:
            leader1.rank += 1
    return

test = 'test1.txt'
full = 'clustering1.txt'
G = createGraph(full)
ans = maxSpacingOfKCluster(G, 4)
print(f'Answer: {ans}')