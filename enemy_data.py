'''
General formatting of how each enemy will be coded
Class enemy name
    def init
        hp
        atk
        def
        res
        stuff
        damagetype (0 = physical, 1 = magic)
        enemy grid position
        etc

    def enemyAction():
    
        def move (All enemies will have def move as a base)
            movenment logic (But some will have abilities will different movenment logic)

        def attack (All enemies will have def attack move as a base)
            attack logic (just their basic attack)

        def ability one
            stuff

        def ability two
            stuff
'''
import pygame
import random

# All normals enemies
class Ursa: # A big bear that is faster and acts more than other enemeis 
    def __init__(self, starting_location):
        self.occupied_tiles = []
        self.max_hp = 50
        self.current_hp = self.max_hp
        self.ATK = 12
        self.DEF = 5
        self.RES = 0
        self.number_of_actions = 2
        self.tile_location = starting_location
        self.target_location = (0, 0)
        self.is_dead = False

    def updateOccupiedTiles(self, taken_tiles): # Update to check whether or not the tile it goes on is already used (Hint: doesn't work)
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.tile_location)
        for tiles in taken_tiles:
            self.occupied_tiles.append(tiles)

    def checkDead(self):
        if self.current_hp <= 0:
            self.is_dead = True

    def enemyAction(self, player_tile_location, tile_grid_connection, player_instance):         
        self.target_location = player_tile_location
        self.grid_conntion = tile_grid_connection            
        self.target_location_first = self.target_location[0]
        self.target_location_second = self.target_location[1]
        self.tile_location_first = self.tile_location[0]
        self.tile_location_second = self.tile_location[1]
        self.checkDead()

        if self.is_dead == True:
            pass
        else:
            for i in range(0, self.number_of_actions): # To do said action
                if player_tile_location not in tile_grid_connection[self.tile_location]:
                    self.move(self.target_location_first, self.target_location_second, self.tile_location_first, self.tile_location_second)
                else:
                    self.basicAttack(player_instance) # This is currently somewhat bugged where it takes the first action and then acts again after the player moves...
        
    def move(self, target_location_first, target_location_second, current_tile_location_first, current_tile_location_second):
        if target_location_first == current_tile_location_first: # Check the possibilites of which direction the player can be in
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
        elif target_location_second == current_tile_location_second:
            if target_location_first < current_tile_location_first:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
        elif target_location_first < current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
        elif target_location_first > current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)

    def basicAttack(self, player_instance):
        damage = max(self.ATK - player_instance.DEF, 1)
        player_instance.currentHP -= damage
    
    def draw(self, screen, spirte, grid_x_y):
        self.drawing_x_y_position = grid_x_y[self.tile_location] # General information to determine where to draw on the x, y cords
        self.drawing_x_position = self.drawing_x_y_position[0] # x position
        self.drawing_y_position = self.drawing_x_y_position[1] # y position
        screen.blit(spirte, (self.drawing_x_position - 70 // 2, self.drawing_y_position - 70 // 2))
        # Drawing the hp bar under the enemy so the player knows how much hp they have
        # Font and text
        font_icon_text = pygame.font.Font(None, 24)
        hp_text = font_icon_text.render(f"{self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, ((self.drawing_x_position - 20, self.drawing_y_position + 20)))
        # Actcual hp bar
        # TBC

class Raider: # A standard enemy that tries its best (Kinda sucks, the ursa is more of a threat due to poor coding that causes it to deal damage even when it isn't it's turn)
    def __init__(self, starting_location):
        self.occupied_tiles = []
        self.max_hp = 70
        self.current_hp = self.max_hp
        self.ATK = 20
        self.DEF = 10
        self.RES = 0
        self.number_of_actions = 1
        self.tile_location = starting_location
        self.target_location = (0, 0)
        self.is_dead = False

    def updateOccupiedTiles(self, taken_tiles):  # Update to check whether or not the tile it goes on is already used (Hint: doesn't work)
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.tile_location)
        for tiles in taken_tiles:
            self.occupied_tiles.append(tiles)

    def checkDead(self):
        if self.current_hp <= 0:
            self.is_dead = True

    def enemyAction(self, player_tile_location, tile_grid_connection, player_instance):         
        self.target_location = player_tile_location
        self.grid_conntion = tile_grid_connection            
        self.target_location_first = self.target_location[0]
        self.target_location_second = self.target_location[1]
        self.tile_location_first = self.tile_location[0]
        self.tile_location_second = self.tile_location[1]
        self.checkDead()

        if self.is_dead == True:
            pass
        else:
            for i in range(0, self.number_of_actions):
                if player_tile_location not in tile_grid_connection[self.tile_location]:
                    self.move(self.target_location_first, self.target_location_second, self.tile_location_first, self.tile_location_second)
                else:
                    self.basicAttack(player_instance)
        
    def move(self, target_location_first, target_location_second, current_tile_location_first, current_tile_location_second):
        if target_location_first == current_tile_location_first: # Check the possibilites of which direction the player can be in
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
        elif target_location_second == current_tile_location_second:
            if target_location_first < current_tile_location_first:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
        elif target_location_first < current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
        elif target_location_first > current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)

    def basicAttack(self, player_instance):
        damage = max(self.ATK - player_instance.DEF, 1)
        player_instance.currentHP -= damage
    
    def draw(self, screen, spirte, grid_x_y):
        self.drawing_x_y_position = grid_x_y[self.tile_location]
        self.drawing_x_position = self.drawing_x_y_position[0]
        self.drawing_y_position = self.drawing_x_y_position[1]
        screen.blit(spirte, (self.drawing_x_position - 70 // 2, self.drawing_y_position - 70 // 2))
        # Drawing the hp bar under the enemy so the player knows how much hp they have
        # Font and text
        font_icon_text = pygame.font.Font(None, 24)
        hp_text = font_icon_text.render(f"{self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, ((self.drawing_x_position - 20, self.drawing_y_position + 20)))
        # Actcual hp bar
        # TBC

class ShieldedRaider: # Just a big tanky boi that is meant to act as a roadblock and to corner the player if possible
    def __init__(self, starting_location):
        self.occupied_tiles = []
        self.max_hp = 70
        self.current_hp = self.max_hp
        self.ATK = 20
        self.DEF = 10
        self.RES = 0
        self.number_of_actions = 1
        self.tile_location = starting_location
        self.target_location = (0, 0)
        self.is_dead = False

    def updateOccupiedTiles(self, taken_tiles):  # Update to check whether or not the tile it goes on is already used (Hint: doesn't work)
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.tile_location)
        for tiles in taken_tiles:
            self.occupied_tiles.append(tiles)

    def checkDead(self):
        if self.current_hp <= 0:
            self.is_dead = True

    def enemyAction(self, player_tile_location, tile_grid_connection, player_instance):         
        self.target_location = player_tile_location
        self.grid_conntion = tile_grid_connection            
        self.target_location_first = self.target_location[0]
        self.target_location_second = self.target_location[1]
        self.tile_location_first = self.tile_location[0]
        self.tile_location_second = self.tile_location[1]
        self.checkDead()

        if self.is_dead == True:
            pass
        else:
            for i in range(0, self.number_of_actions):
                if player_tile_location not in tile_grid_connection[self.tile_location]:
                    self.move(self.target_location_first, self.target_location_second, self.tile_location_first, self.tile_location_second)
                else:
                    self.basicAttack(player_instance)
        
    def move(self, target_location_first, target_location_second, current_tile_location_first, current_tile_location_second):
        if target_location_first == current_tile_location_first: # Check the possibilites of which direction the player can be in
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
        elif target_location_second == current_tile_location_second:
            if target_location_first < current_tile_location_first:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
        elif target_location_first < current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
        elif target_location_first > current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)

    def basicAttack(self, player_instance):
        damage = max(self.ATK - player_instance.DEF, 1)
        player_instance.currentHP -= damage
    
    def draw(self, screen, spirte, grid_x_y):
        self.drawing_x_y_position = grid_x_y[self.tile_location]
        self.drawing_x_position = self.drawing_x_y_position[0]
        self.drawing_y_position = self.drawing_x_y_position[1]
        screen.blit(spirte, (self.drawing_x_position - 70 // 2, self.drawing_y_position - 70 // 2))
        # Drawing the hp bar under the enemy so the player knows how much hp they have
        # Font and text
        font_icon_text = pygame.font.Font(None, 24)
        hp_text = font_icon_text.render(f"{self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, ((self.drawing_x_position - 20, self.drawing_y_position + 20)))
        # Actcual hp bar
        # TBC

class Agent: # Agent enemy, first enemy to deal magic type damage
    def __init__(self, starting_location):
        self.occupied_tiles = []
        self.max_hp = 60
        self.current_hp = self.max_hp
        self.ATK = 12
        self.DEF = 5
        self.RES = 15
        self.number_of_actions = 1
        self.tile_location = starting_location
        self.target_location = (0, 0)
        self.is_dead = False

    def updateOccupiedTiles(self, taken_tiles):
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.tile_location)
        for tiles in taken_tiles:
            self.occupied_tiles.append(tiles)

    def checkDead(self):
        if self.current_hp <= 0:
            self.is_dead = True

    def enemyAction(self, player_tile_location, tile_grid_connection, player_instance):         
        self.target_location = player_tile_location
        self.grid_conntion = tile_grid_connection            
        self.target_location_first = self.target_location[0]
        self.target_location_second = self.target_location[1]
        self.tile_location_first = self.tile_location[0]
        self.tile_location_second = self.tile_location[1]
        self.checkDead()

        if self.is_dead == True:
            pass
        else:
            for i in range(0, self.number_of_actions):
                if player_tile_location not in tile_grid_connection[self.tile_location]:
                    self.move(self.target_location_first, self.target_location_second, self.tile_location_first, self.tile_location_second)
                else:
                    self.basicAttack(player_instance)
        
    def move(self, target_location_first, target_location_second, current_tile_location_first, current_tile_location_second):
        if target_location_first == current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
        elif target_location_second == current_tile_location_second:
            if target_location_first < current_tile_location_first:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
        elif target_location_first < current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
        elif target_location_first > current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)

    def basicAttack(self, player_instance):
        res = player_instance.RES
        res = res // 100
        damage = max(self.ATK - (self.ATK*res), 1)
        player_instance.currentHP -= damage
    
    def draw(self, screen, spirte, grid_x_y):
        self.drawing_x_y_position = grid_x_y[self.tile_location]
        self.drawing_x_position = self.drawing_x_y_position[0]
        self.drawing_y_position = self.drawing_x_y_position[1]
        screen.blit(spirte, (self.drawing_x_position - 70 // 2, self.drawing_y_position - 70 // 2))
        # Drawing the hp bar under the enemy so the player knows how much hp they have
        # Font and text
        font_icon_text = pygame.font.Font(None, 24)
        hp_text = font_icon_text.render(f"{self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, ((self.drawing_x_position - 20, self.drawing_y_position + 20)))
        # Actcual hp bar
        # TBC

class JetpackRaider:
    def __init__(self, starting_location):
        self.occupied_tiles = []
        self.max_hp = 50
        self.current_hp = self.max_hp
        self.ATK = 15
        self.DEF = 5
        self.RES = 0
        self.number_of_actions = 1
        self.tile_location = starting_location
        self.target_location = (0, 0)
        self.is_dead = False

    def updateOccupiedTiles(self, taken_tiles):
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.tile_location)
        for tiles in taken_tiles:
            self.occupied_tiles.append(tiles)

    def checkDead(self):
        if self.current_hp <= 0:
            self.is_dead = True

    def enemyAction(self, player_tile_location, tile_grid_connection, player_instance):         
        self.target_location = player_tile_location
        self.grid_conntion = tile_grid_connection            
        self.target_location_first = self.target_location[0]
        self.target_location_second = self.target_location[1]
        self.tile_location_first = self.tile_location[0]
        self.tile_location_second = self.tile_location[1]
        self.checkDead()

        if self.is_dead == True:
            pass
        else:
            for i in range(0, self.number_of_actions):
                if player_tile_location not in tile_grid_connection[self.tile_location]:
                    self.move(self.target_location_first, self.target_location_second, self.tile_location_first, self.tile_location_second)
                else:
                    self.basicAttack(player_instance)
        
    def move(self, target_location_first, target_location_second, current_tile_location_first, current_tile_location_second):
        if target_location_first == current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
        elif target_location_second == current_tile_location_second:
            if target_location_first < current_tile_location_first:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
        elif target_location_first < current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
        elif target_location_first > current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)

    def basicAttack(self, player_instance):
        damage = max(self.ATK - player_instance.DEF, 1)
        player_instance.currentHP -= damage
    
    def draw(self, screen, spirte, grid_x_y):
        self.drawing_x_y_position = grid_x_y[self.tile_location]
        self.drawing_x_position = self.drawing_x_y_position[0]
        self.drawing_y_position = self.drawing_x_y_position[1]
        screen.blit(spirte, (self.drawing_x_position - 70 // 2, self.drawing_y_position - 70 // 2))
        # Drawing the hp bar under the enemy so the player knows how much hp they have
        # Font and text
        font_icon_text = pygame.font.Font(None, 24)
        hp_text = font_icon_text.render(f"{self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, ((self.drawing_x_position - 20, self.drawing_y_position + 20)))
        # Actcual hp bar
        # TBC

class FlagBearer: # Flag bearer enemy
    def __init__(self, starting_location):
        self.occupied_tiles = []
        self.max_hp = 45
        self.current_hp = self.max_hp
        self.ATK = 0
        self.DEF = 5
        self.RES = 0
        self.number_of_actions = 1
        self.tile_location = starting_location
        self.target_location = (0, 0)
        self.is_dead = False

    def checkDead(self):
        if self.current_hp <= 0:
            self.is_dead = True

    def updateOccupiedTiles(self, taken_tiles):
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.tile_location)
        for tiles in taken_tiles:
            self.occupied_tiles.append(tiles)

    def reducingPlayerStats(self, player_instance):
        pass
    
    def draw(self, screen, spirte, grid_x_y):
        self.drawing_x_y_position = grid_x_y[self.tile_location]
        self.drawing_x_position = self.drawing_x_y_position[0]
        self.drawing_y_position = self.drawing_x_y_position[1]
        screen.blit(spirte, (self.drawing_x_position - 70 // 2, self.drawing_y_position - 70 // 2))
        # Drawing the hp bar under the enemy so the player knows how much hp they have
        # Font and text
        font_icon_text = pygame.font.Font(None, 24)
        hp_text = font_icon_text.render(f"{self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, ((self.drawing_x_position - 20, self.drawing_y_position + 20)))
        # Actcual hp bar
        # TBC

# Elite
class Stalker:
    def __init__(self, starting_location, turn_number):
        self.occupied_tiles = []
        self.max_hp = 90
        self.current_hp = self.max_hp
        self.ATK = 35
        self.DEF = 20
        self.RES = 10
        self.number_of_actions = 1
        self.tile_location = starting_location
        self.target_location = (0, 0)
        self.cooldown_jump = 5
        self.cooldown_jump_avaible = True
        self.turn_number = turn_number
        self.is_dead = False

    def updateOccupiedTiles(self, taken_tiles):
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.tile_location)
        for tiles in taken_tiles:
            self.occupied_tiles.append(tiles)

    def checkDead(self):
        if self.current_hp <= 0:
            self.is_dead = True

    def enemyAction(self, player_tile_location, tile_grid_connection, player_instance):         
        self.target_location = player_tile_location
        self.grid_conntion = tile_grid_connection            
        self.target_location_first = self.target_location[0]
        self.target_location_second = self.target_location[1]
        self.tile_location_first = self.tile_location[0]
        self.tile_location_second = self.tile_location[1]
        self.checkDead()
        if self.is_dead == True:
            pass
        else:
            if self.cooldown_jump_avaible == False:
                self.cooldown_jump -= 1
                if self.cooldown_jump == 0:
                    self.cooldown_jump_avaible = True
                    self.cooldown_jump += 2

            for i in range(0, self.number_of_actions):
                if player_tile_location not in tile_grid_connection[self.tile_location]:
                    if self.cooldown_jump_avaible == True:
                        self.jump()
                    else:
                        self.move(self.target_location_first, self.target_location_second, self.tile_location_first, self.tile_location_second)
                else:
                    self.basicAttack(player_instance)
        
    def move(self, target_location_first, target_location_second, current_tile_location_first, current_tile_location_second):
        if target_location_first == current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
        elif target_location_second == current_tile_location_second:
            if target_location_first < current_tile_location_first:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
        elif target_location_first < current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
        elif target_location_first > current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)

    def basicAttack(self, player_instance):
        damage = max(self.ATK - player_instance.DEF, 1)
        player_instance.currentHP -= damage

    def jump(self):
        self.target_location_first
        self.target_location_second
        
        possible_jump_location = (self.target_location_first+1, self.target_location_second)
        if possible_jump_location in self.grid_conntion:
            self.tile_location = possible_jump_location
            self.cooldown_jump_avaible = False
        else:
            possible_jump_location = (self.target_location_first-1, self.target_location_second)
            self.tile_location = possible_jump_location
            self.cooldown_jump_avaible = False
    
    def draw(self, screen, spirte, grid_x_y):
        self.drawing_x_y_position = grid_x_y[self.tile_location]
        self.drawing_x_position = self.drawing_x_y_position[0]
        self.drawing_y_position = self.drawing_x_y_position[1]
        screen.blit(spirte, (self.drawing_x_position - 80 // 2, self.drawing_y_position - 90 // 2))
        # Drawing the hp bar under the enemy so the player knows how much hp they have
        # Font and text
        font_icon_text = pygame.font.Font(None, 24)
        hp_text = font_icon_text.render(f"{self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, ((self.drawing_x_position - 20, self.drawing_y_position + 20)))
        # Actcual hp bar
        # TBC

# Bosses
class EmperorBlade:
    def __init__(self, starting_location):
        self.occupied_tiles = []
        self.max_hp = 300
        self.current_hp = self.max_hp
        self.ATK = 30
        self.DEF = 35
        self.RES = 15
        self.number_of_actions = 2
        self.tile_location = starting_location
        self.target_location = (0, 0)
        self.used_revice = False
        self.is_dead = False

    def updateOccupiedTiles(self, taken_tiles):
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.tile_location)
        for tiles in taken_tiles:
            self.occupied_tiles.append(tiles)

    def checkDead(self):
        if self.current_hp <= 0 and self.used_revice == True:
            self.is_dead = True

    def enemyAction(self, player_tile_location, tile_grid_connection, player_instance):         
        self.target_location = player_tile_location
        self.grid_conntion = tile_grid_connection            
        self.target_location_first = self.target_location[0]
        self.target_location_second = self.target_location[1]
        self.tile_location_first = self.tile_location[0]
        self.tile_location_second = self.tile_location[1]
        if self.is_dead == True:
            pass
        else:
            if self.current_hp <= 0:
                self.unrelenting()
            for i in range(0, self.number_of_actions):
                if player_tile_location not in tile_grid_connection[self.tile_location]:
                    self.move(self.target_location_first, self.target_location_second, self.tile_location_first, self.tile_location_second)
                else:
                    self.basicAttack(player_instance)

    def unrelenting(self):
        self.current_hp += 150
        self.ATK += 10
        
    def move(self, target_location_first, target_location_second, current_tile_location_first, current_tile_location_second):
        if target_location_first == current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first, current_tile_location_second - 1)
        elif target_location_second == current_tile_location_second:
            if target_location_first < current_tile_location_first:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
        elif target_location_first < current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
            else:
                self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
        elif target_location_first > current_tile_location_first:
            if target_location_second < current_tile_location_second:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second)
            else:
                self.tile_location = (current_tile_location_first + 1, current_tile_location_second + 1)
                if self.tile_location in self.occupied_tiles:
                    self.tile_location = (current_tile_location_first - 1, current_tile_location_second - 1)

    def basicAttack(self, player_instance):
        damage = max(self.ATK - player_instance.DEF, 1) # The emperor's blade damage is either doing the right amount or adding the DEF instead of subtracting
        player_instance.currentHP -= damage
    
    def draw(self, screen, spirte, grid_x_y):
        self.drawing_x_y_position = grid_x_y[self.tile_location]
        self.drawing_x_position = self.drawing_x_y_position[0]
        self.drawing_y_position = self.drawing_x_y_position[1]
        screen.blit(spirte, (self.drawing_x_position - 75 // 2, self.drawing_y_position - 90 // 2))
        # Drawing the hp bar under the enemy so the player knows how much hp they have
        # Font and text
        font_icon_text = pygame.font.Font(None, 24)
        hp_text = font_icon_text.render(f"{self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, ((self.drawing_x_position - 20, self.drawing_y_position + 20)))
        # Actcual hp bar
        # TBC

# TBC Future me if I ever come back to this folder and files
class LaSignoraDelCarnevale:
    def __init__(self):
        pass

    def enemyAction():
        pass

        def move():
            pass

        def basicAttack():
            pass
    
    def draw():
        pass