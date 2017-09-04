import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import queue
from prediction import create_tree


def draw_main(lst, path):
    G = nx.DiGraph()
    edge_labels = {}

    index = 1
    root = create_tree(lst)
    q = queue.Queue()
    q.put((root.name, root.type_table))

    while not q.empty():
        name, type_table = q.get()

        for key, val in type_table.items():
            if G.has_node(val.name):
                G.add_edge(name, val.name + str(index), labels=key)
                edge_labels[(name, val.name + str(index))] = key
                index += 1
            else:
                G.add_edge(name, val.name, labels=key)
                edge_labels[(name, val.name)] = key

            if len(val.type_table) > 0:
                q.put((val.name, val.type_table))

    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True, arrows=True)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.savefig(path)
    return
