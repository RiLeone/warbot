#!/usr/bin/env python3
"""
    Utility functions for graphs
    =====================

    TODO

"""
import networkx as nx
import matplotlib.pyplot as plt


def drawGraph(graph):
    """Create a Plot with a Graph
    """
    G = nx.DiGraph()
    G.add_edges_from(graph)

    # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
    pos = nx.spring_layout(G)
    # TODO: add node_size as the size of the state
    nx.draw_networkx_nodes(G, pos, node_color='r')
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
    plt.show()


if __name__ == "__main__":
    print(__doc__)
    import WorldJsonParser

    wjp = WorldJsonParser.WorldJsonParser("../worlds/Switzerland/states.json")
    drawGraph(wjp.graphNodes())
