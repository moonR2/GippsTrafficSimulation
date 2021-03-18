from objects.vehicle import Vehicle
from numpy import random
import numpy as np
from math import dist, sqrt


class Gipps_vehicle(Vehicle):
    def __init__(
        self,
        ith,  # Vehicle ID
        desired_speed,  # Vehicle desired speed
        graph,
        path,
        positions,
        directions,
        gipps,
        street,  # Street class
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
            max_acc = self.pick_normal(max_acc, 0.3)
            eff_size = self.pick_normal(eff_size, 0.3)
            miniGap = eff_size - length
            desired_speed = self.pick_normal(22.22, 3.2)

        super().__init__(
            ith,
            leader,
            simulationStep=reaction_time * 1000,  # Wilson time step
            max_speed=desired_speed,
            miniGap=miniGap,
            length=length,
            path=path,
            positions=positions
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
        self.pass_point = 0 
        self.edges, self.road_ids = self.group_edges()
        self.road_id = -1        
        self.first_road = self.road_ids[
            (self.path[0], self.path[1])
        ]  # Assigning first road to road_id

    def get_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Check for influence
    def pick_normal(self, mean, std):
        pick = random.normal(mean, std)
        return pick

    def print_info(self):
        print("max_acc: ", self.max_acc)
        print("eff_size: ", self.eff_size)
        print("minigap: ", self.miniGap)
        print("desired_speed: ", self.desired_speed)

    # Generate a dictionary edges:angle
    def group_edges(self):
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

    def update_test(self):  # Update in two dimensions
        self.list_update()
        print("------------------------------------------------------------")
        print("Vehicle path", self.path)
        # Distance between vehicle and next node
        distance = self.get_distance(self.bi_location, self.positions[self.path[0]])
        check = self.positions[self.path[0]]
        print("Vehicle N:", self.ith)
        print("Current Location:", self.bi_location)
        print("Distance to next node:", distance)
        last_location = self.bi_location
        new_location = np.empty(2, dtype=float)
        new_speed = self.model.get_speed_xy(self)
        new_acceleration = (new_speed - self.speed) / self.reac_time
        new_speed_x = new_speed * np.cos(np.deg2rad(self.angle))
        new_speed_y = new_speed * np.sin(np.deg2rad(self.angle))
        speed_x = self.speed * np.cos(np.deg2rad(self.angle))
        speed_y = self.speed * np.sin(np.deg2rad(self.angle))
        x_component = (
            self.bi_location[0] + 0.5 * (speed_x + new_speed_x) * self.reac_time
        )
        y_component = (
            self.bi_location[1] + 0.5 * (speed_y + new_speed_y) * self.reac_time
        )
        new_location[0] = np.round(x_component,12)
        new_location[1] = np.round(y_component,12)
        self.speed = new_speed
        self.bi_location = new_location
        self.acceleration = new_acceleration
        #print("vehicle speed", self.speed)

        dist_locations = self.get_distance(self.bi_location, last_location)
        # Printing Roads
        #for i in range(len(self.street.streets)):
        #    print("Vehicles in Road", self.street.streets[i].ith)
        #    print(self.street.streets[i].plat)
        if distance < dist_locations:
            if len(self.path) != 1:
        #        print("Vehicle changed road")
                last_road = self.road_id
        #        print("Last road:", last_road)
                new_angle = self.edges[self.path[0], self.path[1]]
                last_angle = self.angle
        #        print("Next Road angle:",new_angle)
                new_road_id = self.road_ids[self.path[0], self.path[1]]
                # New vehicle location is the same as the street node
                self.bi_location = np.array([check[0], check[1]])
                # Change angle to the new road angle
                self.angle = new_angle
                self.road_id = new_road_id
                n_vehicles_road = len(self.street.streets[self.road_id].plat)
                # Pop the first element from the vehicle optimal path
                self.path.pop(0)
        #        print("Vehicle next road:", self.street.streets[self.road_id].ith)
                self.street.streets[self.road_id].plat.append(
                    self.ith
                )  # List to track vehicles ids
                self.street.streets[self.road_id].vehicles.append(
                    self
                )  # List to track vehicles object
                # When vehicle change direction remove itself from the last road
                if (
                    self.ith in self.street.streets[last_road].plat
                    and self.road_id != self.first_road
                ):
                    index_to_remove = self.street.streets[last_road].plat.index(
                        self.ith
                    )
                    self.street.streets[last_road].plat.remove(self.ith)
                    self.street.streets[last_road].vehicles.pop(index_to_remove)
                # Remove itself from being leader
                if self.follower and last_angle != new_angle:
                    self.follower.leader = None
                # The vehicle has a new leader if vehicles exists in the new road
                if n_vehicles_road >= 1:
                    self.leader = self.street.streets[self.road_id].vehicles[
                        n_vehicles_road - 1
                    ]
        #            print("Vehicle has a new leader:", self.leader.ith)

        #print("Next location:", self.bi_location)
        #if self.leader:
        #    print("Vehicle leader:", self.leader.ith)
        #if self.leader == None:
        #    print("Vehicle does not have a leader")
        #print("Car in road:", self.road_id)
        self.print_info()
        
        
