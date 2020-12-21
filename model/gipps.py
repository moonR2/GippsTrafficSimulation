from math import sqrt
import numpy as np

"""
Gipps model implementation (1981)
 """


class GippsModel:
    def __init__(self):

        # Necessary parameters to compute the g factor
        self.alpha_g = 0.6  # Greatest speed reduction
        self.l1 = 50 / 3  # Zone of influence upstream
        self.l2 = 10 / 3  # Zone of influence downstream

    def accelerating_part(self, car):
        print("Car location:", car.bi_location)
        inner = 0.025 + car.speed / car.desired_speed

        if inner <= 0:
            print("Error during car travel.", inner, car.speed, car.desired_speed)

        return car.speed + 2.5 * car.max_acc * car.reac_time * (
            1 - car.speed / car.desired_speed
        ) * sqrt(inner)

    def decelerating_part(self, car):
        inner = (car.desired_braking ** 2) * (
            car.reac_time ** 2
        ) - car.desired_braking * (
            2 * (car.leader.location - car.leader.eff_size - car.location)
            - car.speed * car.reac_time
            - (car.leader.speed ** 2) / car.b_hat
        )

        if inner <= 0:
            print("Error during car travel", inner, car.speed, car.desired_speed)

        return car.desired_braking * car.reac_time + sqrt(inner)

    def decelerating_part_test(self, car):
        print("Car location:", car.bi_location)
        inner = (car.desired_braking ** 2) * (
            car.reac_time ** 2
        ) - car.desired_braking * (
            2 * (car.leader.bi_location - car.leader.eff_size - car.bi_location)
            - car.speed * car.reac_time
            - (car.leader.speed ** 2) / car.b_hat
        )

        # Handling negatives values when there is no movement in X or Y
        for i in range(len(inner)):
            if inner[i] < 0:
                inner[i] = 0
        handler = car.desired_braking * car.reac_time + np.sqrt(inner)
        for i in range(len(handler)):
            if handler[i] < 0:
                handler[i] = 0
        return handler

    def get_speed(self, car):
        car.desired_speed = car.max_speed
        v_free = self.accelerating_part(car)
        if car.leader:
            v_follow = self.decelerating_part(car)
            return min(v_free, v_follow)
        return v_free

    def get_speed_y(self, car):
        car.desired_speed = car.max_speed
        v_free = self.accelerating_part(car)
        if car.leader:
            v_follow = self.decelerating_part(car)
            return min(v_free, v_follow)
        return v_free

    def get_speed_test(self, car):
        print("---------------------------------------------------------------")
        print("car:", car.ith)
        car.desired_speed = car.max_speed
        v_free = self.accelerating_part(car)
        if car.leader:
            v_vector = self.decelerating_part_test(car)
            print("V_vector: ", v_vector)
            v_follow = (v_vector[0] * np.cos(np.deg2rad(car.angle))) + (
                v_vector[1] * np.sin(np.deg2rad(car.angle))
            )
            print("V_free:", v_free)
            print("V_follow: ", v_follow)
            return min(v_free, v_follow)
        print("v_free", v_free)
        return v_free
