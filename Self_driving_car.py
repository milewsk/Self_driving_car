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

        self.position = [0,0] 
        self.angle = 0 
        self.speed = 0
    
        self.speed_set = False

        self.radars = [] # List For Sensors / Radars
        self.drawing_radars = [] # Radars To Be Drawn


        # Musimy mieć środek pojazdu w aktualnym położeniu na mapie 
        # Dodamy jego położenie na mapie - użyjemy połowę długości i szerokości aby wyznaczyć środek obieku
        self.car_center = [position[0]+(CAR_SIZE_X/2),position[1]+(CAR_SIZE_Y/2)]

        #parametry które posłużą nam do wyznaczania kolejnych generacji
        self.alive = True
        self.distance = 0
        self.time = 0

        

        # Jeśli któryś z krańców auta dotknie granicy samochód umiera
        def check_collision(self, game_map):
            self.alive = True
            for point in self.corners:
                if game_map.get_at((int(point[0]),int(point[1]))) == end_color:
                    self.alive = False
                    break;
        # sprawdzanie życia obiektu
        def is_ailve(self):
            return self.alive


        def get_reward(self):
            return self.distance / (CAR_SIZE_X/2)

        #obracanie się w okół własnej osi
        def rotate_center(self,image,angle):
            rect = image.get_rect()
            rot_img = pygame.transform.rotate(image,angle)
            rot_rect = rect.copy()
            rot_rect.center = rot_img.get_rect().center
            rot_img = rot_img.subsurface(rotrot_rect).copy()

        def draw(self,screen):
            screen.blit(self.rotated_sprite, self.position)
            self.draw_radar(screen)
        
        #tworzenie linii i kólka w okół samochodu
        def draw_radar(self,screen):
            for radar in self.radars:
                position = radar[0]
                pygame.draw.line(screen, (0,255,0), self.center, position, 1)
                pygame.draw.circle(screen,(0,255,0), position, 5)

        def check_radar(self,degree,game_map):
            lenght = 0
            x = int(self.center[0]+math.cos(math.radians(360-(self.angle+degree)))*lenght)
            y = int(self.center[1]+math.sin(math.radians(360-(self.angle+degree)))*lenght)

            while not game_map.get_at((x,y)) == end_color and lenght < 300:
                lenght = lenght + 1
                x = int(self.center[0]+math.cos(math.radians(360-(self.angle+degree)))*lenght)
                y = int(self.center[1]+math.sin(math.radians(360-(self.angle+degree)))*lenght)

            dist = inst(math.sqrt(math.pow(x - self.center[0],2)+math.pow(y - self.center[1],2)))
            self.radars.append([(x,y), dist])

        def update(self,game_map):
            if self.speed_set:
                self.speed = 20
                self.speed_set = True
            
                #Rotacja sprite i przesunięcie w poprawną stronę względem osi X
                #Nie można zbilżyć się bliżej niż 20 px
            self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
            #Rotacja X
            self.position[0] += math.cos(math.radians(360-self.angle)) * self.speed
            self.position[0] = max(self.position[0], 20)
            self.position[0] = min(self.position[0], WIDTH - 120)

            self.distance += self.speed
            self.time += 1
            
            #Rotacja Y
            self.position[0] += math.sin(math.radians(360-self.angle)) * self.speed
            self.position[0] = max(self.position[1], 20)
            self.position[0] = min(self.position[1], WIDTH - 120)

            #Po zmianie pozycji aktualizacja centrum
            self.center = [int(self.position[0])+CAR_SIZE_X/2,int(self.position[1]) + CAR_SIZE_Y/2]

            #Obliczanie położenia dla 4 rogów modelu
            length = 0.5 * CAR_SIZE_X
            left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
            right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
            left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
            right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
            self.corners = [left_top, right_top, left_bottom, right_bottom]

            #Po obliczeniu położenia sprawdzamy czy obiekt nie doktnie krawędzi
            #Czy nie umrze

            self.check_collision(game_map)
            self.radars.clear()

            for d in range(-90, 120, 45):
                self.chceck_radar(d,game_map)

        def get_data(self):
            radars = self.radars
            return_values = [0, 0, 0, 0, 0]
            for i, radar in enumerate(radars):
                return_values[i] = int(radar[1]/30)

            return return_values
