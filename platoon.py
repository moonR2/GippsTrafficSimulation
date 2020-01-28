"""The class platoon have the lists to save the information for vehicles, the list platoon have n cars (object)
which is object has a list lrecords with it [Acceleration, Speed, Location, Headway] and ltime with the respective
simulation time for each record"""

class Platoon:
    def __init__(self):
        self.n = 0
        self.platoon = []
        self.lrecords = []
        self.ltime = []
        self.delays = []
        self.vehPass = 0

    def add_vehicle(self, car):
        self.platoon.append(car)
        self.n += 1

    def run(self, loop_num):

        # Creating n vehicles and append it to platoon list
        for i in range(loop_num):
            for idx in range(self.n):
                self.platoon[idx].update()
                
        lastUpdate = sorted(self.platoon[idx].ltime)[-1]

        for idx in range(self.n):
            #Getting the last location from idx vehicle
            indexLoc = self.platoon[idx].ltime.index(lastUpdate)
            idxLoc = self.platoon[idx].lrecords[indexLoc][2]
            self.lrecords.append(self.platoon[idx].lrecords) # List for test purposes 
            if  idxLoc > 0:
                # count vehicle passing
                self.vehPass += 1
    
        for i in range(loop_num * 2): # *2 For Correclty simulation time 
            for idx in range(self.vehPass): # Update new vehicle information 
                self.platoon[idx].update()
                
        # Append delays to a list         
        for idx in range(self.vehPass):
            self.delays.append(self.platoon[idx].calc_delay())

        