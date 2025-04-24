from src.graph import Graph
from src.random_graph import generate_random_graph
from src.read_graph import read_graph
from src.ui import UI

if __name__ == "__main__":
    initial_graph = Graph()
    read_graph(initial_graph, "input")
    ui = UI(initial_graph)
    ui.run()
