# Course: CS261 - Data Structures
# Author: Theresa Quach
# Assignment:   #6 Directed Graph Implementation
# Description: Implementation of an directed graph using an adjacency matrix to store the vertices and edges of the graph

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Method that adds a new vertex to the graph, starting from integer index 0 and increasing upward. The method
        returns an integer representing the number of vertices in the graph after the addition.
        """
        self.v_count += 1                                                                                                   # increment number of vertices in matrix
        new_vertex = [0 for x in range(self.v_count)]                                                                       # create new list(row) for new vertex with edges to other vertices in matrix initialized to 0
        self.adj_matrix.append(new_vertex)                                                                                  # add new row to matrix
        for row in range(self.v_count-1):                                                                                   # go to previous rows
            self.adj_matrix[row].append(0)                                                                                  # add another column in each row for new vertex, initialized to 0
        return self.v_count


    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Method that takes as parameters a source vertex, a destination vertex, and a weight (integer) that represents the edge
        between those two vertices, in the direction given. If either (or both) vertices do not exist in the graph, if the weight
        is not a positive integer, or if src and dst are the same vertex, method does nothing.
        If an edge already exists in the graph, the edge is updated with the new weight.

        """

        if src == dst:
            return
        if src > self.v_count-1 or src < 0:                                                                                            # self.v_count-1 for 0-indexing
            return
        if dst > self.v_count-1 or dst < 0:
            return
        if weight < 0:
            return
        self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        Method that takes a source vertex and a destination vertex and removes the edge between them (resets to 0). If either
        the source or destination vertices don't exist, or if there is no edge between them, nothing happens.
        """
        if src > self.v_count-1 or src < 0:
            return
        if dst > self.v_count-1 or dst < 0:
            return
        self.adj_matrix[src][dst] = 0                                                                                       # reset edge to 0 to remove (if no edge exists, still 0)


    def get_vertices(self) -> []:
        """
        Method that returns a list of the vertices in the graph (named by their index number).
        """
        vertices = []
        for vertex in range(self.v_count):
            vertices.append(vertex)
        return vertices


    def get_edges(self) -> []:
        """
        Method that returns a list of edges from the graph. Each edge is represented as a tuple of the source and destination
        vertices, and then the weight of the edge between them. 0 means no edge exists between the two vertices. Order of
        the edges in the list does not matter.
        """
        edges = []
        for src in range(self.v_count):
            for dst in range(self.v_count):
                if self.adj_matrix[src][dst] != 0:
                    edges.append((src, dst, self.adj_matrix[src][dst]))
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Method that takes as a parameter a path (which is a list of vertex indices) and returns True if the vertices sequence
        given represents a valid path in the graph (there is a direct edge leading from one to the next until the last vertex
        in the sequence). An empty path is considered valid. Otherwise, it returns False.
        """
        if not path:                                                                                                        # if path is empty
            return True
        for i in range(len(path)-1):                                                                                        # iterate through path with i as source and i+1 as destination (because using i+1, need to set range as length of path -1)
            if self.adj_matrix[path[i]][path[i+1]] == 0:                                                                               # if there is a 0 (nonexisting) edge between source and destination vertices, return False
                return False
        return True                                                                                                         # if loop exists without returning False, is valid path


    def dfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        pass

    def bfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        pass

    def has_cycle(self):
        """
        TODO: Write this implementation
        """
        pass

    def dijkstra(self, src: int) -> []:
        """
        TODO: Write this implementation
        """
        pass


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
