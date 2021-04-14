# GippsTrafficSimulation
## Installation Guide
This section will guide the interested person to create a new Python virtual environmentand install the requirements to be able to run the simulator.  The first step is to clone theGitHub repository to our desktop.  We can do this in two different ways. The first way is by downloading the source code directly from the repository page; the downloaded zip 
file must be unzipped.  The second method is by cloning the repository using the command line, the repository can be cloned using the following command:
```bash
git  clone  https:// github.com/moonR2/GippsTrafficSimulation.git
```
Now that the repository is on our desktop, we need to install the necessary dependencies. This is the list of dependencies we need to install:
* NumPy
* Matplotlib
* NetworkX

There are different ways to install these dependencies. We recommend creating a Python virtual environment, to create a new virtual environment we can use the following code:
```bash
python3  -m venv Gipps 
````
This code will create a new virtual environment called Gipps. Now to use this environment we need to source it:
```bash
source /Gipps/bin/active
```
Finally, we can install the dependencies using PyPi. Remember that to run the following command we must change the directory to the repository folder:
```
pip  install  -r requirements.txt
```
## Run the Experiments
Now that we have everything ready to run the simulation or contribute to the project. We will explain the scheme of the different files, and what are the changes that we must make to run the different experiments. The files called:  first.py, second.py, third.py, and fourth.py; are the files correspondingto each experiment. These are the files that we will run with Python, for example,  the following code will run the first experiment
```
python3  first.py
```
However, before running each experiment a change is necessary for the simulation.py file. The file simulation.py contains the class called Simulation. This class is in charge of creating the different types of simulations; where each simulation is a method of the class. In the case of the simulation in two dimensions, the parameter path, contains the path ofthe vehicles.  It is important to change this parameter for each experiment; since the nodes passed to the shortestpath() function must exist in the street network. The following list describes the start and end node of each experiment:
* First experiment:  The path of the vehicles goes from node *a* to node *b*.
* Second experiment:  The path of the vehicles goes from node *a* to node *b*.
* Third experiment:  The path of the vehicles goes from node *a* to node *c2*.
* Fourth experiment:  The path of the vehicles goes from node *25* to node *14*.

Of course, we can change or randomly generate the nodes to our liking, as long as the nodes exist in the graph. But to reproduce the results described in this project we must use the nodes listed above. The file platoon.py contains a class called Platoon. In this class, there are several lists in charge of saving the different information generated in the simulation. Finally, the folders model and objects contain different classes. Also, a custom simulation can be created easily. The first step is to build the street network, but it is also recommended to read the NetworkX documentation for creating more complex graphs.  Once the graph is created we need to create a street object with the edges and nodes from the graph.  Finally, we need to call the desired simulation by using the methods from the class Simulation; where its parameters are:
* Number of vehicles.
* Street network speed limit.
* Street network graph.
* Street network nodes with their respective coordinates.
* Street class.
* A boolean indicating if you want the vehicle parameters to be generated randomly.
* The reaction time of the drivers.

Once the simulation is run, the vehicle data can be accessed through the platoon class. Matplotlib makes use of this data to be able to visualize the simulation. Any questions orproblems can be sent to the issues section.
