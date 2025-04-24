# Read the graph from a text file (as an external function)
def read_graph(graph, file_name):
    """
    Complexity - O(m)
    Read the graph from a text file.
    :param graph: the graph to be read
    :param file_name: the name of the file
    :return: None
    """
    with open(file_name) as input_file:
        lines = input_file.readlines()

    graph.clear_graph()
    first_line = lines[0].split()
    graph.vertice_count = int(first_line[0])

    for line in lines[1:]:
        start_vertex, end_vertex, cost = map(int, line.split())
        graph.add_edge(start_vertex, end_vertex, cost)
