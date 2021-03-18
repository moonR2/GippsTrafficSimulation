import matplotlib.pyplot as plt
from simulation import Simulation
from objects.road import road, street
import numpy as np
import sys
import networkx as nx

# Parameters needed for simulation
simulation_time = 40
n = 6
intended_speed = (80 * 1000) / 3600  # 22,22
sim = Simulation(time=simulation_time, avStep=100)
colors = ["red", "blue", "black", "green", "pink"]
streets = []

if sim:
    # Dictionary handling the coordinates of each edge
    pos = {
        "a": (10, 0),
        "b": (510, 0)
    }
    # Getting the start of the road from the graph
    positions = list(pos.values())
    start = positions[0][1]

    # Variables and  parameters for animation
    # fig, ax = plt.subplots()
    points = []

    # Trying to make a graph lol
    graph = nx.DiGraph()
    graph.add_nodes_from(pos.keys())
    # Position of the node as node atrribute
    for d, p in pos.items():
        graph.nodes[d]["pos"] = p

    edges_list = [
        ("a","b")
    ]
    graph.add_edges_from(edges_list)

    # Testing road class 
    st = street()
    for i in range(len(edges_list)):
        new_road = road(edges_list[i],pos,i)
        st.add_street(new_road)

    a_route = nx.shortest_path(graph, "a", "b")
    nx.draw(graph, pos,with_labels=True, node_size = 200, node_color = "green", width = 2.0, style = "dashed", label = "500m Road Link")
    nx.draw_networkx_edges(graph, pos)
    g = sim.run_xy(
        n, intended_speed, graph, pos, st, randomness=True, reac_time=2 / 3
    )
    # Animation
    for i in range(len(g.platoon[0].lrecords)):
        for p in points:
            p.remove()

        points = []

        for j in range(n):

            # plt.xlim(g.platoon[0].lrecords[0][2],g.platoon[0].lrecords[-1][2]) # Max and min location
            # This workaround make a zooom of the cars
            length = g.platoon[j].lrecords[i][4]
            plt.xlim(-90,600) # Max and min location
            plt.ylim(-200,200) # Road
            # points.append(plt.scatter(g.platoon[j].lrecords[i][2],start,marker='s',color=colors[j]))
            points.append(
                plt.scatter(
                    g.platoon[j].position[i][0],
                    g.platoon[j].position[i][1],
                    marker="s",
                    color="blue",
                    s=(length * 5)
                )
            )
            plt.xlabel("Vehicle location")
            plt.axis("off")
            path = "images/test" + str(i) + ".png"
            plt.savefig(path)
            plt.pause(0.01)
    plt.show()
