# Course: CS261 - Data Structures
# Author: Theresa Quach
# Assignment:   #6 Directed Graph Implementation
# Description: Implementation of an directed graph using an adjacency matrix to store the vertices and edges of the graph

from collections import deque
import heapq

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
        Method that takes a starting vertex index and an ending vertex index and an ending vertex and returns a list of
        vertices visited during a recursive depth-first search of the graph. If the search encounters the ending vertex, or if all of
        the vertices have been visited, the search will stop. Search proceeds by picking the next ascending value vertex.
        """
        visited = []
        if v_start < 0 or v_start > self.v_count-1:
            return visited
        self.rec_dfs(v_start, v_end, visited)
        return visited


    def rec_dfs(self, cur_v=None, end_v=None, list_v=None):
        """
        Recursive helper method for depth-first search of the adjacency matrix graph. Takes as parameters a current vertex,
        the end vertex originally passed, and a list of already-visited vertices.
        :param cur_v: current vertex being visited
        :param end_v: ending vertex
        :param list_v: list of currently visited vertices
        :return: list of total visited vertices from DFS
        """

        # Append the new vertex to list of vertices visited
        if cur_v not in list_v:
            list_v.append(cur_v)

        # Return conditions without visiting additional vertices
        if cur_v == end_v:
            return list_v

        # Add neighbors of current vertex to a new deque to visit (in ascending order)
        v_deque = deque([])
        for neighbor in range(self.v_count):                                                                                # for a vertex's neighbors
            if self.adj_matrix[cur_v][neighbor] != 0 and neighbor not in list_v:                                                   # neighbor!=0 -> to be an actual neighbor, and not already visited
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
            if end_v in list_v:
                return list_v
            current = v_deque.popleft()                                                                                     # pop out first(leftmost) neighbor to be visited next
            self.rec_dfs(current, end_v, list_v )

        return list_v


    def bfs(self, v_start, v_end=None) -> []:
        """
        Method that takes a starting vertex and ending vertex, and returns a list of vertices visited in the graph after
        a breadth-first search traversal of the graph. Uses a recursive helper method to perform the breadth-first search
        of the graph.
        """
        visited = []
        if v_start <0 or v_start>self.v_count-1:
            return visited
        v_deque = deque([v_start])                                                                                          # deque to hold current level vertices, initialized with start vertex
        visited.append(v_start)                                                                                             # add start vertex to visited list
        self.rec_bfs(v_end, visited, v_deque)
        return visited


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

        # While the v_deque is not empty, pop from the front of the deque -> add successors to s_deque numerically ascending -> add successors in s_deque to visited list -> normal append vertices in s_deque to next_deque
        s_deque = deque([])                                                                                                 # deque to add successors of current vertex (and added to visited list)
        next_deque = deque([])                                                                                              # deque with successors that is passed back to method
        while cur_deque:                                                                                                    # goes through all current level vertices
            current = cur_deque.popleft()

            # Add current level vertex's direct successors to s_deque if they've not been visited
            for neighbor in range(self.v_count):
                if self.adj_matrix[current][neighbor] != 0 and neighbor not in list_v and neighbor not in cur_deque:        # if next index shares an edge with current vertex(actually a neighbor), and not already visited or on current level to be visited
                    if not s_deque:
                        s_deque.append(neighbor)
                    else:
                        i=0
                        deque_len = len(s_deque)
                        while i < deque_len:                                                                                # ordering loop that adds successor vertices into s_deque in ascending order
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


    def has_cycle(self)-> bool:
        """
        Method that returns True if the graph contains at least one cycle, and False otherwise. It uses a recursive helper method
        to do a regular DFS traversal on the graph to check for cycles. Code for detecting cycle in directed graph is modified version
        of undirected graph (with modifications to include adjacency matrix and removal or parent vertex tracker
        """
        for vertex in range(len(self.adj_matrix)):                                                                          # checks all vertices

            # Initialize visited dictionary -> each key is vertex, initialized to False (unvisited)
            visited = {vertex: False for vertex in range(len(self.adj_matrix))}                                             # Must be initialized within for loop for each component looked at. Otherwise would retain 'True' value from previous components
            if self.dfs_cycle(vertex, visited) == True:                                                                     # if the dfs traversal returns True, cycle is found, so return True
                return True
        return False                                                                                                        # all vertices have been checked without returning True, so no cycle exists (False)


    def dfs_cycle(self, cur_v=None, list_v = None):
        """
        Recursive helper method that does a regular dfs search on the list. No need to keep track of parent vertex as if there is a
        directed edge from child back to parent, that is considered a loop.
        :param cur_v: current vertex being visited (starts at vertex passed by calling method)
        :param list_v: dictionary of vertices whose values equal True if they've been visited and False if unvisited; a vertex
                resets to false during call if path has to be rewound (to try a different directed path)
        :return: True if a cycle is found (if a neighboring vertex is already visited but the neighbor of the current vertex isn't its parent
        """
        list_v[cur_v] = True                                                                                                # mark the current vertex as having been visited (True)
        for neighbor in range(len(self.adj_matrix[cur_v])):
            if self.adj_matrix[cur_v][neighbor] != 0 and list_v[neighbor] == False:                                         # if the neighbor is an actual neighbor (edge weight not 0) and unvisited, visit the neighbor recursively (dfs traversal),
                cycle = self.dfs_cycle(neighbor, list_v)                                                                    # using neighbor as new current vertex, and passing visited list
                if cycle == True:                                                                                           # if previous call returned true, return True
                    return True
            elif self.adj_matrix[cur_v][neighbor] != 0:                                                                     # if the neighbor has been visited and there is a directed edge (non-zero value) leading back to the previous node, considered a cycle -> return True
                return True
        list_v[cur_v] = False                                                                                               # if the recursive call returns false(no cycle found on current directed path), reset the visited vertex to False (resetting graph for different path)
        return False


    def dijkstra(self, src: int) -> []:
        """
        Method that takes a starting vertex and calculates the shortest path length from that vertex to all other vertices
        in the graph. It returns a list containing the shortest path found (smallest sum of edges) between the source vertex
        to the destination vertex.
        """
        visited = [float('inf') for x in range(self.v_count)]
        visited[src] = 0
        pq = []
        heapq.heappush(pq,(0, src))
        while pq:
            current = heapq.heappop(pq)                                                                                     # front vertex of priority queue
            v = current[1]
            d = current[0]                                                                                                  # distance travelled so far to current vertex
            if visited[v] == float('inf'):                                                                                  # if the current vertex hasn't been travelled to yet, add distance travelled to it to visited array
                visited[v] = d
            if d <= visited[v]:                                                                                             # else if the vertex has been travelled to, but the distance travelled already is less than distance recorded for the current vertex
                for n in range(self.v_count):                                                                               # for all vertices in graph
                    n_d = self.adj_matrix[v][n]                                                                             # n_d is distance from current vertex to n (neighboring) vertex
                    if n_d!= 0 and d+n_d < visited[n]:                                                                      # if n is actually neighbor of v (n_d not zero), and the total distance travelled to n (calculated by adding current edge n_d to total distance so far d)                                                              # push (neighbor, total distance) to priority queue, where total distance = distance travelled so far + distance from current vertex to neighbor)
                        visited[n] = d+n_d                                                                                  # adjust the value of the neighbor in visited array and,
                        heapq.heappush(pq, (d + n_d, n))                                                                    # push that neighbor with new smaller distance to priority queue
        return visited





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
    print(g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')


    print("\nPDF - dijkstra() gradescope example 1")
    print("--------------------------")
    new = DirectedGraph()
    for _ in range(12):
        new.add_vertex()
    edges = [(2,1,19), (2,9,8), (8,1,13), (8,2,18), (9,4,2), (10,7,4), (10,9,6), (11,0,11), (11,9,11), (11,10,4)]
    for src, dst, weight in edges:
        new.add_edge(src, dst, weight)
    print (new)
    test = new.dijkstra(11)
    print(test)

    print("\nPDF - method has_cycle() gradescope example 1")
    print("----------------------------------")
    edges = [(1, 6, 6), (2, 8, 3), (2, 12, 5), (3, 1, 5),
             (3, 12, 6), (5, 4, 3), (5, 8, 1), (7, 2, 13),
             (8, 2, 9), (10, 7, 5), (11, 12, 4), (12, 0, 16)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.has_cycle(), sep='\n')