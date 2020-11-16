from objects.vehicle import Vehicle
from pygame.math import Vector2 
from numpy import random

class Gipps_vehicle(Vehicle):
    def __init__(self, ith, desired_speed,y_location,positions, gipps,leader=None, reaction_time = 2 /3, 
        randomness = False, length = 5):

        max_acc = 1.7
        eff_size = 6.5
        miniGap = 2 
        desired_speed = 20

        if randomness: 
            max_acc = self.pick_normal(max_acc,0.3**2)
            eff_size = self.pick_normal(eff_size, 0.3**2)
            miniGap = eff_size - length 
            desired_speed = self.pick_normal(desired_speed, 3.2**2)

        super().__init__(
            ith,
            leader,
            y_location,
            simulationStep = reaction_time * 1000,
            max_speed = desired_speed,
            miniGap = miniGap, 
            length = length
            )

        self.max_acc = max_acc
        self.connected = False 
        self.eff_size = eff_size
        self.desired_speed = self.max_speed 
        self.desired_braking = -2 * self.max_acc # Max decelaration (Bn)
        self.reac_time = reaction_time 
        self.b_hat = min(-3.0,(self.desired_braking - 3) / 2)
        self.model = gipps 
        self.count = 0 
        self.positions = positions 

    # Check for influence
    def pick_normal(self,mean,std):
        pick = random.normal(mean,std)
        while pick > mean + std or pick < mean - std:
            pick = random.normal(mean,std)        
        return pick 
        
    def update(self):
        self.list_update()
        if self.suddenBraking:
            self.count += 1 
            new_acceleration = self.desired_braking
            new_speed = self.speed + self.reac_time/2 * (self.acceleration 
                + new_acceleration)
            #new_speed = self.model.get_speed(self)
        else:
            new_speed = self.model.get_speed(self)
        
        new_acceleration = (new_speed - self.speed) / self.reac_time
        #Euler integration method 
        new_location = self.location + 0.5 * (self.speed + new_speed) * self.reac_time 
        self.acceleration = new_acceleration
        self.speed = new_speed
        self.location = new_location

    def update_bidimensional(self):
        posList = list(self.positions.values())
        self.list_update()
        print("x",self.ith,self.location)
        print("y",self.ith,self.y_location)
        if(self.location >= 190): 
            print("HERE")
            new_speed = self.model.get_speed_y(self)
            new_acceleration = (new_speed - self.speed) / self.reac_time
            #Euler integration method 
            new_location_y = self.y_location + 0.5 * (self.speed + new_speed) * self.reac_time 
            self.acceleration = new_acceleration
            self.speed = new_speed
            self.y_location = new_location_y
        else:

            new_speed = self.model.get_speed(self)
            new_acceleration = (new_speed - self.speed) / self.reac_time
            #Euler integration method 
            new_location = self.location + 0.5 * (self.speed + new_speed) * self.reac_time 
            self.acceleration = new_acceleration
            self.speed = new_speed
            self.location = new_location

                
