import numpy as np
from copy import deepcopy
from math import dist, sqrt
class Vehicle:
    def __init__(
        self, ith, leader, simulationStep, max_speed, length, miniGap, path, positions
    ):
        self.ith = ith  # The itg vehicle in the queue
        self.set_leader(leader)
        self.max_speed = max_speed
        self.length = length  # lenght of the vehicle
        self.miniGap = miniGap  # the min gap between vehicles
        self.simulationStep = simulationStep  # simulation step (ms)
        self.simTime = 0  # Simulation start time (ms)
        self.suddenBraking = False  # Should the vehicle brake?
        self.positions = positions
        self.path = deepcopy(path)
        self.location = self.calc_location()  # Actual location of the vehicle
        self.y_location = -509.64540729300904
        #self.y_location = 0
        self.init_location = self.calc_location()  # Initial location of the vehicle
        self.bi_location = np.array([self.location, self.y_location])
        self.acceleration = 0  # Acceleration (m/s)
        self.speed = 0  # Speed (m/s)
        self.headway = 0  # Headway (s)
        self.lrecords = []
        self.ltime = []
        self.follower = None  # Set follower vehicle
        self.prev_location = 0  # Vehicle previous location
        self.time_pass_zero = None
        self.headway_pass_zero = None
        self.speed_pass_zero = None
        self.position = []
        self.speedPass = []
        self.angle = 0.0

    def set_leader(self, leader):
        self.leader = leader
        if leader:
            leader.follower = self

    # Compute the initial position of the vehicles
    def calc_location(self):
        print(self.positions[self.path[0]])
        # Trusty values
        if self.ith == 0: 
            self.location = self.positions[self.path[0]][0]
        if self.leader:
            return self.leader.location - self.miniGap - self.leader.length
        return 0

    def start_sudden_braking(self):
        self.suddenBraking = True

    def stop_sudden_braking(self):
        self.suddenBraking = False

    def calc_delay(self):
        if self.location > 0:
            difference = self.location - self.init_location
            return (self.simTime / 1000 - difference / self.max_speed) / (
                difference / 1000
            )

    # Now the info is working with lists instead of dictionaries
    def infoToLists(self):
        if self.leader:
            #sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
            self.headway = sqrt((self.leader.bi_location[0] - self.bi_location[0]) ** 2 + (self.leader.bi_location[1] - self.bi_location[1]) ** 2)

        self.lrecords.append(
            list(
                map(
                    lambda x: round(x, 4),
                    [self.acceleration, self.speed, self.bi_location[1], self.headway, self.length],
                )
            )
        )
        self.ltime.append(round(self.simTime / 1000, 2))
        self.position.append(self.bi_location)
        

        self.simTime += self.simulationStep

    def list_update(self):
        self.infoToLists()

        if self.leader:
            spacing = self.leader.location - self.location - self.leader.length
            if spacing <= 0:
                print("Vehicle has crashed", self.ith)

        if self.time_pass_zero == None and (self.bi_location[0] >= 130 and self.bi_location[1] <= -530):
            self.time_pass_zero = self.simTime
            self.headway_pass_zero = self.headway
            self.speed_pass_zero = self.speed

            print("HERE VEHICLE")
            print(self.time_pass_zero)
            print(self.headway_pass_zero)
            print(self.speed_pass_zero)
