from simulation import Simulation

simulation_time = 5
n = 2
intended_speed = 80 * 1000/3600 
sim = Simulation(time = simulation_time, avStep = 100)

if sim:
    print("Running Gipps simulation")
    print("Simulation Time : [Acceleration, Speed, Location, Headway]") 
    g = sim.run_gipps_simulation(n,intended_speed,randomness=False,reac_time=2/3)
    
    for i in range(len(g.platoon)):
        print("Vehicle: ",i)
        for j in range(len(g.platoon[i].lrecords)):
            print("--------------------------------------------------")
            print("Simulation Time: ",g.platoon[i].ltime[j])
            print("A,S,L,H: ", g.platoon[i].lrecords[j])

