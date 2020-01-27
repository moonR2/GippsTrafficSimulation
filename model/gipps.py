from math import exp
from math import sqrt

""" 
Gipps model implementation (1981)
 """
class GippsModel: 
    def __init__(self):

        # Necessary parameters to compute the g factor 
        self.alpha_g = 0.6 # Greatest speed reduction 
        self.l1 = 50 / 3 # Zone of influence upstream 
        self.l2 = 10/3 # Zone of influence downstream 
    
    #Not being use 
    def g_factor(self,car):
        """ Compute the desired G factor to reduce speed at junctions """
        x1 = max(0-car.location, 0) # Distance between the vehicle pos and the stop-line
        x2 = max(car.location - 0, 0) # Distance between the stop-line and the vehicle pos
        inner = -(x1**2) / (2 * (self.l1 ** 2)) - (x2 ** 2) / (2 * (self.l2 ** 2))
        g = 1 - self.alpha_g * exp(inner)
        return g 
    
    def accelerating_part(self,car):
        inner = (0.025 + car.speed / car.desired_speed)

        if inner <= 0:
            print("Error during car travel.", inner, car.speed, car.desired_speed)

        return car.speed + 2.5 * car.max_acc * car.reac_time * (1 
            - car.speed / car.desired_speed) * sqrt(inner)

    def decelerating_part(self,car):
        inner = (car.desired_braking ** 2) * (car.reac_time ** 2) - car.desired_braking * (2 * ( car.leader.location -
                car.leader.eff_size - car.location) - car.speed *
                car.reac_time - (car.leader.speed ** 2) / car.b_hat)

        if inner <= 0:
            print("Error during car travel",inner,car.speed,car.desired_speed)

        return car.desired_braking * car.reac_time + sqrt(inner)

    """ Apply the G factor and compute the vehicle v(t) speed  """
    #G Factor removed from the EQ 
    def get_speed(self,car):
        car.desired_speed = car.max_speed 
        g_a = self.accelerating_part(car)
        if car.leader:
            g_b = self.decelerating_part(car)
            return min(g_a,g_b)
        return g_a 

