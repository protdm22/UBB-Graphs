import random
from src.graph import Graph


# Create a random graph with specified number of vertices and of edges (as an external function)
def generate_random_graph(number_of_vertices, number_of_edges):
    """
    Complexity - O(n^2)

    https://wiki.python.org/moin/TimeComplexity
        - the time complexity of set() is O(n)
        - the time complexity of accessing an element is in a dict is O(1)

    Generate a random graph with a specified number of vertices and of edges.
    If the number of edges is greater than the maximum possible number of edges,
    the graph will have the maximum number of edges.

    :param number_of_vertices: the number of vertices
    :param number_of_edges: the number of edges
    :return: the generated graph
    """
    graph = Graph(number_of_vertices)
    edge_counter = 0
    max_edges = number_of_vertices ** 2

    while edge_counter < number_of_edges and edge_counter < max_edges:
        start_vertex = random.randint(0, number_of_vertices - 1)
        end_vertex = random.randint(0, number_of_vertices - 1)
        if not graph.is_edge(start_vertex, end_vertex):
            cost = random.randint(0, 100)
            graph.add_edge(start_vertex, end_vertex, cost)
            edge_counter += 1

    return graph
