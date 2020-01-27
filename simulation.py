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

    def run_gipps_simulation(self, n, desired_speed, randomness = False, reac_time = 2 / 3):
        loop_num = self.get_gipps_loop_num(self.time,reac_time)
        plat = Platoon()
        leader = None 
        for i in range(n):
            newcar = Gipps_vehicle(ith=i, desired_speed = desired_speed, gipps=self.gipps, 
                leader = leader, reaction_time = reac_time,randomness = randomness, length=5)
            plat.add_vehicle(newcar)
            leader = newcar
        plat.run(loop_num)
        return plat 