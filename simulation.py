from platoon import Platoon
from objects.gipps_vehicle import Gipps_vehicle
from model.gipps import GippsModel 
import math 
import random 

class Simulation():
    def __init__(self,time,avStep = 100):
        self.time = time 
        self.gipps = GippsModel()
        self.avStep = avStep
        
    def get_gipps_loop_num(self, time, driver_reaction_time):
        return math.ceil(time / driver_reaction_time) #Return the greatest integer number 

#New definition with Y coord added 
    def run_gipps_simulation(self, n, desired_speed, y_location, randomness = False, reac_time = 2 / 3):
        loop_num = self.get_gipps_loop_num(self.time,reac_time)
        plat = Platoon()
        leader = None 
        for i in range(n):
            newcar = Gipps_vehicle(ith=i, desired_speed = desired_speed, gipps=self.gipps,y_location=y_location,
                leader = leader, reaction_time = reac_time,randomness = randomness, length=5)
            plat.add_vehicle(newcar)
            leader = newcar
        plat.run(loop_num)
        return plat 

    def run_gipps_simulation_braking(self, n, intend_speed, sim_length_after_stop,
                                    stop_veh_idx=0, randomness=False, react_time=2/3):
        p = self.run_gipps_simulation(n,intend_speed,randomness,react_time)
        p.platoon[stop_veh_idx].start_sudden_braking()
        new_loop_num = self.get_gipps_loop_num(sim_length_after_stop,react_time)
        p.run(new_loop_num)
        return p 

    def rung_gipps_graph(self,n, desired_speed, y_location,positions, randomness = False,
            reac_time = 2/3):
            loop_num = self.get_gipps_loop_num(self.time, reac_time)
            plat = Platoon() 
            leader = None 
            for i in range(n):
                newcar = Gipps_vehicle(ith=i,desired_speed = desired_speed, gipps=self.gipps, 
                    y_location = y_location,positions=positions, leader = leader, reaction_time= reac_time,
                    randomness= randomness, length= 5) 
                plat.add_vehicle(newcar)
                leader = newcar
            plat.run_bidimensional(loop_num,positions)
            return plat 
            

