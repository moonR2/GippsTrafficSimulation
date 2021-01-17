from math import sqrt, cos, sin
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

    def accelerating_part_xy(self, car):

        inner = 0.025 + car.speed / car.desired_speed

        if inner <= 0:
            print("Error during car travel.", inner, car.speed, car.desired_speed)

        x = (car.speed + 2.5 * car.max_acc * car.reac_time * (
            1 - car.speed / car.desired_speed
        ) * sqrt(inner)) * np.cos(np.deg2rad(car.angle))

        y = (car.speed + 2.5 * car.max_acc * car.reac_time * (
            1 - car.speed / car.desired_speed
        ) * sqrt(inner)) * np.sin(np.deg2rad(car.angle))
        
        return [x,y]

    def decelerating_part_xy(self, car):
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
                print("Inner:",inner)
                inner[i] = 0
        handler = car.desired_braking * car.reac_time + np.sqrt(inner)
        x = handler[0] * np.cos(np.deg2rad(car.angle))
        y = handler[1] * np.sin(np.deg2rad(car.angle))
        return [x,y]

    def accelerating_part(self, car):
        #print("Car location:", car.bi_location)
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

    def get_speed(self, car):
        car.desired_speed = car.max_speed
        v_free = self.accelerating_part(car)
        if car.leader:
            v_follow = self.decelerating_part(car)
            return min(v_free, v_follow)
        return v_free

    def get_speed_xy(self, car):
        car.desired_speed = car.max_speed
        v_free = self.accelerating_part_xy(car)
        v_free = np.round(v_free,8)
        if car.leader:
            v_follow = self.decelerating_part_xy(car)
            v_follow = np.round(v_follow,8)
            print("V_free:", v_free)
            print("V_follow: ", v_follow)
            print(np.minimum(v_free,v_follow))
            minimun = np.minimum(v_free,v_follow)
            v_follow_scalar = sqrt(v_follow[0] ** 2 + v_follow[1] ** 2)
            v_free_scalar = sqrt(v_free[0] ** 2 + v_free[1] ** 2)
            print("V_free_scalar:", v_free_scalar)
            print("V_follow_scalar: ", v_follow_scalar)
            if minimun[0] - v_free[0] == 0 and minimun[1] - v_free[1] == 0:
                return v_free_scalar
            else:
                return v_follow_scalar
        v_free_scalar = sqrt(v_free[0] ** 2 + v_free[1] ** 2)
        print("v_free_scalar", v_free_scalar)
        return v_free_scalar
