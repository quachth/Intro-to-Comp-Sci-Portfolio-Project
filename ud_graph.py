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
        Method that returns a list of edges in the graph (any order) as a tuple of the two vertices making that edge
        """
        e_list = []
        for vertex in self.adj_list:                                                                                        # for each key in the graph dictionary
            for neighbor in self.adj_list[vertex]:                                                                          # iterate through its edges
                edge = (vertex, neighbor)                                                                                   # create edge tuple
                reverse_edge = (neighbor, vertex)                                                                           # reverse_edge is the same edge with the strings backwards
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



    def bfs(self, v_start=None, v_end=None) -> []:
        """
        Method that takes a start vertex and and end vertex and returns a list of vertices visited during BFS search. Vertices
        are added to the list during the search until either the end vertex is reached, or all vertices have been visited (end
        vertex does not exist within the graph)
        Vertices are picked in alphabetical order.
        """
        v_visited = []
        if v_start not in self.adj_list:
            return v_visited
        v_deque = deque([v_start])                                                                                          # deque to hold current level vertices, initialized with start vertex
        v_visited.append(v_start)                                                                                           # add start vertex to visited list
        self.rec_bfs(v_end, v_visited,v_deque)
        return v_visited



    def rec_bfs(self, end_vertex=None, list_v=None, cur_deque=None):
        """
        Recursive helper method for Breadth-First Search that examines current-level vertices from the current deque passed
        to it and adds direct successor vertices from each vertex examined in a BFS manner
        :param end_vertex: The vertex that signals the end of the BFS search. If none is provided, or if it doesn't exist
                in the graph, the BFS continues until all vertices have been visited
        :param list_v: the list of visited vertices
        :param cur_deque: the deque of vertices to be processed for their direct successors
        :return: list of visited vertices
        """
        # Check if end vertex is already in list
        if end_vertex in list_v:
            return list_v

        # While the v_deque is not empty, pop from the front of the deque -> add successors to s_deque alphabetically -> add successors in s_deque to visited list -> normal append vertices in s_deque to next_deque
        s_deque = deque([])                                                                                                 # deque to add successors of current vertex (and added to visited list)
        next_deque = deque([])                                                                                              # deque with successors that is passed back to method
        while cur_deque:                                                                                                    # goes through all current level vertices
            current = cur_deque.popleft()

            # Add current level vertex's direct successors to s_deque if they've not been visited
            for neighbor in self.adj_list[current]:
                if neighbor not in list_v and neighbor not in cur_deque:
                    if not s_deque:
                        s_deque.append(neighbor)
                    else:
                        i=0
                        deque_len = len(s_deque)
                        while i < deque_len:                                                                                # alphabetizing loop that adds successor vertices into s_deque
                            if neighbor < s_deque[i] and neighbor not in s_deque:
                                s_deque.insert(i, neighbor)
                            i +=1
                        if neighbor not in s_deque:                                                                         # if it reaches here, vertex is later/larger than all other neighbors in deque, so append it to the end
                            s_deque.append(neighbor)

            # For each element in s_deque (current level vertex's direct successors), if not visited yet, add to visited list
            for vertex in s_deque:
                if vertex not in list_v:
                    list_v.append(vertex)
                if vertex == end_vertex:  # if end vertex found, return visited list
                    return list_v

            # Append normally current vertex's direct successors to next_deque(eventually passed back recursively
            for vertex in s_deque:
                next_deque.append(vertex)

        # if deque for successors has vertices, pass it back to method recursively
        if next_deque:
            self.rec_bfs(end_vertex, list_v, next_deque)
        return list_v                                                                                                       # if reached here, while loop for current deque has finished and successor deque is empty.



    def count_connected_components(self) -> int:
        """
        Method that returns the number of connected components in the graph
        """
        unvisited = deque([])                                                                                               # unvisited deque to put all vertices in the graph
        total_v = []                                                                                                        # list to hold all visited vertices up to current point
        component = 0                                                                                                       # variable to hold count of components

        # Add all graph's vertices to deque
        for vertex in self.adj_list:
            unvisited.append(vertex)

        # While the list of vertices in total_v don't match graph (not all vertices have been visited)
        while unvisited:                                                                                                    # while deque is still populated with vertices
            current = unvisited.pop()                                                                                       # pop a vertex into current
            if current not in total_v:                                                                                      # if it hasn't been visited yet, do a dfs on it
                visited = self.dfs(current)
                component +=1
            for vertex in visited:                                                                                          # add all vertices visited from single dfs search to total visited list
                total_v.append(vertex)
        return component                                                                                                    # loop ends when all vertices have been visited


    def has_cycle(self)-> bool:
        """
        Method that returns True if the graph contains at least one cycle, and False otherwise. It uses a recursive helper method
        to do a regular (non-alphabetical) DFS traversal on the graph to check for cycles. This code was written using references
        to the DFS/BFS algorithm in the exploration Working with Graphs and the algorithm from
        https://www.interviewbit.com/tutorial/depth-first-search/ for generic DFS, except it uses boolean values instead of an
        empty set to mark a vertex as visited or not (True or False)
        """
        for vertex in self.adj_list:                                                                                        # checks all vertices

            # Initialize visited dictionary -> each key is vertex, initialized to False (unvisited)
            visited = {vertex: False for vertex in self.adj_list}                                                           # Must be initialized within for loop for each component looked at. Otherwise would retain 'True' value from previous components
            parent = None                                                                                                   # initialize parent variable to None within for loop
            if self.dfs_cycle(vertex, parent, visited) == True:                                                             # if the dfs traversal returns True, cycle is found, so return True
                return True
        return False                                                                                                        # all vertices have been checked without returning True, so no cycle exists (False)


    def dfs_cycle(self, cur_v=None, parent_v = None, list_v = None):
        """
        Recursive helper method that does a regular dfs search on the list while keeping track of the current parent node. Extra condition
        involving neighbor-parent vertices comparison used to detect cycle in graph
        :param cur_v: current vertex being visited (starts at vertex passed by calling method)
        :param parent_v: initially None, becomes current vertex on subsequent recursive call when passing back a neighbor/adjacent vertex
        :param list_v: dictionary of vertices whose values equal True if they've been visited and False if unvisited
        :return: True if a cycle is found (if a neighboring vertex is already visited but the neighbor of the current vertex isn't its parent
        """
        list_v[cur_v] = True                                                                                                # mark the current vertex as having been visited (True)
        for neighbor in self.adj_list[cur_v]:                                                                               # for the neighbors of this current vertex
            if list_v[neighbor] == False:                                                                                   # if the neighbor is unvisited, visit the neighbor recursively (dfs traversal),
                cycle = self.dfs_cycle(neighbor, cur_v, list_v)                                                             # using neighbor as new current vertex, current vertex as parent, and the visited dict
                if cycle == True:
                    return True
            else:
                if neighbor != parent_v:                                                                                    # if the neighbor has been visited, and the neighbor is not the parent of the current vertex, cycle found
                    return True
        return False



   


if __name__ == '__main__':
    pass

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


    #print("\nPDF - method dfs() and bfs() example 1")
    #print("--------------------------------------")
    #edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    #g = UndirectedGraph(edges)
    #test_cases = 'ABCDEGH'
    #for case in test_cases:
    #    print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    #print('-----')
    #for i in range(1, len(test_cases)):
    #    v1, v2 = test_cases[i], test_cases[-1 - i]
    #    print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    #print("\nGradescope Random Values test#1")
    #print("--------------------------------------")
    #edges2 = []
    #test_graph = UndirectedGraph(edges2)
    #print(test_graph.bfs('J'))

    #print("\nGradescope Random Values test#2")
    #print("--------------------------------------")
    #edges3 = ['GB', 'GI', 'BK', 'KF', 'HI', 'HA','HE']
    #test_graph2 = UndirectedGraph(edges3)
    #print(test_graph2.bfs('G'))


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


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
