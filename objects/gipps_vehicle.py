from objects.vehicle import Vehicle
from numpy import random
import numpy as np


class Gipps_vehicle(Vehicle):
    def __init__(
        self,
        ith,
        desired_speed,
        graph,
        path,
        positions,
        directions,
        gipps,
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
        self.path = path
        self.positions = positions
        self.directions = directions
        self.graph = graph
        self.direction = "Right"

    # Check for influence
    def pick_normal(self, mean, std):
        pick = random.normal(mean, std)
        while pick > mean + std or pick < mean - std:
            pick = random.normal(mean, std)
        return pick

    def print_info(location_magnitude, xy):
        print("Magnitude:", location_magnitude)
        print("X:", xy[0])
        print("Y:", xy[1])

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

    def update_x_negative(self):
        new_speed = self.model.get_speed(self)
        new_acceleration = (new_speed - self.speed) / self.reac_time
        # Euler integration method
        new_location = self.location + 0.5 * (self.speed + new_speed) * self.reac_time
        self.acceleration = new_acceleration
        self.speed = new_speed
        difference = new_location - self.location
        self.location = self.location - difference

    def update_y_negative(self):
        new_speed = self.model.get_speed_y(self)
        new_acceleration = (new_speed - self.speed) / self.reac_time
        new_location_y = (
            self.y_location + 0.5 * (self.speed + new_speed) * self.reac_time
        )
        self.acceleration = new_acceleration
        self.speed = new_speed
        difference = new_location_y - self.location
        self.y_location = self.location - difference

    def update_bidimensional(self):
        self.list_update()
        self.bi_location = np.array([self.location, self.y_location])
        for node in self.path:
            if self.location > self.positions[node][0]:
                print("Up")
                self.direction = "Up"
            elif self.y_location > self.positions[node][1]:
                print("right")
                self.direction = "Right"

        if self.direction == "Right":
            self.update_x()
        elif self.direction == "Up":
            self.update_y()

    def update_test(self):
        self.list_update()
        new_location = np.empty(2, dtype=float)
        new_speed = self.model.get_speed_test(self)
        new_acceleration = (new_speed - self.speed) / self.reac_time
        x_component = (
            self.bi_location[0] + 0.5 * (self.speed + new_speed) * self.reac_time
        )
        y_component = (
            self.bi_location[1] + 0.5 * (self.speed + new_speed) * self.reac_time
        )
        location_mag = (x_component * np.cos(np.deg2rad(self.angle))) + (
            y_component * np.sin(np.deg2rad(self.angle))
        )
        new_location[0] = np.round(location_mag * np.cos(np.deg2rad(self.angle)), 8)
        new_location[1] = np.round(location_mag * np.sin(np.deg2rad(self.angle)), 8)
        self.acceleration = new_acceleration
        self.speed = new_speed
        self.bi_location = new_location
