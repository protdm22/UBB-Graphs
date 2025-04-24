import os

from src.random_graph import generate_random_graph
from src.read_graph import read_graph
from src.write_graph import write_graph

EXIT = "0"

GET_NR_OF_VERTICES = "1"
GET_NR_OF_EDGES = "2"
PARSE_VERTICES = "3"
CHECK_EDGE = "4"
GET_DEGREE = "5"
PARSE_EDGES = "6"
MODIFY_COST = "7"
MODIFY_GRAPH = "8"
READ_GRAPH = "9"
WRITE_GRAPH = "10"
RANDOM_GRAPH = "11"
COPY_GRAPH = "12"
CHANGE_GRAPH = "13"
BACKWARD_BFS = "14"


class UI:
    def __init__(self, graph):
        self.__graph = graph
        self.__graph_copy = None

    @staticmethod
    def print_menu():
        print("--------Menu--------")
        print("1. Get the number of vertices")
        print("2. Get the number of edges")
        print("3. Parse the set of vertices")
        print("4. Check if edge exists")
        print("5. Get degree of vertex")
        print("6. Parse the set of edges of a vertex")
        print("7. Get/Modify edge cost")
        print("8. Modify graph")
        print("9. Read graph from a file")
        print("10. Write graph to a file from a file")
        print("11. Generate a random graph")
        print("12. Copy graph")
        print("13. Change graph")
        print("14. Find shortest path using backward BFS")
        print("0. Exit")
        print("--------------------")

    def run(self):
        while True:
            self.print_menu()

            option = input(">>> ")

            try:
                if option == EXIT:
                    break

                elif option == GET_NR_OF_VERTICES:
                    print(f"The graph has {self.__graph.number_of_vertices} vertices")

                elif option == GET_NR_OF_EDGES:
                    print(f"The graph has {self.__graph.number_of_edges} edges")

                elif option == PARSE_VERTICES:
                    vertices = self.__graph.parse_vertices()
                    vertices_set = ""
                    for vertex in vertices:
                        vertices_set += f"{str(vertex)} "
                    print(f"The set of vertices is: {vertices_set}")

                elif option == CHECK_EDGE:
                    start_vertex = int(input("Start vertex: "))
                    end_vertex = int(input("End vertex: "))
                    if self.__graph.is_vertex(start_vertex) and self.__graph.is_vertex(end_vertex):
                        if self.__graph.is_edge(start_vertex, end_vertex):
                            print(
                                f"There is an edge from {start_vertex} to {end_vertex} (cost: {self.__graph.get_cost(start_vertex, end_vertex)})")
                        else:
                            print(f"There is no edge from {start_vertex} to {end_vertex}")
                    else:
                        print("Invalid vertices!")

                elif option == GET_DEGREE:
                    vertex = int(input("Vertex: "))
                    if self.__graph.is_vertex(vertex):
                        option = input("1. In degree\n2. Out degree\n>>> ")
                        if option == "1":
                            print(f"The in degree of vertex {vertex} is {self.__graph.in_degree(vertex)}")
                        elif option == "2":
                            print(f"The out degree of vertex {vertex} is {self.__graph.out_degree(vertex)}")
                        else:
                            print("Invalid option!")
                    else:
                        print(f"Vertex {vertex} does not exist!")

                elif option == PARSE_EDGES:
                    try:
                        vertex = int(input("Vertex: "))
                        if self.__graph.is_vertex(vertex):
                            option = input("1. Inbound\n2. Outbound\n>>> ")
                            if option == "1":
                                edges = self.__graph.parse_inbound(vertex)
                                edge_set = ""
                                for edge in edges:
                                    edge_set += f"{str(edge)} "
                                print(f"The set of inbound edges for vertex {vertex} is: {edge_set}")
                            elif option == "2":
                                edges = self.__graph.parse_outbound(vertex)
                                edge_set = ""
                                for edge in edges:
                                    edge_set += f"{str(edge)} "
                                print(f"The set of outbound edges for vertex {vertex} is: {edge_set}")
                            else:
                                print("Invalid option!")
                        else:
                            print(f"Vertex {vertex} does not exist!")

                    except ValueError:
                        print("Vertices must be integers!")

                elif option == MODIFY_COST:
                    try:
                        start_vertex = int(input("Start vertex: "))
                        end_vertex = int(input("End vertex: "))
                        if self.__graph.is_vertex(start_vertex) and self.__graph.is_vertex(end_vertex):
                            if self.__graph.is_edge(start_vertex, end_vertex):
                                print(f"Current cost: {self.__graph.get_cost(start_vertex, end_vertex)}")
                                cost = int(input("Enter new cost: "))
                                self.__graph.modify_cost((start_vertex, end_vertex), cost)

                            else:
                                print(f"There is no edge from {start_vertex} to {end_vertex}")
                        else:
                            print("Invalid vertices!")

                    except ValueError:
                        print("Vertices must be integers!")

                elif option == MODIFY_GRAPH:
                    option = input("1. Add edge\n2. Delete edge\n3. Add vertex\n4. Delete vertex\n>>> ")

                    if option == "1":
                        try:
                            start_vertex = int(input("Enter start vertex: "))
                            end_vertex = int(input("Enter end vertex: "))
                            cost = int(input("Enter cost: "))
                            if self.__graph.add_edge(start_vertex, end_vertex, cost):
                                print(f"Edge between {start_vertex} and {end_vertex} successfully added")
                            else:
                                print(f"There already is an edge between vertices {start_vertex} and {end_vertex}")
                        except ValueError:
                            print("Vertices must be integers!")

                    elif option == "2":
                        try:
                            start_vertex = int(input("Enter start vertex: "))
                            end_vertex = int(input("Enter end vertex: "))
                            if self.__graph.remove_edge(start_vertex, end_vertex):
                                print(f"Edge between {start_vertex} and {end_vertex} removed successfully")
                            else:
                                print(f"There is no edge between {start_vertex} and {end_vertex}")
                        except ValueError:
                            print("Vertices must be integers!")

                    elif option == "3":
                        try:
                            vertex = int(input("Enter vertex: "))
                            if self.__graph.add_vertex(vertex):
                                print(f"Vertex {vertex} added successfully")
                            else:
                                print(f"Vertex {vertex} already exists")
                        except ValueError:
                            print("Vertex must be an integer!")

                    elif option == "4":
                        try:
                            vertex = int(input("Enter vertex: "))
                            if self.__graph.remove_vertex(vertex):
                                print(f"Vertex {vertex} removed successfully")
                            else:
                                print(f"Vertex {vertex} does not exist")
                        except ValueError:
                            print("Vertex must be an integer!")

                    else:
                        print("Invalid option!")

                elif option == READ_GRAPH:
                    filename = input("Enter filename to read from: ")
                    if os.path.exists(filename):
                        read_graph(self.__graph, filename)
                    else:
                        print("File not found!")


                elif option == WRITE_GRAPH:
                    filename = input("Enter filename to write to: ")
                    write_graph(self.__graph, filename)

                elif option == RANDOM_GRAPH:
                    vertices = int(input("Enter number of vertices:"))
                    edges = int(input("Enter number of edges:"))
                    self.__graph = generate_random_graph(vertices, edges)

                elif option == COPY_GRAPH:
                    self.__graph_copy = self.__graph.copy_graph()
                    print("Graph copied successfully")

                elif option == CHANGE_GRAPH:
                    self.__graph_copy, self.__graph = self.__graph, self.__graph_copy
                    print("Graph changed successfully")

                elif option == BACKWARD_BFS:
                    start_vertex = int(input("Start vertex: "))
                    end_vertex = int(input("End vertex: "))
                    if self.__graph.is_vertex(start_vertex) and self.__graph.is_vertex(end_vertex):
                        path = self.__graph.backward_bfs(start_vertex, end_vertex)
                        if path is not None:
                            print(f"Path from {start_vertex} to {end_vertex}: {path}, length: {len(path) - 1}")
                        else:
                            print(f"No path from {start_vertex} to {end_vertex}")
                    else:
                        print("Invalid vertices!")
                else:
                    print("Invalid option!")

            except ValueError:
                print("Value must be an integer!")
