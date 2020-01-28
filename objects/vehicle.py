class Vehicle:
    def __init__(self, ith, leader, simulationStep, max_speed, length, miniGap):
        self.ith = ith # The itg vehicle in the queue
        self.set_leader(leader) 
        self.max_speed = max_speed
        self.length = length # lenght of the vehicle 
        self.miniGap = miniGap # the min gap between vehicles 
        self.simulationStep = simulationStep # simulation step (ms)
        self.simTime = 0 # Simulation start time (ms)
        self.suddenBraking = False # Should the vehicle brake? 
        self.location = self.calc_location() # Actual location of the vehicle 
        self.init_location = self.calc_location() # Initial location of the vehicle
        self.acceleration = 0 # Acceleration (m/s)
        self.speed = 0 # Speed (m/s)
        self.headway = 0 # Headway (s)
        self.lrecords = []
        self.ltime = []
        self.follower = None # Set follower vehicle 
        self.prev_location = 0 # Vehicle previous location 
        self.time_pass_zero = None 
        self.headway_pass_zero = None 
        self.speed_pass_zero = None 

    def set_leader(self, leader): 
        self.leader = leader 
        if leader:
            leader.follower = self 

    def calc_location(self):
        if self.leader: 
            return self.leader.location - self.miniGap - self.leader.length
        return 0 
    
    def start_sudden_braking(self):
        self.suddenBraking = True
    
    def calc_delay(self):
        if self.location > 0: 
            difference = (self.location - self.init_location)
            return (self.simTime / 1000 - difference / self.max_speed) / (difference/1000)

    # Now the info is working with lists instead of dictionaries 
    def infoToLists(self):
        self.headway = 0 
        if self.leader and self.speed > 0: 
            self.headway = (self.leader.location - self.location) / self.speed

        self.lrecords.append(list(map(lambda x: round(x,4),[self.acceleration, self.speed, self.location, self.headway])))
        self.ltime.append(self.simTime)

        self.simTime += self.simulationStep

    def list_update(self):
        self.infoToLists()

        if self.leader:
            spacing = self.leader.location - self.location - self.leader.length
            if spacing <= 0:
                print("Vehicle has crashed", self.ith)

        if self.time_pass_zero == None and self.location >= 0: 
            self.time_pass_zero = self.simTime
            self.headway_pass_zero = self.headway
            self.speed_pass_zero = self.speed

   
