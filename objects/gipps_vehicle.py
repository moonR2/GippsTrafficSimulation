from objects.vehicle import Vehicle
from numpy import random
import numpy as np
from math import dist, sqrt


class Gipps_vehicle(Vehicle):
    def __init__(
        self,
        ith, # Vehicle ID
        desired_speed, # Vehicle desired speed
        graph,
        path,
        positions,
        directions,
        gipps,
        street, # Street class 
        leader=None,
        reaction_time=2 / 3,
        randomness=False,
        length=5,
    ):

        max_acc = 1.7
        eff_size = 6.5
        miniGap = 2
        desired_speed = 20

        # Distributions taken from Gipps 1981
        if randomness:
            max_acc = self.pick_normal(max_acc, 0.3 ** 2)
            eff_size = self.pick_normal(eff_size, 0.3 ** 2)
            miniGap = eff_size - length
            desired_speed = self.pick_normal(desired_speed, 3.2 ** 2)

        super().__init__(
            ith,
            leader,
            simulationStep=reaction_time,  # Wilson time step
            max_speed=desired_speed,
            miniGap=miniGap,
            length=length,
            path=path
        )

        self.max_acc = max_acc
        self.connected = False
        self.eff_size = eff_size
        self.desired_speed = self.max_speed
        self.desired_braking = -2 * self.max_acc  # Max decelaration (Bn)
        self.reac_time = reaction_time
        self.b_hat = min(-3.0, (self.desired_braking - 3) / 2)
        self.model = gipps
        self.count = 0
        self.graph = graph
        self.positions = positions
        self.directions = directions
        self.street = street
        self.edges, self.road_ids = self.group_edges()
        self.road_id = self.road_ids[(self.path[0],self.path[1])] # Assigning first road to road_id
        self.first_road = self.road_ids[(self.path[0],self.path[1])] # Assigning first road to road_id

    # Check for influence
    def get_distance(self,p1,p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def pick_normal(self, mean, std):
        pick = random.normal(mean, std)
        while pick > mean + std or pick < mean - std:
            pick = random.normal(mean, std)
        return pick

    def print_info(self, location_magnitude, xy):
        print("Magnitude:", location_magnitude)
        print("X:", xy[0])
        print("Y:", xy[1])

    # Generate a dictionary edges:angle
    def group_edges(self):
        print("Here:",len(self.street.streets))
        edges = {}
        road_ids = {}
        for i in range(len(self.street.streets)):
            edges[self.street.streets[i].edge] = self.street.streets[i].angle
            road_ids[self.street.streets[i].edge] = self.street.streets[i].ith
        return edges, road_ids

    def update(self):  # Basic update only in X axis
        self.list_update()
        if self.suddenBraking:
            self.count += 1
            new_acceleration = self.desired_braking
            new_speed = self.speed + self.reac_time / 2 * (
                self.acceleration + new_acceleration
            )
            # new_speed = self.model.get_speed(self)
        else:
            new_speed = self.model.get_speed(self)

        new_acceleration = (new_speed - self.speed) / self.reac_time
        # Euler integration method to compute new location
        new_location = self.location + 0.5 * (self.speed + new_speed) * self.reac_time
        self.acceleration = new_acceleration
        self.speed = new_speed
        self.location = new_location

    def update_test(self): # Update in two dimensions
        self.list_update()
        print("------------------------------------------------------------")
        print("Vehicle path", self.path)
        # Distance between vehicle and next node
        distance = self.get_distance(self.bi_location, self.positions[self.path[0]])
        check = self.positions[self.path[0]]
        print(self.ith)
        print("Bi_location:", self.bi_location)
        print("Distance:",distance)
        last_location = self.bi_location
        new_location = np.empty(2, dtype=float)
        new_speed = self.model.get_speed_xy(self)
        new_speed_x = new_speed * np.cos(np.deg2rad(self.angle))
        new_speed_y = new_speed * np.sin(np.deg2rad(self.angle))
        speed_x = self.speed * np.cos(np.deg2rad(self.angle))
        speed_y = self.speed * np.sin(np.deg2rad(self.angle))
        print("x", new_speed_x)
        print("y", new_speed_y)
        print("xnow", speed_x)
        print("ynow", speed_y)
        new_acceleration = (new_speed - self.speed) / self.reac_time
        x_component = (
            self.bi_location[0] + 0.5 * (speed_x + new_speed_x) * self.reac_time
        )
        y_component = (
            self.bi_location[1] + 0.5 * (speed_y + new_speed_y) * self.reac_time
        )
        new_location[0] = x_component
        new_location[1] = y_component
        self.acceleration = new_acceleration
        self.speed = new_speed
        self.bi_location = new_location
        dist_locations = self.get_distance(self.bi_location,last_location)
        for i in range(len(self.street.streets)):
            print("Roads ---", self.street.streets[i].ith)
            print(self.street.streets[i].plat)
        if distance < dist_locations:
            if len(self.path) != 1:
                last_road = self.road_id
                print("Last road:",last_road)
                new_angle = self.edges[self.path[0], self.path[1]]
                new_road_id = self.road_ids[self.path[0],self.path[1]]
                print("Change angle")
                # New vehicle location is the same as the street node
                self.bi_location = np.array([check[0],check[1]])
                # Change angle to the new road angle
                self.angle = new_angle
                self.road_id = new_road_id
                # Pop the first element from the vehicle optimal path
                self.path.pop(0)
                print(self.street.streets[self.road_id].ith)
                self.street.streets[self.road_id].plat.append(self.ith)
                # When vehicle change direction remove itself from the last road
                if self.ith in self.street.streets[last_road].plat and self.road_id != self.first_road:
                    self.street.streets[last_road].plat.remove(self.ith)
                if self.follower:
                    #self.follower.ith.leader == None
                    print("Vehicle follower:", self.follower.ith)

        print("Next location:",self.bi_location)
        #print(self.street.streets[self.road_id].plat)
        print("Car in road:", self.road_id)
