# Code to perform self driving car based on genetic algorithm

#import must have lib's

import sys
import math
import os
import random

# based on pygame and neat library
import pygame
import neat

# Szerokość i wysokość mapy
WIDTH = 1920
HEIGHT = 1080

# Wybrane wyiary pixelowe samochodu
CAR_SIZE_X = 90
CAR_SIZE_Y = 60

# Potrzebujemy koloru piksela który spowoduje koniec życia samochodu
end_color = (255,255,255,255)

# Potrzebujemy globalnego licznika iteracji generacji
generation_number = 0

# Potrzebujemy klasy samochód z której tworzone będą obiekty 
# Potrzebe właściwości: 
# - czy żyje
# - skręcanie, rotowanie się o x stopni względem osi
# - prędkość danego pojazdu
# - jego aktualne położenie na mapie
# - zdolność przyśpieszania i zwalniania 

class car:

    #inicjacja obiektu i przypisanie początkowych parametrów
    def __init__(self):

        #załadowanie modelu i zeskalowanie do podanych przez as pixeli
        self.model = pygame.image.load("car.png").convert()
        self.model = pygame.transform.scale(self.model, (CAR_SIZE_X,CAR_SIZE_Y))

        self.posision = [0,0] 
        self.angle = 0 
        self.speed = 0
    
        self.speed_set = False

        self.radars = [] # List For Sensors / Radars
        self.drawing_radars = [] # Radars To Be Drawn


        # Musimy mieć środek pojazdu w aktualnym położeniu na mapie 
        # Dodamy jego położenie na mapie - użyjemy połowę długości i szerokości aby wyznaczyć środek obieku
        self.car_center = [posision[0]+(CAR_SIZE_X/2),posision[1]+(CAR_SIZE_Y/2)]

        #parametry które posłużą nam do wyznaczania kolejnych generacji
        self.alive = True
        self.distance = 0
        self.time = 0

        # Jeśli któryś z krańców auta dotknie granicy samochód umiera
        def chcec_collision(self, game_map):
            self.alive = True
            for point in self.corners:
                if game_map.get_at((int(point[0]),int(point[1]))) == end_color:
                    self.alive = False
                    break;