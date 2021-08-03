# Course: CS261 - Data Structures
# Author: Theresa Quach
# Assignment: Undirected Graph Implementation
# Description: Implementation of an undirected graph using an adjacency list to store the vertices and edges of the graph

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Method takes a vertex (string) and adds it to the graph. If a vertex with the same name is already in the graph,
        nothing is added.
        """
        if v not in self.adj_list:
            self.adj_list[v] = []


    def add_edge(self, u: str, v: str) -> None:
        """
        Method takes two vertices and adds the edge connecting the two vertices to the graph. If one or both vertices are not in
        the graph already, method will create the vertex and then create the edge between them. If u and v refer to the same vertex,
        or if the edge already exists in the graph, nothing is added.
        """
        if u == v:
            return
        if u not in self.adj_list:                                                                                          # Adding edge/direct neighbor to key 'u'
            self.adj_list[u] = [v]                                                                                          # if u doesn't exist, create it and add edge
        else:
            if v not in self.adj_list[u]:                                                                                   # if u exists, add edge to preexisting neighbor list
                self.adj_list[u].append(v)
        if v not in self.adj_list:                                                                                          # Adding edge/direct neighbor to key 'v'
            self.adj_list[v] = [u]                                                                                          # if v doesn't exist, create it and add edge
        else:
            if u not in self.adj_list[v]:                                                                                   # if v exists, add edge by appending to preexisting list
                self.adj_list[v].append(u)


    def remove_edge(self, v: str, u: str) -> None:
        """
        Method that takes two vertices and removes the edge between them. If one or both vertices don't exist with in the graph,
        or if the edge between them doesn't exist, method does nothing.
        """
        if v == u:                                                                                                          # if vertices are the same (no loops) = do nothing
            return
        if v not in self.adj_list:                                                                                          # Check if vertices passed exist in graph; if vertex v isn't in the graph, do nothing
            return
        if u not in self.adj_list:                                                                                          # if vertex u isn't in the graph, do nothing
            return
        if u in self.adj_list[v]:                                                                                           # If here, both vertices exist -> check each vertex and remove edge from both
            self.adj_list[v].remove(u)                                                                                      # if there is an edge to u in v, remove it
        if v in self.adj_list[u]:                                                                                           # if there is an edge to v in u, remove it
            self.adj_list[u].remove(v)


    def remove_vertex(self, v: str) -> None:
        """
        Method takes a vertex and removes that vertex and all connected edges from the graph.
        """
        if v not in self.adj_list:
            return
        self.adj_list.pop(v)                                                                                                # Delete key 'v' and its associated value (list of neighbors/edges) from the graph
        for key in self.adj_list:                                                                                           # Iterate through rest of dictionary -> if 'v' is found as a neighbor/edge to other vertices, delete it
            if v in self.adj_list[key]:
                self.adj_list[key].remove(v)
        

    def get_vertices(self) -> []:
        """
        Method that returns a list of vertices in the graph (any order)
        """
        v_list = []
        for key in self.adj_list:
            v_list.append(key)
        return v_list
       

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        e_list = []
        for vertex in self.adj_list:                                                                                        # for each key in the graph dictionary
            for neighbor in self.adj_list[vertex]:                                                                          # iterate through its edges
                edge = vertex + neighbor                                                                                    # concatenate key string and value string to get edge name
                reverse_edge = neighbor + vertex                                                                            # reverse_edge is the same edge with the strings backwards
                if edge not in e_list and reverse_edge not in e_list:                                                       # if neither has been added to the edge list, add it
                    e_list.append(edge)
        return e_list
        

    def is_valid_path(self, path: []) -> bool:
        """
        Method that takes as a parameter a list of vertex names (which represents a path) and returns true if the provided
        path is valid. Otherwise, it returns False
        """
        if path == []:                                                                                                      # Empty path returns true
            return True
        for vertex in path:                                                                                                 # Check that all vertices in path given are in the graph. If not, return False
            if vertex not in self.adj_list:
                return False
        for index in range(len(path)-1):                                                                                    # Starting from the first vertex in path, see if there is an edge between it and the next vertex in the path. If not, return False
            vertex = path[index]                                                                                            # first vertex will be first string in path
            neighbor = path[index+1]                                                                                        # neighboring vertex to check is the following string in path
            if neighbor not in self.adj_list[vertex]:                                                                       # if the neighbor isn't in the list of neighbors/edges of the vertex being examined, return false
                return False
            index += 1                                                                                                      # else, keep iterating through path
        return True                                                                                                         # if this reached, there is an edge between all vertices in the given path -> is valid returns True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Method that takes a starting vertex and an ending vertex and performs a depth-first search of the graph via a recursive
        helper method that adds vertices to be visited to the deque, and visited vertices to the list to be returned.
        Vertices to traverse are picked in alphabetical order. If the starting vertex is not in the graph, an empty list is returned.
        If the ending vertex is not in the graph, the search continues as if there was no end vertex (until all vertices are visited).
        """
        v_visited = []
        if v_start not in self.adj_list:
            return v_visited
        self.rec_dfs(v_start, v_end, v_visited)
        return v_visited


    def rec_dfs(self, vertex=None, end_vertex=None, list_v=None):
        """
        Recursive helper method that takes as parameters the vertex to be added to the list of visited vertices, the provided end vertex, and the list of visited vertices.
        A new deque is created and alphabetized for each set of neighbors (to keep separate from previous/future vertices' neighbor).
        Neighbors are added to the deque only if they have not been previously visited (in visit list).
        Each neighbor in the created deque is popped into a variable and recursively passed back to the function and the process is repeated until all deques are
            empty/visitable vertices are all added to the list, or until the end vertex is hit.
        """
        # Append the new vertex to list of vertices visited
        if vertex not in list_v:
            list_v.append(vertex)

        # Return conditions without visiting additional vertices
        if vertex == end_vertex:
            return list_v

        # Add neighbors of current vertex to a new deque to visit (in alphabetical order)
        v_deque = deque([])
        for neighbor in self.adj_list[vertex]:                                                                              # for a vertex's neighbors
            if neighbor not in list_v:                                                                                      # if the neighbor hasn't already been visited (in visited list)
                if not v_deque:                                                                                             # if deque is empty, append first neighbor found
                    v_deque.append(neighbor)
                else:                                                                                                       # if a neighbor already in the deque
                    i = 0
                    deque_len = len(v_deque)
                    while i < deque_len:                                                                                    # Alphabetizing-while loop
                        if neighbor < v_deque[i] and neighbor not in v_deque:                                               # go through deque to alphabetize neighbors (i.e. if current neighbor is less than/earlier than neighbor in deque, insert it before the deque-neighbor
                            v_deque.insert(i, neighbor)
                        i += 1
                    if neighbor not in v_deque:                                                                             # if it reaches here, it's later/larger than all other neighbors in deque, so append it to the end
                        v_deque.append(neighbor)

        # Recursion to set next visited vertex as first neighbor in deque
        while v_deque:                                                                                                      # while current deque of neighbors is not empty,
            if end_vertex in list_v:
                return list_v
            current = v_deque.popleft()                                                                                     # pop out first(leftmost) neighbor to be visited next
            self.rec_dfs(current, end_vertex, list_v )

        return list_v


       

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
      

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
       

   


