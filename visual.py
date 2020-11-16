import pygame 
from pygame.math import Vector2
from simulation import Simulation
import os 
from objects.gipps_vehicle import Gipps_vehicle
from model.gipps import GippsModel
import matplotlib.pyplot as plt
#Libraries to handle graphs :)) 
import numpy as np
import networkx as nx

class Game: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Tutorial")
        width = 1600 
        height = 720 
        self.screen = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()
        self.ticks = 60 
        self.exit = False
        
    def run(self): 
        # Dictionary handling the coordinates of each edge
        pos = {
            "a":(10,10),
            "b":(10,400),
            "c":(400,400),
            "d":(400,10)
        }
        print(pos.keys())
        # Trying to make a graph lol 
        G = nx.Graph() 
        G.add_nodes_from(pos.keys())
        #Position of the node as node atrribute 
        for n, p in pos.items():
            G.nodes[n]['pos'] = p 

        G.add_edge("a","b")
        G.add_edge("b","c")
        G.add_edge("c","d")
        G.add_edge("d","a")
        print(G.nodes())
        print(G.edges())

        nx.draw(G,pos)
        plt.show()
        #Loading car asset 
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir,"car.png")
        car_image = pygame.image.load(image_path).convert() # Metodo convert agregador revisar 

        # Parameters for car 0 
        simulation_time = 60
        n = 5 
        intended_speed = (80 * 1000)/3600 
        sim = Simulation(time = simulation_time, avStep=100)
        # Intentando llamar a update() con un solo auto TEST >>>>??:?::?:
        # La clase Gipps vehicle tiene la funcion update() 
        # Entonces creamos una instancia de la clase 
        car = Gipps_vehicle(ith=0, desired_speed = intended_speed, gipps=GippsModel(),
            leader = None, reaction_time = 2/3,randomness = False, length=5, y_location = 200)
        ppu = 1 #Car ratio relation to real world

        while not self.exit:
            
            dt = self.clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            #CAR LOGIG HERE 

            car.update() 
            # print(car.location)

            #Prints 2DVector(x,y)
            #print(car.position)

            # Drawing 
            self.screen.fill((0,0,0))
            rotated = pygame.transform.rotate(car_image,car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            
            pygame.display.flip()

            self.clock.tick(self.ticks)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 
    print("EVERYTHING WORKING??? XDDDD")
            
