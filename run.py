from simulation import Simulation

simulation_time = 5
n = 2
intended_speed = 80 * 1000/3600 
sim = Simulation(time = simulation_time, avStep = 100)

if sim:
    print("Running Gipps simulation")
    print("Simulation Time : [Acceleration, Speed, Location, Headway]") 
    #print("Simulation Time: ", simulation_time, "n: ", n, "Int_speed: ", intended_speed)
    g = sim.run_gipps_simulation(n,intended_speed,randomness=False,reac_time=2/3)
    print(g.lrecords)
    #for key,value in g.records.items():
    #    print("Vehicle: ", key)
    #    print("Simulation Time : [Acceleration, Speed, Headway] \n", value)
        