if __name__ == '__main__':

    #print("\nPDF - method add_vertex() / add_edge example 1")
    #print("----------------------------------------------")
    #g = UndirectedGraph()
    #print(g)

    #for v in 'ABCDE':
    #    g.add_vertex(v)
    #print(g)

    #g.add_vertex('A')
    #print(g)

    #for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #    g.add_edge(u, v)
    #print(g)


    #print("\nPDF - method remove_edge() / remove_vertex example 1")
    #print("----------------------------------------------------")
    #g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    #g.remove_vertex('DOES NOT EXIST')
    #g.remove_edge('A', 'B')
    #g.remove_edge('X', 'B')
    #print(g)
    #g.remove_vertex('D')
    #print(g)


    #print("\nPDF - method get_vertices() / get_edges() example 1")
    #print("---------------------------------------------------")
    #g = UndirectedGraph()
    #print(g.get_edges(), g.get_vertices(), sep='\n')
    #g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    #print(g.get_edges(), g.get_vertices(), sep='\n')


    #print("\nPDF - method is_valid_path() example 1")
    #print("--------------------------------------")
    #g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    #test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    #for path in test_cases:
    #    print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    #print("\nPDF - method count_connected_components() example 1")
    #print("---------------------------------------------------")
    #edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    #g = UndirectedGraph(edges)
    #test_cases = (
    #    'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #    'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #    'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #    'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    #for case in test_cases:
    #    command, edge = case.split()
    #    u, v = edge
    #    g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #    print(g.count_connected_components(), end=' ')
    #print()


    #print("\nPDF - method has_cycle() example 1")
    #print("----------------------------------")
    #edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    #g = UndirectedGraph(edges)
    #test_cases = (
    #    'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #    'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #    'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #    'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
    #    'add FG', 'remove GE')
    #for case in test_cases:
    #    command, edge = case.split()
    #    u, v = edge
    #    g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #    print('{:<10}'.format(case), g.has_cycle())
