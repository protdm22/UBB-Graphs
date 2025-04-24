# Write the graph from a text file (as an external function)
def write_graph(graph, file_name):
    """
    Complexity - O(m)
    Write the graph to a text file.
    :param graph: the graph to be written
    :param file_name: the name of the file
    :return: None
    """
    output_file = open(file_name, "w")
    output_file.write(f"{graph.number_of_vertices} {graph.number_of_edges}\n")
    for edge in graph.get_edges_list():
        output_file.write(f"{edge[0]} {edge[1]} {graph.get_cost(edge[0], edge[1])}\n")
    output_file.close()
