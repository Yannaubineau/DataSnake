import random
import keyboard
import sys
import time
import numpy as np
import os
# Configuration
FPS = 0.2
WIDTH = 10
LENGTH = 10

# Coordinates : [line (X), column (Y)]
map = [[[row, column] for row in  range(0,WIDTH)] for column in range(0,LENGTH)]

class Snake:
    def __init__(self, map):
        # Define map
        self.map = map
        self.length_map = len(self.map[0])
        self.width_map = len(self.map)
        
        # Define interaction with map + snake + apple
        self.update_temp_forbidden_tiles_list = []
        self.available_tiles_list = [[[row, column] for row in  range(1,self.width_map-1)] for column in range(1,self.length_map-1)]
        self.available_tiles_list = sum(self.available_tiles_list, [])

        self.apple = []
        self.snake = np.array([[2,3],[2,4],[2,5]])
        self.length_snake = len(self.snake)

        # Define movement coordinate
        self.down_list = [1,0]
        self.up_list = [-1,0]
        self.left_list = [0,-1]
        self.right_list = [0,1]
        self.current_move = []
    
    # Main movement function
    def movement_snake(self, input_player):
        # Update current movement
        self.current_move = self.snake[0] + input_player
        # Condition : not going back on itself 
        if (((self.current_move).tolist() == self.snake[1].tolist()) != True):
            # Condition : either goes in a wall or eat itself
            if (self.current_move).tolist() not in self.available_tiles_list:
                self.death()
            # Else : move
            else:
                # Condition : special event, eats the apple
                if (self.current_move).tolist() == self.apple:
                    self.snake_eat_apple(input_player)
                # Else : simple movement
                else:
                    self.snake = np.append([self.current_move],self.snake,axis = 0) # New head
                    self.snake = np.delete(self.snake,len(self.snake)-1 ,axis = 0) # Delete old tail
                    # Update temporary forbidden tiles as the snake moved
                    self.update_temp_forbidden_tiles()
        
    # Special event movement function : the snake ate an apple
    def snake_eat_apple(self,input_player):
        self.snake = np.append([self.current_move], self.snake, axis = 0) # We add new head without killing old tail
        # Needs to update the map to display a 1 instead of the apple
        self.map[self.snake[0][0]][self.snake[0][1]] = 1
        self.update_temp_forbidden_tiles()  # We update the forbidden tiles (snake larger)
        self.spawn_apple() # And we spawn new apple
                      
    # Main update and display function 
    def update_map(self):
        # Only update the area, not the border, as they don't change
        for lines in range(1,self.width_map-1):
            for columns in range(1,self.length_map-1):
                # We first check if the coordinates are in the snake, rather than testing it in a for loop all the time, which would be less 
                # efficient
                if [lines,columns] in self.snake.tolist():
                    for snake_part in self.snake.tolist():
                        # Change the map to a 1 when it's a part of the snake
                         if [lines,columns] == snake_part:
                            self.map[lines][columns] = 1
                # To a 2 when it's the apple
                elif [lines,columns] == self.apple:
                    self.map[lines][columns] = 2
                # To a 0 when it's nothing
                else:
                    self.map[lines][columns] = 0
        # We clear the console so that it only displays a single arena
        os.system('cls')
        # And we print the map
        print(*self.map,sep='\n')
    
    # Special event function : spawn the apple
    def spawn_apple(self):
        # Choose a coordinate among the available ones
        self.apple = random.choice(self.available_tiles_list)
        # Only update new place of the apple
        for lines in range(1,self.width_map-1):
            for columns in range(1,self.length_map-1):
                if [lines,columns] == self.apple:
                    self.map[lines][columns] = 2

    # Function to update the tiles where the snake looses = if if eats itself
    def update_temp_forbidden_tiles(self):
        self.temp_forbidden_tiles_list = self.snake.tolist()
        # And update the available one
        self.update_available_tiles()
    
    # Function to update the available tiles
    def update_available_tiles(self):
        # First create a copy of the area
        self.available_tiles_list = [[[row, column] for row in  range(1,self.width_map-1)] for column in range(1,self.length_map-1)]
        self.available_tiles_list = sum(self.available_tiles_list, [])
        # Then we delete the temporary forbidden tiles. We don't need to mention the barriers are they are already not in the available ones.
        for item in self.temp_forbidden_tiles_list:
            for tiles in self.available_tiles_list:
                if item == tiles:
                    self.available_tiles_list.remove(tiles)

    # Function to display once the barriers, but do not need to be used again
    def barrier_tiles(self):
        for lines in range(self.width_map):    
            for columns in range(self.length_map):
                map[lines][columns] = 3
    
    # Function triggered when the player lost (run in a whole or snake ate itself)
    def death(self):
        print("You lost")
        time.sleep(1)
        sys.exit()

    # MAIN function : initialize the map and control the keys pressed
    def play(self):
        self.update_temp_forbidden_tiles()
        self.spawn_apple()
        self.barrier_tiles()
        self.update_map()

        # Main loop
        while True:
            if keyboard.is_pressed("bas"):
                while True:
                    time.sleep(FPS)
                    self.movement_snake(self.down_list)
                    self.update_map()
                    if keyboard.is_pressed("haut") or keyboard.is_pressed("droite") or keyboard.is_pressed("gauche"):
                        break
            elif keyboard.is_pressed("haut"):
                while True:
                    time.sleep(FPS)
                    self.movement_snake(self.up_list)
                    self.update_map()
                    if keyboard.is_pressed("bas") or keyboard.is_pressed("droite") or keyboard.is_pressed("gauche"):
                        break
            elif keyboard.is_pressed("droite"):
                while True:
                    time.sleep(FPS)
                    self.movement_snake(self.right_list)
                    self.update_map()
                    if keyboard.is_pressed("bas") or keyboard.is_pressed("haut") or keyboard.is_pressed("gauche"):
                        break
            elif keyboard.is_pressed("gauche"):
                while True:
                    time.sleep(FPS)
                    self.movement_snake(self.left_list)
                    self.update_map()
                    if keyboard.is_pressed("bas") or keyboard.is_pressed("haut") or keyboard.is_pressed("droite"):
                        break
 
            

S = Snake(map)
S.play()