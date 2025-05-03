import copy
import heapq


class Graph:
    def __init__(self, number_of_vertices=0):
        self.__inbound_edges = {}
        self.__outbound_edges = {}
        self.__costs = {}
        self.__vertices = set()
        self.__edge_count = 0
        self.vertice_count = number_of_vertices

        for i in range(number_of_vertices):
            self.__inbound_edges[i] = set()
            self.__outbound_edges[i] = set()

    # get the number of vertices (and edges)
    @property
    def number_of_vertices(self):
        """
        Complexity - Theta(1)
        :return: the number of vertices in the graph
        """
        return self.vertice_count if self.vertice_count > len(self.__vertices) else len(self.__vertices)

    @property
    def number_of_edges(self):
        """
        Complexity - Theta(1)
        :return: the number of edges in the graph
        """
        return self.__edge_count

    # parse (iterate) the set of vertices
    def parse_vertices(self):
        """
        Complexity - Theta(n)
        https://wiki.python.org/moin/TimeComplexity
            - the time complexity of set() is O(n)
            - the time complexity of accessing an element is in a dict is O(1)
        :return: an iterator for the set of vertices
        """
        return set(self.__vertices)

    # given two vertices, find out whether there is an edge from the first one to the second one
    def is_edge(self, start_vertex, end_vertex):
        """
        Complexity - Theta(1)
        https://wiki.python.org/moin/TimeComplexity
            - the time complexity of accessing an element is in a dict is O(1)
        :param start_vertex: start vertex
        :param end_vertex: end vertex
        :return: true if there is an edge from start_vertex to end_vertex, false otherwise
        """
        return end_vertex in self.__outbound_edges[start_vertex]

    # get the in degree and the out degree of a specified vertex
    def in_degree(self, vertex):
        """
        Complexity - Theta(1)
        https://wiki.python.org/moin/TimeComplexity
            - the time complexity of len() is O(1)
        :param vertex: vertex to get the in degree of
        :return: in degree of the vertex
        """
        return len(self.__inbound_edges[vertex])

    def out_degree(self, vertex):
        """
        Complexity - Theta(1)
        https://wiki.python.org/moin/TimeComplexity
            - the time complexity of len() is O(1)
        :param vertex: vertex to get the out degree of
        :return: out degree of the vertex
        """
        return len(self.__outbound_edges[vertex])

    # parse (iterate) the set of outbound edges of a specified vertex (that is, provide an iterator).
    # For each outbound edge, the iterator shall provide the Edge_id of the current edge (or the target vertex, if no Edge_id is used).
    def parse_outbound(self, vertex):
        """
        Complexity - Theta(n)
        https://wiki.python.org/moin/TimeComplexity
            - the time complexity of accessing an element is in a dict is O(1)
        :param vertex: vertex to get the outbound edges of
        :return: an iterator for the set of outbound edges of the vertex
        """
        for vertex in self.__outbound_edges[vertex]:
            yield vertex

    # parse the set of inbound edges of a specified vertex (as above)
    def parse_inbound(self, vertex):
        """
        Complexity - Theta(n)
        https://wiki.python.org/moin/TimeComplexity
            - the time complexity of accessing an element is in a dict is O(1)
        :param vertex: vertex to get the inbound edges of
        :return: an iterator for the set of inbound edges of the vertex
        """
        for vertex in self.__inbound_edges[vertex]:
            yield vertex

    # retrieve or modify the information (the integer) attached to a specified edge
    def modify_cost(self, edge, new_cost):
        """
        Complexity - Theta(1)
        https://wiki.python.org/moin/TimeComplexity
            - the time complexity of accessing an element is in a dict is O(1)
        :param edge: the edge to modify the cost of
        :param new_cost: the new cost of the edge
        :return: None
        """
        self.__costs[edge] = new_cost

    # The graph shall be modifiable: it shall be possible to add and remove an edge, and to add and remove a vertex.
    # Think about what should happen with the properties of existing edges and with the identification of remaining
    # vertices. You may use an abstract Vertex_id instead of an int in order to identify vertices;
    # in this case, provide a way of iterating the vertices of the graph.
    def add_edge(self, start_vertex, end_vertex, cost):
        """
        Complexity - Theta(1)
        https://wiki.python.org/moin/TimeComplexity
            - the time complexity of add() is O(1)
            - the time complexity of accessing an element is in a dict is O(1)
        :param start_vertex: the start vertex
        :param end_vertex: the end vertex
        :param cost: the cost of the edge
        :return: None
        """
        if start_vertex not in self.__vertices:
            self.__vertices.add(start_vertex)
            self.__inbound_edges[start_vertex] = set()
            self.__outbound_edges[start_vertex] = set()

        if end_vertex not in self.__vertices:
            self.__vertices.add(end_vertex)
            self.__inbound_edges[end_vertex] = set()
            self.__outbound_edges[end_vertex] = set()

        if self.is_edge(start_vertex, end_vertex):
            return False

        self.__outbound_edges[start_vertex].add(end_vertex)
        self.__inbound_edges[end_vertex].add(start_vertex)
        self.__costs[(start_vertex, end_vertex)] = cost
        self.__edge_count += 1

        return True

    def remove_edge(self, start_vertex, end_vertex):
        """
        Complexity - Theta(1)
        :param start_vertex: the start vertex
        :param end_vertex: the end vertex
        :return: True if the edge was removed, False otherwise
        """
        if not self.is_edge(start_vertex, end_vertex):
            return False

        self.__outbound_edges[start_vertex].remove(end_vertex)
        self.__inbound_edges[end_vertex].remove(start_vertex)
        self.__costs.pop((start_vertex, end_vertex))
        self.__edge_count -= 1

        return True

    def add_vertex(self, vertex):
        """
        Complexity - Theta(1)
        Adds a vertex to the graph
        :param vertex: the vertex to add
        :return: True if the vertex was added, False otherwise
        """
        if vertex not in self.__vertices:
            self.__vertices.add(vertex)
            return True
        return False

    def remove_vertex(self, vertex_to_remove):
        """
        Complexity - Theta(n)
        Removes a vertex from the graph
        :param vertex_to_remove: the vertex to remove
        :return: True if the vertex was removed, False otherwise
        """
        if vertex_to_remove not in self.__vertices:
            return False

        for vertex in self.parse_vertices():
            self.remove_edge(vertex, vertex_to_remove)
            self.remove_edge(vertex_to_remove, vertex)

        self.__outbound_edges.pop(vertex_to_remove)
        self.__inbound_edges.pop(vertex_to_remove)
        self.__vertices.remove(vertex_to_remove)
        self.vertice_count -= 1

        return True

    # The graph shall be copyable, that is, it should be possible to make an exact copy of a graph,
    # so that the original can be then modified independently of its copy. Think about the desirable
    # behaviour of an Edge_property attached to the original graph, when a copy is made.
    def copy_graph(self):
        """
        Complexity - Theta(n)
        :return: a deep copy of the graph
        """
        return copy.deepcopy(self)

    def get_cost(self, start_vertex, end_vertex):
        """
        Complexity - Theta(1)
        Retrieves the cost of the edge from start_vertex to end_vertex
        :param start_vertex: the start vertex
        :param end_vertex: the end vertex
        :return: the cost of the edge from start_vertex to end_vertex
        """
        return self.__costs[(start_vertex, end_vertex)]

    def get_edges_list(self):
        """
        Complexity - Theta(n)
        Returns a list of all edges in the graph
        :return: a list of all edges in the graph
        """
        return self.__costs.keys()

    def is_vertex(self, vertex):
        """
        Complexity - Theta(1)
        Checks if a vertex is in the graph
        :param vertex: the vertex to check
        :return: True if the vertex is in the graph, False otherwise
        """
        return vertex in self.__vertices

    def clear_graph(self):
        """
        Complexity - Theta(1)
        Clears the graph
        :return: None
        """
        self.__inbound_edges.clear()
        self.__outbound_edges.clear()
        self.__vertices.clear()
        self.__costs.clear()
        self.__edge_count = 0

    def backward_bfs(self, start_vertex, end_vertex):
        # Check if both start and end vertices exist in the graph
        if not self.is_vertex(start_vertex) or not self.is_vertex(end_vertex):
            return None  # Return None if either vertex is not in the graph

        # Initialize the queue with the end vertex (for backward BFS)
        queue = [end_vertex]
        # Dictionary to store distances from the end vertex
        dist_dict = {end_vertex: 0}
        # Dictionary to store the predecessor of each vertex in the path
        next_dict = {end_vertex: None}

        # Perform BFS
        while queue:
            # Dequeue the first vertex in the queue
            current_vertex = queue.pop(0)
            # Get the current distance from the end vertex
            current_distance = dist_dict[current_vertex]

            # Iterate through all inbound neighbors of the current vertex
            for neighbor in self.__inbound_edges[current_vertex]:
                # If the neighbor has not been visited
                if neighbor not in dist_dict:
                    # Update the distance to the neighbor
                    dist_dict[neighbor] = current_distance + 1
                    # Set the current vertex as the predecessor of the neighbor
                    next_dict[neighbor] = current_vertex
                    # Enqueue the neighbor for further exploration
                    queue.append(neighbor)

        # If the start vertex is not reachable from the end vertex, return None
        if start_vertex not in dist_dict:
            return None

        # Reconstruct the path from start_vertex to end_vertex
        path = []
        current_vertex = start_vertex
        while current_vertex is not None:
            # Add the current vertex to the path
            path.append(current_vertex)
            # Move to the next vertex in the path
            current_vertex = next_dict[current_vertex]

        # Return the path (in forward order from start_vertex to end_vertex)
        return path

    def dijkstra(self, start_vertex, end_vertex):
        """
        Finds the lowest cost walk between two vertices using Dijkstra's algorithm.
        :param start_vertex: the starting vertex
        :param end_vertex: the ending vertex
        :return: a tuple (path, cost) where path is the list of vertices in the lowest cost walk
                 and cost is the total cost of the walk. Returns None if no path exists.
        """
        # Check if both start and end vertices exist in the graph
        if not self.is_vertex(start_vertex) or not self.is_vertex(end_vertex):
            return None  # Return None if either vertex is not in the graph

        # Priority queue to store (current_cost, current_vertex)
        # The queue ensures that the vertex with the smallest cost is processed first
        priority_queue = [(0, start_vertex)]

        # Dictionary to store the minimum cost to reach each vertex
        # Initialize all vertices with infinity cost, except the start vertex which has a cost of 0
        dist_dict = {vertex: float('inf') for vertex in self.__vertices}
        dist_dict[start_vertex] = 0

        # Dictionary to store the predecessor of each vertex
        # This is used to reconstruct the path after the algorithm finishes
        prev_dict = {start_vertex: None}

        # Process the priority queue until it is empty
        while priority_queue:
            # Extract the vertex with the smallest cost from the queue
            current_cost, current_vertex = heapq.heappop(priority_queue)

            # If the current vertex is the end vertex, we can stop early
            if current_vertex == end_vertex:
                break

            # Iterate through all neighbors of the current vertex
            for neighbor in self.parse_outbound(current_vertex):
                # Get the cost of the edge from the current vertex to the neighbor
                cost = self.get_cost(current_vertex, neighbor)

                # Calculate the new cost to reach the neighbor
                new_cost = current_cost + cost

                # If the new cost is smaller than the previously recorded cost for the neighbor
                if new_cost < dist_dict[neighbor]:
                    # Update the minimum cost to reach the neighbor
                    dist_dict[neighbor] = new_cost

                    # Update the predecessor of the neighbor to the current vertex
                    prev_dict[neighbor] = current_vertex

                    # Add the neighbor to the priority queue with the updated cost
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        # If the end vertex is unreachable (its cost is still infinity), return None
        if dist_dict[end_vertex] == float('inf'):
            return None

        # Reconstruct the path from the start vertex to the end vertex
        path = []
        current_vertex = end_vertex
        while current_vertex is not None:
            # Add the current vertex to the path
            path.append(current_vertex)

            # Move to the predecessor of the current vertex
            current_vertex = prev_dict[current_vertex]

        # Reverse the path to get it in the correct order (from start to end)
        path.reverse()

        # Return the reconstructed path and the total cost of the walk
        return path, dist_dict[end_vertex]
