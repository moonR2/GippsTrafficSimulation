import matplotlib.pyplot as plt
from simulation import Simulation
from objects.road import road, street
import numpy as np
import sys
import networkx as nx
from statistics import mean 

# Parameters needed for simulation
simulation_time = 90
n = 10
intended_speed = 33.33 
sim = Simulation(time=simulation_time, avStep=100)
colors = ["red", "blue", "black", "green", "pink"]
streets = []
def plot_trajectory(platoon,x_max,y_max):
    vec = []
    time = []
    for i in range(len(platoon)):
        for j in range(len(platoon[0].lrecords)):
            vec.append(platoon[i].lrecords[j][3])

        ylabelmap = str("Vehicle: %d" %(i+1))
        plt.ylabel("Vehicle Location $(m)$")
        plt.xlabel("Simulation Time $(sec)$")
        plt.legend("Vehicle n")
        plt.xlim(0,x_max)
        plt.ylim(0,y_max)
        plt.grid()
        plt.plot(platoon[0].ltime,vec,label=ylabelmap)
        L = plt.legend()
        L.get_texts()[i].set_text(ylabelmap)
        vec = []
    plt.savefig("images/HeadwayVsTime.png")

if sim:
    s_means = []
    h_means = []
    # Trying to make a graph lol
    edges_list = []
    points = []
    random_state = np.random.RandomState(42)
    graph = nx.fast_gnp_random_graph(35,0.1,random_state,directed=True)
    #path = nx.shortest_path(graph,0,12)
    #print(path)

    #nx.draw(graph, with_labels=True, node_size = 10, node_color = "purple")
    for e in list(graph.edges):
        edges_list.append(e)
    for j in list(graph.nodes):
        print(j)
   
    pos = nx.nx_agraph.graphviz_layout(graph)
    pos = nx.rescale_layout_dict(pos,scale=1000)
    # Position of the node as node atrribute
    # Testing road class 
    st = street()
    for i in range(len(edges_list)):
        new_road = road(edges_list[i],pos,i)
        st.add_street(new_road)

    s_means = []
    h_means = []
    #a_route = nx.shortest_path(graph, "0", "12")
    #nx.draw(graph, pos,with_labels=True, node_size = 50, node_color = "red", width = 2.0, style = "dashed", label = "500m Road Link")
    for j in range(200):
        for i in range(10):
            speeds = []
            headways = []
            platoons = []
            total_pass = 0 
            st = street()
            for i in range(len(edges_list)):
                new_road = road(edges_list[i],pos,i)
                st.add_street(new_road)

            g = sim.run_xy(
                n, intended_speed, graph, pos, st, randomness=True, reac_time=2 / 3
            )
            del st 
            platoons.append(g)

            for i in platoons:
                total_pass += i.vehPass
            
            for i in platoons:
                for j in range(n):
                    if i.platoon[j].speed_pass_zero != None:
                        speeds.append(i.platoon[j].speed_pass_zero)
                    if i.platoon[j].headway_pass_zero != 0 and i.platoon[j].headway_pass_zero != None:
                        headways.append(i.platoon[j].headway_pass_zero)

            s_means.append(np.round(np.mean(speeds),2))
            h_means.append(np.round(np.mean(headways),2))
            print(len(speeds))
            print("Mean Speed:", mean(speeds))
            print(len(headways))
            print("Mean Hedway:", mean(headways))

    print(s_means)
    print(h_means)
    plt.xlabel("Average space headway $(metres)$")
    plt.ylabel("Mean Speed $(m/s)$")
    plt.grid()
    plt.scatter(h_means,s_means,linewidths=0.5)
    plt.show()
    path = "images/test" + "headwaysVsSpeed.png"
    plt.savefig(path)
    #for i in range(len(g.platoon[0].lrecords)):
    #    for j in range(n):
    #        print("headway", g.platoon[j].lrecords[i][3])
    #        print("headway", g.platoon[j].ltime)
    # Animation
    #for i in range(len(g.platoon[0].lrecords)):
    #    for p in points:
    #        p.remove()

    #    points = []

    #    for j in range(n):

    #        # plt.xlim(g.platoon[0].lrecords[0][2],g.platoon[0].lrecords[-1][2]) # Max and min location
    #        # This workaround make a zooom of the cars
    #        length = g.platoon[j].lrecords[i][4]
    #        #plt.xlim(-90,600) # Max and min location
    #        #plt.ylim(-200,200) # Road
    #        # points.append(plt.scatter(g.platoon[j].lrecords[i][2],start,marker='s',color=colors[j]))
    #        points.append(
    #            plt.scatter(
    #                g.platoon[j].position[i][0],
    #                g.platoon[j].position[i][1],
    #                marker="s",
    #                color="blue",
    #                s=(length * 5)
    #            )
    #        )
    #        plt.xlabel("Vehicle location")
    #        plt.axis("off")
    #        path = "images/test" + str(i) + ".png"
    #        #plt.savefig(path)
    #        plt.pause(0.01)
    #plt.show()
# Location vs Time plot 
    #x_max = g.platoon[0].ltime[-1]
    #y_max = 100
    #plot_trajectory(g.platoon,x_max,y_max+0.02)
    #plt.grid()
    #plt.show() 