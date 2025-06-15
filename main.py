import card_data
import enemy_data
import pygame
import random
import math
import os
import sys
pygame.init()

class PlayerCharacter:
    def __init__(self, maxHP = 110, ATK = 15, ATKM = 5, DEF = 10, RES = 0):
        self.maxHP = maxHP
        self.currentHP = maxHP
        self.ATK = ATK
        self.ATKM = ATKM
        self.DEF = DEF
        self.RES = RES
        self.max_stamina = 4
        self.current_stamina = self.max_stamina
        self.max_lunacy = 150
        self.current_lunacy = 75
        self.deck_combat = []
        self.deck_equipment = []
        self.deck_four_cards = []
        self.tileLocation = (2, 5)
        self.player_turn = True
        self.is_dead = False

    def check_dead(self):
        if self.currentHP < 0:
            self.is_dead = True
            Game.quitGame()

    def endTurn(self):
        self.player_turn = False
        self.current_stamina = self.max_stamina

    def basicMovenment(self, movement_direction_value): # I needed to copy and paste the grid for player movenemnt
        self.battle_field_connection_grid_for_player = {
            (1, 1): [(1, 2), (2, 1), (2, 2)],
            (1, 2): [(1, 1), (1, 3), (2, 2), (2, 3)],
            (1, 3): [(1, 2), (1, 4), (2, 3), (2, 4)],
            (1, 4): [(1, 3), (1, 5), (2, 4), (2, 5)],
            (1, 5): [(1, 4), (2, 5), (2, 6)],
            (2, 1): [(1, 1), (2, 2), (3, 1), (3, 2)],
            (2, 2): [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2), (3, 3)],
            (2, 3): [(1, 2), (1, 3), (2, 2), (2, 4), (3, 3), (3, 4)],
            (2, 4): [(1, 3), (1, 4), (2, 3), (2, 5), (3, 4), (3, 5)],
            (2, 5): [(1, 4), (1, 5), (2, 4), (2, 6), (3, 5), (3, 6)],
            (2, 6): [(1, 5), (2, 5), (3, 6), (3, 7)],
            (3, 1): [(2, 1), (3, 2), (4, 1), (4, 2)],
            (3, 2): [(2, 1), (2, 2), (3, 1), (3, 3), (4, 2), (4, 3)],
            (3, 3): [(2, 2), (2, 3), (3, 2), (3, 4), (4, 3), (4, 4)],
            (3, 4): [(2, 3), (2, 4), (3, 3), (3, 5), (4, 4), (4, 5)],
            (3, 5): [(2, 4), (2, 5), (3, 4), (3, 6), (4, 5), (4, 6)],
            (3, 6): [(2, 5), (2, 6), (3, 5), (3, 7), (4, 6), (4, 7)],
            (3, 7): [(2, 6), (3, 6), (4, 7), (4, 8)],
            (4, 1): [(3, 1), (4, 2), (5, 1), (5, 2)],
            (4, 2): [(3, 1), (3, 2), (4, 1), (4, 3), (5, 2), (5, 3)],
            (4, 3): [(3, 2), (3, 3), (4, 2), (4, 4), (5, 3), (5, 4)],
            (4, 4): [(3, 3), (3, 4), (4, 3), (4, 5), (5, 4), (5, 5)],
            (4, 5): [(3, 4), (3, 5), (4, 4), (4, 6), (5, 5), (5, 6)],
            (4, 6): [(3, 5), (3, 6), (4, 5), (4, 7), (5, 6), (5, 7)],
            (4, 7): [(3, 6), (3, 7), (4, 6), (4, 8), (5, 7), (5, 8)],
            (4, 8): [(3, 7), (4, 7), (5, 8), (5, 9)],
            (5, 1): [(4, 1), (5, 2), (6, 2)],
            (5, 2): [(4, 1), (4, 2), (5, 1), (5, 3), (6, 2), (6, 3)],
            (5, 3): [(4, 2), (4, 3), (5, 2), (5, 4), (6, 3), (6, 4)],
            (5, 4): [(4, 3), (4, 4), (5, 3), (5, 5), (6, 4), (6, 5)],
            (5, 5): [(4, 4), (4, 5), (5, 4), (5, 6), (6, 5), (6, 6)],
            (5, 6): [(4, 5), (4, 6), (5, 5), (5, 7), (6, 6), (6, 7)],
            (5, 7): [(4, 6), (4, 7), (5, 6), (5, 8), (6, 7), (6, 8)],
            (5, 8): [(4, 7), (4, 8), (5, 7), (5, 9), (6, 8), (6, 9)],
            (5, 9): [(4, 8), (5, 8), (6, 9)],
            (6, 2): [(5, 1), (5, 2), (6, 3), (7, 3)],
            (6, 3): [(5, 2), (5, 3), (6, 2), (6, 4), (7, 3), (7, 4)],
            (6, 4): [(5, 3), (5, 4), (6, 3), (6, 5), (7, 4), (7, 5)],
            (6, 5): [(5, 4), (5, 5), (6, 4), (6, 6), (7, 5), (7, 6)],
            (6, 6): [(5, 5), (5, 6), (6, 5), (6, 7), (7, 6), (7, 7)],
            (6, 7): [(5, 6), (5, 7), (6, 6), (6, 8), (7, 7), (7, 8)],
            (6, 8): [(5, 7), (5, 8), (6, 7), (6, 9), (7, 8), (7, 9)],
            (6, 9): [(5, 8), (5, 9), (6, 8), (7, 9)],
            (7, 3): [(6, 2), (6, 3), (7, 4), (8, 4)],
            (7, 4): [(6, 4), (6, 5), (7, 3), (7, 5), (8, 4), (8, 5)],
            (7, 5): [(6, 5), (6, 6), (7, 4), (7, 6), (8, 5), (8, 6)],
            (7, 6): [(6, 6), (6, 7), (7, 5), (7, 7), (8, 6), (8, 7)],
            (7, 7): [(6, 7), (6, 8), (7, 6), (7, 8), (8, 7), (8, 8)],
            (7, 8): [(6, 8), (6, 9), (7, 7), (7, 9), (8, 8), (8, 9)],
            (7, 9): [(6, 8), (6, 9), (7, 8), (8, 9)],
            (8, 4): [(7, 3), (7, 4), (8, 5), (9, 5)],
            (8, 5): [(7, 4), (7, 5), (8, 4), (8, 6), (9, 5), (9, 6)],
            (8, 6): [(7, 5), (7, 6), (8, 5), (8, 7), (9, 6), (9, 7)],
            (8, 7): [(7, 6), (7, 7), (8, 6), (8, 8), (9, 7), (9, 8)],
            (8, 8): [(7, 7), (7, 8), (8, 7), (8, 9), (9, 8), (9, 9)],
            (8, 9): [(7, 8), (7, 9), (8, 8), (9, 9)],
            (9, 5): [(8, 4), (8, 5), (9, 6)],
            (9, 6): [(8, 5), (8, 6), (9, 5), (9,7)],
            (9, 7): [(8, 6), (8, 7), (9, 6), (9,8)],
            (9, 8): [(8, 7), (8, 8), (9, 7), (9,9)],
            (9, 9): [(8, 8), (8, 9), (9, 8)]
        }
        '''
        Create a dict to track what letter goes in what direction
        w = top left = 1
        e = top right = 2
        d = right = 3
        a = left = 4
        z = bottom left = 5
        x = bottom right = 6
        '''
        movenment_dict = {
            1: (self.tileLocation[0]-1, self.tileLocation[1]-1),
            2: (self.tileLocation[0], self.tileLocation[1]-1),
            3: (self.tileLocation[0]+1, self.tileLocation[1]),
            4: (self.tileLocation[0]-1, self.tileLocation[1]),
            5: (self.tileLocation[0], self.tileLocation[1]+1),
            6: (self.tileLocation[0]+1, self.tileLocation[1]+1)
        }
        self.dest_tile_location = movenment_dict[movement_direction_value]
        # Check if the movenment is valid and reduce stamina by 1 (Because they moved)
        if self.dest_tile_location in self.battle_field_connection_grid_for_player and self.current_stamina > 0:
            self.tileLocation = self.dest_tile_location
            self.current_stamina -= 1

    def basicAttack():
        pass

class Game:
    def __init__(self):
        '''
        Making the battle field connection grid
        From a tile with 6 neighbours and 4 neighbours, the rule is 
        (-1, -1), (-1 0), (0, -1), (0, +1), (+1, 0), (+1, +1)

        This will help with how the player will move and enemy will move
        This will also help with how cards will target certain tiles
        '''
        self.battle_field_connection_grid = {
            (1, 1): [(1, 2), (2, 1), (2, 2)],
            (1, 2): [(1, 1), (1, 3), (2, 2), (2, 3)],
            (1, 3): [(1, 2), (1, 4), (2, 3), (2, 4)],
            (1, 4): [(1, 3), (1, 5), (2, 4), (2, 5)],
            (1, 5): [(1, 4), (2, 5), (2, 6)],
            (2, 1): [(1, 1), (2, 2), (3, 1), (3, 2)],
            (2, 2): [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2), (3, 3)],
            (2, 3): [(1, 2), (1, 3), (2, 2), (2, 4), (3, 3), (3, 4)],
            (2, 4): [(1, 3), (1, 4), (2, 3), (2, 5), (3, 4), (3, 5)],
            (2, 5): [(1, 4), (1, 5), (2, 4), (2, 6), (3, 5), (3, 6)],
            (2, 6): [(1, 5), (2, 5), (3, 6), (3, 7)],
            (3, 1): [(2, 1), (3, 2), (4, 1), (4, 2)],
            (3, 2): [(2, 1), (2, 2), (3, 1), (3, 3), (4, 2), (4, 3)],
            (3, 3): [(2, 2), (2, 3), (3, 2), (3, 4), (4, 3), (4, 4)],
            (3, 4): [(2, 3), (2, 4), (3, 3), (3, 5), (4, 4), (4, 5)],
            (3, 5): [(2, 4), (2, 5), (3, 4), (3, 6), (4, 5), (4, 6)],
            (3, 6): [(2, 5), (2, 6), (3, 5), (3, 7), (4, 6), (4, 7)],
            (3, 7): [(2, 6), (3, 6), (4, 7), (4, 8)],
            (4, 1): [(3, 1), (4, 2), (5, 1), (5, 2)],
            (4, 2): [(3, 1), (3, 2), (4, 1), (4, 3), (5, 2), (5, 3)],
            (4, 3): [(3, 2), (3, 3), (4, 2), (4, 4), (5, 3), (5, 4)],
            (4, 4): [(3, 3), (3, 4), (4, 3), (4, 5), (5, 4), (5, 5)],
            (4, 5): [(3, 4), (3, 5), (4, 4), (4, 6), (5, 5), (5, 6)],
            (4, 6): [(3, 5), (3, 6), (4, 5), (4, 7), (5, 6), (5, 7)],
            (4, 7): [(3, 6), (3, 7), (4, 6), (4, 8), (5, 7), (5, 8)],
            (4, 8): [(3, 7), (4, 7), (5, 8), (5, 9)],
            (5, 1): [(4, 1), (5, 2), (6, 2)],
            (5, 2): [(4, 1), (4, 2), (5, 1), (5, 3), (6, 2), (6, 3)],
            (5, 3): [(4, 2), (4, 3), (5, 2), (5, 4), (6, 3), (6, 4)],
            (5, 4): [(4, 3), (4, 4), (5, 3), (5, 5), (6, 4), (6, 5)],
            (5, 5): [(4, 4), (4, 5), (5, 4), (5, 6), (6, 5), (6, 6)],
            (5, 6): [(4, 5), (4, 6), (5, 5), (5, 7), (6, 6), (6, 7)],
            (5, 7): [(4, 6), (4, 7), (5, 6), (5, 8), (6, 7), (6, 8)],
            (5, 8): [(4, 7), (4, 8), (5, 7), (5, 9), (6, 8), (6, 9)],
            (5, 9): [(4, 8), (5, 8), (6, 9)],
            (6, 2): [(5, 1), (5, 2), (6, 3), (7, 3)],
            (6, 3): [(5, 2), (5, 3), (6, 2), (6, 4), (7, 3), (7, 4)],
            (6, 4): [(5, 3), (5, 4), (6, 3), (6, 5), (7, 4), (7, 5)],
            (6, 5): [(5, 4), (5, 5), (6, 4), (6, 6), (7, 5), (7, 6)],
            (6, 6): [(5, 5), (5, 6), (6, 5), (6, 7), (7, 6), (7, 7)],
            (6, 7): [(5, 6), (5, 7), (6, 6), (6, 8), (7, 7), (7, 8)],
            (6, 8): [(5, 7), (5, 8), (6, 7), (6, 9), (7, 8), (7, 9)],
            (6, 9): [(5, 8), (5, 9), (6, 8), (7, 9)],
            (7, 3): [(6, 2), (6, 3), (7, 4), (8, 4)],
            (7, 4): [(6, 4), (6, 5), (7, 3), (7, 5), (8, 4), (8, 5)],
            (7, 5): [(6, 5), (6, 6), (7, 4), (7, 6), (8, 5), (8, 6)],
            (7, 6): [(6, 6), (6, 7), (7, 5), (7, 7), (8, 6), (8, 7)],
            (7, 7): [(6, 7), (6, 8), (7, 6), (7, 8), (8, 7), (8, 8)],
            (7, 8): [(6, 8), (6, 9), (7, 7), (7, 9), (8, 8), (8, 9)],
            (7, 9): [(6, 8), (6, 9), (7, 8), (8, 9)],
            (8, 4): [(7, 3), (7, 4), (8, 5), (9, 5)],
            (8, 5): [(7, 4), (7, 5), (8, 4), (8, 6), (9, 5), (9, 6)],
            (8, 6): [(7, 5), (7, 6), (8, 5), (8, 7), (9, 6), (9, 7)],
            (8, 7): [(7, 6), (7, 7), (8, 6), (8, 8), (9, 7), (9, 8)],
            (8, 8): [(7, 7), (7, 8), (8, 7), (8, 9), (9, 8), (9, 9)],
            (8, 9): [(7, 8), (7, 9), (8, 8), (9, 9)],
            (9, 5): [(8, 4), (8, 5), (9, 6)],
            (9, 6): [(8, 5), (8, 6), (9, 5), (9,7)],
            (9, 7): [(8, 6), (8, 7), (9, 6), (9,8)],
            (9, 8): [(8, 7), (8, 8), (9, 7), (9,9)],
            (9, 9): [(8, 8), (8, 9), (9, 8)]
        }
        '''
        A dictonary to contain the x, y coordinates of where a picture should be placed
        The pattern for going left and right interm of x position is +80 then +85 or -80 then -85
        The pattern for going up and down interm of y position is +75 or -75
        The point (1, 5) starts at x = 730 and y = 425
        The point (1, 4) starts at x = 770 (X increase by 40 each time)
        print(self.grid_position_x_y_cord[(1, 1)]) -> 890, 125
        '''
        self.grid_position_x_y_cord = {
            (1, 1): (890, 125),
            (1, 2): (850, 200),
            (1, 3): (810, 275),
            (1, 4): (770, 350),
            (1, 5): (730, 425),
            (2, 1): (970, 125),
            (2, 2): (930, 200),
            (2, 3): (890, 275),
            (2, 4): (850, 350),
            (2, 5): (810, 425),
            (2, 6): (770, 500),
            (3, 1): (1055, 125),
            (3, 2): (1015, 200),
            (3, 3): (975, 275),
            (3, 4): (930, 350),
            (3, 5): (890, 425),
            (3, 6): (850, 500),
            (3, 7): (810, 575),
            (4, 1): (1135, 125),
            (4, 2): (1095, 200),
            (4, 3): (1055, 275),
            (4, 4): (1015, 350),
            (4, 5): (970, 425),
            (4, 6): (930, 500),
            (4, 7): (890, 575),
            (4, 8): (850, 650),
            (5, 1): (1220, 125),
            (5, 2): (1180, 200),
            (5, 3): (1140, 275),
            (5, 4): (1095, 350),
            (5, 5): (1055, 425),
            (5, 6): (1015, 500),
            (5, 7): (970, 575),
            (5, 8): (930, 650),
            (5, 9): (890, 725),
            (6, 2): (1260, 200),
            (6, 3): (1220, 275),
            (6, 4): (1180, 350),
            (6, 5): (1135, 425),
            (6, 6): (1095, 500),
            (6, 7): (1055, 575),
            (6, 8): (1015, 650),
            (6, 9): (970, 725),
            (7, 3): (1305, 275),
            (7, 4): (1260, 350),
            (7, 5): (1220, 425),
            (7, 6): (1180, 500),
            (7, 7): (1140, 575),
            (7, 8): (1100, 650),
            (7, 9): (1060, 725),
            (8, 4): (1340, 350),
            (8, 5): (1300, 425),
            (8, 6): (1260, 500),
            (8, 7): (1220, 575),
            (8, 8): (1180, 650),
            (8, 9): (1140, 725),
            (9, 5): (1380, 425),
            (9, 6): (1340, 500),
            (9, 7): (1300, 575),
            (9, 8): (1260, 650),
            (9, 9): (1220, 725)
        }
        # Checking who occupies what tiles
        self.occupied_tiles = []

        # What turn number it is
        self.turn_number = 0
        
        # Make the screen size
        self.screen = pygame.display.set_mode((1600, 900))
        self.mouse_position = pygame.mouse.get_pos()
        # Make a player class
        self.player = PlayerCharacter()
        # Get the battle ground background (Serves as a background for the entire thing)
        self.battle_ground_back_ground = pygame.image.load(os.path.join("Ui", "battle_grounds.png"))
        self.battle_ground_back_ground = pygame.transform.scale(self.battle_ground_back_ground, (1600, 900))
        # Character spirte
        self.characterSpirte = pygame.image.load(os.path.join("spirtes", "player", "Player.png"))
        self.character_spirte_size_x = 70
        self.character_spirte_size_y = 70
        self.characterSpirte = pygame.transform.scale(self.characterSpirte, (self.character_spirte_size_x, self.character_spirte_size_y))
        # Get the icons for deity abilities 
        self.insanity_ability = pygame.image.load(os.path.join("Ui", "battle_icons", "deityabilities", "thedecadenza", "insanity.png"))
        self.lunacy_bar = pygame.image.load(os.path.join("Ui", "battle_icons", "deityabilities", "thedecadenza", "lunacybar.png"))
        self.mental_ability = pygame.image.load(os.path.join("Ui", "battle_icons", "deityabilities", "thedecadenza", "mental.png"))
        self.obession_ability = pygame.image.load(os.path.join("Ui", "battle_icons", "deityabilities", "thedecadenza", "obession.png"))
        # Get the icons for battle (health, stamina, other buttons)
        self.attack_modifer_stat_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "attack_modifer_stat_icon.png"))
        self.attack_stat_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "attack_stat_icon.png"))
        self.defense_stat_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "defense_stat_icon.png"))
        self.end_turn_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "end_turn.png"))
        self.enemy_targetting_hexgon_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "enemy_targetting_hexgon.png"))
        self.enemy_turn_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "enemy_turn.png"))
        self.energy_cost_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "energy_cost.png"))
        self.heart_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "heart.png"))
        self.res_stat_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "res_stat_icon.png"))
        self.stamina_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "stamina.png"))
        self.targetting_hexgon_icon = pygame.image.load(os.path.join("Ui", "battle_icons", "targetting_hexgon.png"))
        # Getting the hpbar progress (For both the enemy and player)
        self.hp_bar_icon_0_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_0_8.png"))
        self.hp_bar_icon_1_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_1_8.png"))
        self.hp_bar_icon_2_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_2_8.png"))
        self.hp_bar_icon_3_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_3_8.png"))
        self.hp_bar_icon_4_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_4_8.png"))
        self.hp_bar_icon_5_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_5_8.png"))
        self.hp_bar_icon_6_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_6_8.png"))
        self.hp_bar_icon_7_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_7_8.png"))
        self.hp_bar_icon_8_8 = pygame.image.load(os.path.join("Ui", "battle_icons", "enemyhpbar", "hpbar_8_8.png"))
        
        # Getting the spirtes for the player's cards
        # Combat Cards
        self.short_sword_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "short_sword+.png"))
        self.scythe_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "scythe.png"))
        self.scythe_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "scythe+.png"))
        self.hand_book_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "handbook.png"))
        self.hand_book_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "handbook+.png"))
        self.crystal_orb_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "crystal_orb+.png"))
        self.magic_sword_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "magic_sword.png"))
        self.magic_sword_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "magic_sword+.png"))
        self.pile_driver_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "pile_driver.png"))
        self.pile_driver_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "pile_driver+.png"))
        self.knife_i_made_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "knife_i_made+.png"))
        self.galactic_baseballer_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "galactic_baseballer.png"))
        self.the_young_fang_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "the_young_fang+.png"))
        self.blueberry_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "blueberry+.png"))
        self.dark_chocolate_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "dark_chocolate+.png"))

        # Equipment Cards
        self.small_shield_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "small_shield+.png"))
        self.combat_knife_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "combat_knife+.png"))
        self.res_shield_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "res_shield.png"))
        self.sword_of_victoria_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "sword_of_victoria.png"))
        self.battlefield_analyzer_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "battlefield_analyzer.png"))
        self.stim_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "stim.png"))
        self.stim_upgraded_spirte = pygame.image.load(os.path.join("spirtes", "cards", "upgradedcards", "stim+.png"))
        self.strong_tea_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "strong_tea.png"))
        self.M3_craw_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "M3_craw.png"))

        # Uility Card
        self.transmitter_spirte = pygame.image.load(os.path.join("spirtes", "cards", "unupgradedcards", "transmitter.png"))

        # Scaling the card spirtes
        self.card_width = 160
        self.card_height = 240
        # Equipement
        self.combat_knife_upgraded_spirte = pygame.transform.scale(self.combat_knife_upgraded_spirte, (self.card_width, self.card_height))
        self.small_shield_upgraded_spirte = pygame.transform.scale(self.small_shield_upgraded_spirte, (self.card_width, self.card_height))
        self.sword_of_victoria_spirte = pygame.transform.scale(self.sword_of_victoria_spirte, (self.card_width, self.card_height))
        self.res_shield_spirte = pygame.transform.scale(self.res_shield_spirte, (self.card_width, self.card_height))
        self.M3_craw_spirte = pygame.transform.scale(self.M3_craw_spirte, (self.card_width, self.card_height))
        # Combat
        self.the_young_fang_upgraded_spirte = pygame.transform.scale(self.the_young_fang_upgraded_spirte, (self.card_width, self.card_height))
        self.blueberry_upgraded_spirte = pygame.transform.scale(self.blueberry_upgraded_spirte, (self.card_width, self.card_height))
        self.dark_chocolate_upgraded_spirte = pygame.transform.scale(self.dark_chocolate_upgraded_spirte, (self.card_width, self.card_height))
        self.magic_sword_upgraded_spirte = pygame.transform.scale(self.magic_sword_upgraded_spirte, (self.card_width, self.card_height))
        self.galactic_baseballer_spirte = pygame.transform.scale(self.galactic_baseballer_spirte, (self.card_width, self.card_height))
        self.pile_driver_upgraded_spirte = pygame.transform.scale(self.pile_driver_upgraded_spirte, (self.card_width, self.card_height))

        # Enemy Spirtes
        self.ursa_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "normal", "ursa.png"))
        self.raider_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "normal", "raider.png"))
        self.shielded_raider_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "normal", "shielded_raider.png"))
        self.agent_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "normal", "agent.png"))
        self.stalker_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "elites", "stalker.png"))
        self.jetpack_raider_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "normal", "jetpack_raider.png"))
        self.flag_bearer_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "normal", "flag_bearer.png"))
        self.emperor_blade_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "boss", "emperor's_blade.png"))
        self.la_signora_del_carnevale_spirte = pygame.image.load(os.path.join("spirtes", "enemy", "boss", "la_signora_del_carnevale.png"))
        # Enemy Scaling
        self.ursa_spirte = pygame.transform.scale(self.ursa_spirte, (70, 70))
        self.raider_spirte = pygame.transform.scale(self.raider_spirte, (70, 70))
        self.shielded_raider_spirte = pygame.transform.scale(self.shielded_raider_spirte, (70, 70))
        self.agent_spirte = pygame.transform.scale(self.agent_spirte, (70, 70))
        self.stalker_spirte = pygame.transform.scale(self.stalker_spirte, (70, 80))
        self.jetpack_raider_spirte = pygame.transform.scale(self.jetpack_raider_spirte, (70, 70))
        self.flag_bearer_spirte = pygame.transform.scale(self.flag_bearer_spirte, (70, 70))
        self.emperor_blade_spirte = pygame.transform.scale(self.emperor_blade_spirte, (75, 90))
        self.la_signora_del_carnevale_spirte = pygame.transform.scale(self.la_signora_del_carnevale_spirte, (70, 70))

        # Hard Coding the enemies here
        # Stage one
        self.stage_one_ursa = enemy_data.Ursa((6,4))
        self.stage_one_raider = enemy_data.Raider((7,6))
        self.list_of_stage_one_enemies = [self.stage_one_raider, self.stage_one_ursa]

        # Stage two
        self.stage_two_shielded_raider_one = enemy_data.ShieldedRaider((5,3))
        self.stage_two_shielded_raider_two = enemy_data.ShieldedRaider((7,7))
        self.stage_two_agent_one = enemy_data.Agent((7,4))
        self.stage_two_agent_two = enemy_data.Agent((8,6))
        self.list_of_stage_two_enemies = [self.stage_two_agent_one, self.stage_two_agent_two, self.stage_two_shielded_raider_one, self.stage_two_shielded_raider_two]

        # Stage three
        self.stage_three_jetpack_raider_one = enemy_data.JetpackRaider((6,3))
        self.stage_three_jetpack_raider_two = enemy_data.JetpackRaider((6,4))
        self.stage_three_jetpack_raider_three = enemy_data.JetpackRaider((7,6))
        self.stage_three_jetpack_raider_four = enemy_data.JetpackRaider((8,7))
        self.stage_three_flag_bearer_one = enemy_data.FlagBearer((8,5))
        self.list_of_stage_three_enemies = [self.stage_three_flag_bearer_one, self.stage_three_jetpack_raider_one, self.stage_three_jetpack_raider_two, self.stage_three_jetpack_raider_three, self.stage_three_jetpack_raider_four]

        # Stage four
        self.stage_four_stalker_one = enemy_data.Stalker((4,5), self.turn_number)
        self.stage_four_ursa_one = enemy_data.Ursa((4,7))
        self.stage_four_raider_one = enemy_data.Raider((2,3))
        self.list_of_stage_four_enemies = [self.stage_four_raider_one, self.stage_four_stalker_one, self.stage_four_ursa_one]

        # Stage five
        self.stage_five_emperor_blade_one = enemy_data.EmperorBlade((7,5))
        self.stage_five_jetpack_raider_one = enemy_data.JetpackRaider((2,4))
        self.stage_five_jetpack_raider_two = enemy_data.JetpackRaider((3,5))
        self.stage_five_jetpack_raider_three = enemy_data.JetpackRaider((3,6))
        self.stage_five_flag_bearer_one = enemy_data.FlagBearer((8,5))
        self.list_of_stage_five_enemies = [self.stage_five_emperor_blade_one, self.stage_five_jetpack_raider_one, self.stage_five_jetpack_raider_two, self.stage_five_jetpack_raider_three, self.stage_five_flag_bearer_one]

        # Stage six
        self.stage_six_la_signora_del_carnevale = enemy_data.LaSignoraDelCarnevale()

        '''
        Future Tony, Please code in a way to update the stage number so the player can go from one round to another
        But I will say that the diffcultly may have been a little high because the enemies can easily wipe half of your hp in one turn
        On stage number 2, when the the shielded raiders and agents all attack at once, you lose 70% of your hp in one hit
        Both a skill issue on the player for grouping all of them together to and to let them all hit the player on the same turn
        But also a problem with how much ATK they have...
        '''
        self.stage_number = 1

        # Hard coding cards
        # Equipement cards, should only be played once
        self.combat_knife = card_data.CombatKnife()
        self.small_shield = card_data.SmallShield()
        self.res_shield = card_data.RESShield()
        self.sword_of_victoria = card_data.SwordOfVictoria()
        self.M3_craw = card_data.M3Craw()
        # Appending the equipment cards to a list in player class
        self.player.deck_equipment.append(1) # Each number represents the cards above in the same order
        self.player.deck_equipment.append(2)
        self.player.deck_equipment.append(3)
        self.player.deck_equipment.append(4)
        self.player.deck_equipment.append(5)
        
        # Combat cards, played based on the number of instances there is
        self.the_young_fang = card_data.TheYoungFang()
        self.blueberry = card_data.Blueberry()
        self.dark_chocolate = card_data.DarkChocolate()
        self.magic_sword = card_data.MagicSword()
        self.pile_driver = card_data.PileDriver()
        self.galactic_baseballer = card_data.GalacticBaseballer()
        # Appending the possible comnbats cards to the player class deck of combat cards
        self.player.deck_combat.append(1001) # Each number represents the cards above in the same order
        self.player.deck_combat.append(1002)
        self.player.deck_combat.append(1003)
        self.player.deck_combat.append(1004)
        self.player.deck_combat.append(1005)
        self.player.deck_combat.append(1006)

        # Amount of updates the card choice (A temp fix about to becoome a perm fix)
        self.amount_of_update_card_choice = 1

    def givePlayerCardChoice(self, amount_of_update_card_choices): # Assigning cards to card slots
        if amount_of_update_card_choices == 1:
            self.player.deck_four_cards.clear()
            self.amount_of_equipment_card = 0
            for i in range(0, 4):
                self.random_card_equipment_combat = random.randint(1,2)
                if self.random_card_equipment_combat == 1 and self.player.deck_equipment != None and self.amount_of_equipment_card == 0:
                    self.random_equipment_card = random.randint(0,len(self.player.deck_equipment) - 1)
                    self.player.deck_four_cards.append(self.player.deck_equipment[self.random_equipment_card])
                    self.amount_of_equipment_card += 1
                else:
                    self.random_combat_card = random.randint(0, 5)
                    self.player.deck_four_cards.append(self.player.deck_combat[self.random_combat_card])
        else:
            pass

    def playCard(self, card_slot_number, stage_number): # When playing a card choice, we want to get that card to play
        if stage_number == 1: # Checking what list of stage enemies to give to the cards
            self.list_given = [self.stage_one_ursa, self.stage_one_raider]
        elif stage_number == 2:
            self.list_given = [self.stage_two_agent_two, self.stage_two_agent_one, self.stage_two_shielded_raider_one, self.stage_two_shielded_raider_two]
        elif stage_number == 3:
            self.list_given = [self.stage_three_flag_bearer_one, self.stage_three_jetpack_raider_one, self.stage_three_jetpack_raider_two, self.stage_three_jetpack_raider_three, self.stage_three_jetpack_raider_four]
        elif stage_number == 4:
            self.list_given = [self.stage_four_raider_one, self.stage_four_stalker_one, self.stage_four_ursa_one]
        elif stage_number == 5:
            self.list_given = [self.stage_five_emperor_blade_one, self.stage_five_flag_bearer_one, self.stage_five_jetpack_raider_one, self.stage_five_jetpack_raider_two, self.stage_five_jetpack_raider_three]

        # Depending on card slot called, then we check what card it is and call it
        if card_slot_number == 1: # We do a bunch of if statement checks to determine what card it is
            if self.player.deck_four_cards[0] == 1: # Check if the card in the first position is the combat knife
                self.combat_knife.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 2:
                self.small_shield.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 3:
                self.res_shield.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 4:
                self.sword_of_victoria.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 5:
                self.M3_craw.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 1001:
                self.the_young_fang.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 1002:
                self.blueberry.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 1003:
                self.dark_chocolate.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 1004:
                self.magic_sword.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 1005:
                self.pile_driver.play(self.player, self.list_given)
            elif self.player.deck_four_cards[0] == 1006:
                self.galactic_baseballer.play(self.player, self.list_given)
        elif card_slot_number == 2: # Check the second position
            if self.player.deck_four_cards[1] == 1: # Check if the card in the first position is the combat knife
                self.combat_knife.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 2:
                self.small_shield.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 3:
                self.res_shield.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 4:
                self.sword_of_victoria.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 5:
                self.M3_craw.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 1001:
                self.the_young_fang.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 1002:
                self.blueberry.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 1003:
                self.dark_chocolate.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 1004:
                self.magic_sword.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 1005:
                self.pile_driver.play(self.player, self.list_given)
            elif self.player.deck_four_cards[1] == 1006:
                self.galactic_baseballer.play(self.player, self.list_given)
        elif card_slot_number == 3: # Check the thrid position
            if self.player.deck_four_cards[2] == 1: # Check if the card in the first position is the combat knife
                self.combat_knife.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 2:
                self.small_shield.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 3:
                self.res_shield.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 4:
                self.sword_of_victoria.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 5:
                self.M3_craw.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 1001:
                self.the_young_fang.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 1002:
                self.blueberry.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 1003:
                self.dark_chocolate.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 1004:
                self.magic_sword.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 1005:
                self.pile_driver.play(self.player, self.list_given)
            elif self.player.deck_four_cards[2] == 1006:
                self.galactic_baseballer.play(self.player, self.list_given)
        elif card_slot_number == 4: # Check the fourth position
            if self.player.deck_four_cards[3] == 1: # Check if the card in the first position is the combat knife
                self.combat_knife.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 2:
                self.small_shield.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 3:
                self.res_shield.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 4:
                self.sword_of_victoria.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 5:
                self.M3_craw.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 1001:
                self.the_young_fang.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 1002:
                self.blueberry.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 1003:
                self.dark_chocolate.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 1004:
                self.magic_sword.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 1005:
                self.pile_driver.play(self.player, self.list_given)
            elif self.player.deck_four_cards[3] == 1006:
                self.galactic_baseballer.play(self.player, self.list_given)

    def quitGame():
        pygame.quit()
        sys.exit()

    def drawIcons(self):
        # Scaling the icons to fit the screen
        self.icon_size_x = 50
        self.icon_size_y = 50
        # deity abiltiies first
        self.insanity_ability = pygame.transform.scale(self.insanity_ability, (self.icon_size_x, self.icon_size_y))
        self.lunacy_bar = pygame.transform.scale(self.lunacy_bar, (235, 75))
        self.mental_ability = pygame.transform.scale(self.mental_ability, (self.icon_size_x, self.icon_size_y))
        self.obession_ability = pygame.transform.scale(self.obession_ability, (self.icon_size_x, self.icon_size_y))
        # battle icons
        self.attack_modifer_stat_icon = pygame.transform.scale(self.attack_modifer_stat_icon, (self.icon_size_x, self.icon_size_y))
        self.attack_stat_icon = pygame.transform.scale(self.attack_stat_icon, (self.icon_size_x, self.icon_size_y))
        self.defense_stat_icon = pygame.transform.scale(self.defense_stat_icon, (self.icon_size_x, self.icon_size_y))
        self.heart_icon = pygame.transform.scale(self.heart_icon, (self.icon_size_x, self.icon_size_y))
        self.res_stat_icon = pygame.transform.scale(self.res_stat_icon, (self.icon_size_x, self.icon_size_y))
        self.stamina_icon = pygame.transform.scale(self.stamina_icon, (self.icon_size_x, self.icon_size_y))
        # HP bar size
        self.hp_bar_icon_0_8 = pygame.transform.scale(self.hp_bar_icon_0_8, (420, 125))
        self.hp_bar_icon_1_8 = pygame.transform.scale(self.hp_bar_icon_1_8, (420, 125))
        self.hp_bar_icon_2_8 = pygame.transform.scale(self.hp_bar_icon_2_8, (420, 125))
        self.hp_bar_icon_3_8 = pygame.transform.scale(self.hp_bar_icon_3_8, (420, 125))
        self.hp_bar_icon_4_8 = pygame.transform.scale(self.hp_bar_icon_4_8, (420, 125))
        self.hp_bar_icon_5_8 = pygame.transform.scale(self.hp_bar_icon_5_8, (420, 125))
        self.hp_bar_icon_6_8 = pygame.transform.scale(self.hp_bar_icon_6_8, (420, 125))
        self.hp_bar_icon_7_8 = pygame.transform.scale(self.hp_bar_icon_7_8, (420, 125))
        self.hp_bar_icon_8_8 = pygame.transform.scale(self.hp_bar_icon_8_8, (420, 125))
        # Drawing them onto the screen
        # Drawing the deity abilities onto the screen
        self.screen.blit(self.mental_ability, (400 - self.icon_size_x // 2, 200 - self.icon_size_y // 2))
        self.screen.blit(self.obession_ability, (480 - self.icon_size_x // 2, 200 - self.icon_size_y // 2))
        self.screen.blit(self.lunacy_bar, (80, 200 -  75 // 2))
        # Drawing top left basic UI for health, def and res
        # Drawing the hp bar of the player
        if self.player.currentHP == self.player.maxHP:
            self.screen.blit(self.hp_bar_icon_8_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))
        elif (self.player.currentHP / self.player.maxHP) * 100 > 88:
            self.screen.blit(self.hp_bar_icon_7_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))
        elif (self.player.currentHP / self.player.maxHP) * 100 > 75:
            self.screen.blit(self.hp_bar_icon_6_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))
        elif (self.player.currentHP / self.player.maxHP) * 100 > 62:
            self.screen.blit(self.hp_bar_icon_5_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))
        elif (self.player.currentHP / self.player.maxHP) * 100 > 50:
            self.screen.blit(self.hp_bar_icon_4_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))
        elif (self.player.currentHP / self.player.maxHP) * 100 > 37:
            self.screen.blit(self.hp_bar_icon_3_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))
        elif (self.player.currentHP / self.player.maxHP) * 100 > 25:
            self.screen.blit(self.hp_bar_icon_2_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))
        elif (self.player.currentHP / self.player.maxHP) * 100 > 0:
            self.screen.blit(self.hp_bar_icon_1_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))
        else:
            self.screen.blit(self.hp_bar_icon_0_8, (80 - self.icon_size_x // 2, 80 - self.icon_size_y // 2))

        # Filling in text for the two bars (HP and Lunacy)
        font_bar = pygame.font.Font(None, 36)
        hp_bar_text = font_bar.render(f"{self.player.currentHP} / {self.player.maxHP} HP", True, (255, 255, 255))
        lunacy_bar_text = font_bar.render(f"{self.player.current_lunacy} / {self.player.max_lunacy} Lunacy", True, (255, 255, 255))
        self.screen.blit(hp_bar_text, (120 - self.icon_size_x // 2, 130 - self.icon_size_y // 2))
        self.screen.blit(lunacy_bar_text, (120 - self.icon_size_x // 2, 215 - self.icon_size_y // 2))

        # To center to the png to the correct x, y coors
        self.screen.blit(self.defense_stat_icon, (100 - self.icon_size_x // 2, 300 - self.icon_size_y // 2))
        self.screen.blit(self.res_stat_icon, (180 - self.icon_size_x // 2, 300 - self.icon_size_y // 2))
        self.screen.blit(self.attack_stat_icon, (260 - self.icon_size_x // 2, 300 - self.icon_size_y // 2))
        self.screen.blit(self.attack_modifer_stat_icon, (340 - self.icon_size_x // 2, 300 - self.icon_size_y // 2))
        self.screen.blit(self.stamina_icon, (420 - self.icon_size_x // 2, 300 - self.icon_size_y // 2))

        # Filling in text for the icons
        font_icon_text = pygame.font.Font(None, 24)
        defense_text = font_icon_text.render(f"{self.player.DEF} DEF", True, (255, 255, 255))
        res_text = font_icon_text.render(f"{self.player.RES} RES", True, (255, 255, 255))
        attack_text = font_icon_text.render(f"{self.player.ATK} ATK", True, (255, 255, 255))
        attack_modifier_text = font_icon_text.render(f"{self.player.ATKM} ATKM", True, (255, 255, 255))
        stamina_text = font_icon_text.render(f"{self.player.current_stamina} / {self.player.max_stamina} STA", True, (255, 255, 255))
        self.screen.blit(defense_text, (100 - self.icon_size_x // 2, 350 - self.icon_size_y // 2))
        self.screen.blit(res_text, (180 - self.icon_size_x // 2, 350 - self.icon_size_y // 2))
        self.screen.blit(attack_text, (260 - self.icon_size_x // 2, 350 - self.icon_size_y // 2))
        self.screen.blit(attack_modifier_text, (340 - self.icon_size_x // 2, 350 - self.icon_size_y // 2))
        self.screen.blit(stamina_text, (420 - self.icon_size_x // 2, 350 - self.icon_size_y // 2))

        Game.drawPlayerPosition(self)
        Game.drawEnemySpirtes(self, self.stage_number)

    def drawCards(self): # Drawing the player's cards
        self.x_position_one = 180
        self.x_position_two = 370
        self.y_position_one = 500
        self.y_position_two = 750
        for i in range(0, 4): # To draw the four cards into their respective slots, 250 x 375 : 1 x 1.5
            if self.player.deck_four_cards[i] == 1:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.combat_knife_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.combat_knife_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.combat_knife_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.combat_knife_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 2:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.small_shield_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.small_shield_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.small_shield_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.small_shield_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 4:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.sword_of_victoria_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.sword_of_victoria_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.sword_of_victoria_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.sword_of_victoria_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 3:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.res_shield_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.res_shield_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.res_shield_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.res_shield_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 5:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.M3_craw_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.M3_craw_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.M3_craw_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.M3_craw_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 1001:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.the_young_fang_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.the_young_fang_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.the_young_fang_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.the_young_fang_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 1002:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.blueberry_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.blueberry_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.blueberry_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.blueberry_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 1003:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.dark_chocolate_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.dark_chocolate_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.dark_chocolate_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.dark_chocolate_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 1004:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.magic_sword_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.magic_sword_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.magic_sword_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.magic_sword_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 1006:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.galactic_baseballer_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.galactic_baseballer_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.galactic_baseballer_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.galactic_baseballer_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))
            elif self.player.deck_four_cards[i] == 1005:
                if i < 2: # In card slot 1 or 2 and should be displayed on the higher level
                    if i == 0: # must be first slot
                        self.screen.blit(self.pile_driver_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_one - self.card_height // 2))
                    else: # must be second slot
                        self.screen.blit(self.pile_driver_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_one - self.card_height // 2))
                else: # Must be in card slot 3 or 4 which means we must display them on the lower level
                    if i == 3: # must be first slot on lower level
                        self.screen.blit(self.pile_driver_upgraded_spirte, (self.x_position_one - self.card_width // 2, self.y_position_two - self.card_height // 2))
                    else: # must be second slot on lower level
                        self.screen.blit(self.pile_driver_upgraded_spirte, (self.x_position_two - self.card_width // 2, self.y_position_two - self.card_height // 2))

    def updateOccupiedTiles(self, stage_number): # Tries to make sure enemies aren't literally on top of each other, does provide a new gameplay element
        self.occupied_tiles.clear()
        self.occupied_tiles.append(self.player.tileLocation)
        if stage_number == 1:
            self.occupied_tiles.append(self.stage_one_ursa.tile_location)
            self.occupied_tiles.append(self.stage_one_raider.tile_location)
            self.stage_one_ursa.updateOccupiedTiles(self.occupied_tiles)
            self.stage_one_raider.updateOccupiedTiles(self.occupied_tiles)
        elif stage_number == 2:
            self.occupied_tiles.append(self.stage_two_shielded_raider_one.tile_location)
            self.occupied_tiles.append(self.stage_two_shielded_raider_two.tile_location)
            self.occupied_tiles.append(self.stage_two_agent_one.tile_location)
            self.occupied_tiles.append(self.stage_two_agent_two.tile_location)
            self.stage_two_shielded_raider_one.updateOccupiedTiles(self.occupied_tiles)
            self.stage_two_shielded_raider_two.updateOccupiedTiles(self.occupied_tiles)
            self.stage_two_agent_one.updateOccupiedTiles(self.occupied_tiles)
            self.stage_two_agent_two.updateOccupiedTiles(self.occupied_tiles)
        elif stage_number == 3:
            self.occupied_tiles.append(self.stage_three_flag_bearer_one.tile_location)
            self.occupied_tiles.append(self.stage_three_jetpack_raider_one.tile_location)
            self.occupied_tiles.append(self.stage_three_jetpack_raider_two.tile_location)
            self.occupied_tiles.append(self.stage_three_jetpack_raider_three.tile_location)
            self.occupied_tiles.append(self.stage_three_jetpack_raider_four.tile_location)
            self.stage_three_jetpack_raider_one.updateOccupiedTiles(self.occupied_tiles)
            self.stage_three_jetpack_raider_two.updateOccupiedTiles(self.occupied_tiles)
            self.stage_three_jetpack_raider_three.updateOccupiedTiles(self.occupied_tiles)
            self.stage_three_jetpack_raider_four.updateOccupiedTiles(self.occupied_tiles)
            self.stage_three_flag_bearer_one.updateOccupiedTiles(self.occupied_tiles)
        elif stage_number == 4:
            self.occupied_tiles.append(self.stage_four_raider_one.tile_location)
            self.occupied_tiles.append(self.stage_four_stalker_one.tile_location)
            self.occupied_tiles.append(self.stage_four_ursa_one.tile_location)
            self.stage_four_stalker_one.updateOccupiedTiles(self.occupied_tiles)
            self.stage_four_ursa_one.updateOccupiedTiles(self.occupied_tiles)
            self.stage_four_raider_one.updateOccupiedTiles(self.occupied_tiles)
        elif stage_number == 5: # Please do these ones when possible
            self.occupied_tiles.append(self.stage_five_emperor_blade_one.tile_location)
            self.occupied_tiles.append(self.stage_five_flag_bearer_one.tile_location)
            self.occupied_tiles.append(self.stage_five_jetpack_raider_one.tile_location)
            self.occupied_tiles.append(self.stage_five_jetpack_raider_two.tile_location)
            self.occupied_tiles.append(self.stage_five_jetpack_raider_three.tile_location)
            self.stage_five_emperor_blade_one.updateOccupiedTiles(self.occupied_tiles)
            self.stage_five_flag_bearer_one.updateOccupiedTiles(self.occupied_tiles)
            self.stage_five_jetpack_raider_one.updateOccupiedTiles(self.occupied_tiles)
            self.stage_five_jetpack_raider_two.updateOccupiedTiles(self.occupied_tiles)
            self.stage_five_jetpack_raider_three.updateOccupiedTiles(self.occupied_tiles)

    def drawPlayerPosition(self):
        self.character_x_y_position = self.grid_position_x_y_cord[self.player.tileLocation]
        self.character_x_position = self.character_x_y_position[0]
        self.character_y_position = self.character_x_y_position[1]
        self.screen.blit(self.characterSpirte, (self.character_x_position - self.character_spirte_size_x // 2, self.character_y_position - self.character_spirte_size_y // 2))

    def drawEnemySpirtes(self, stage_number): # We give it stage_number to determine what spirtes need to be drawn
        if stage_number == 1:
            self.stage_one_ursa.draw(self.screen, self.ursa_spirte, self.grid_position_x_y_cord)
            self.stage_one_raider.draw(self.screen, self.raider_spirte, self.grid_position_x_y_cord)
        elif stage_number == 2:
            self.stage_two_shielded_raider_one.draw(self.screen, self.shielded_raider_spirte, self.grid_position_x_y_cord)
            self.stage_two_shielded_raider_two.draw(self.screen, self.shielded_raider_spirte, self.grid_position_x_y_cord)
            self.stage_two_agent_one.draw(self.screen, self.agent_spirte, self.grid_position_x_y_cord)
            self.stage_two_agent_two.draw(self.screen, self.agent_spirte, self.grid_position_x_y_cord)
        elif stage_number == 3:
            self.stage_three_jetpack_raider_one.draw(self.screen, self.jetpack_raider_spirte, self.grid_position_x_y_cord)
            self.stage_three_jetpack_raider_two.draw(self.screen, self.jetpack_raider_spirte, self.grid_position_x_y_cord)
            self.stage_three_jetpack_raider_three.draw(self.screen, self.jetpack_raider_spirte, self.grid_position_x_y_cord)
            self.stage_three_jetpack_raider_four.draw(self.screen, self.jetpack_raider_spirte, self.grid_position_x_y_cord)
            self.stage_three_flag_bearer_one.draw(self.screen, self.flag_bearer_spirte, self.grid_position_x_y_cord)
        elif stage_number == 4:
            self.stage_four_stalker_one.draw(self.screen, self.stalker_spirte, self.grid_position_x_y_cord)
            self.stage_four_ursa_one.draw(self.screen, self.ursa_spirte, self.grid_position_x_y_cord)
            self.stage_four_raider_one.draw(self.screen, self.raider_spirte, self.grid_position_x_y_cord)
        elif stage_number == 5:
            self.stage_five_emperor_blade_one.draw(self.screen, self.emperor_blade_spirte, self.grid_position_x_y_cord)
            self.stage_five_jetpack_raider_one.draw(self.screen, self.jetpack_raider_spirte, self.grid_position_x_y_cord)
            self.stage_five_jetpack_raider_two.draw(self.screen, self.jetpack_raider_spirte, self.grid_position_x_y_cord)
            self.stage_five_jetpack_raider_three.draw(self.screen, self.jetpack_raider_spirte, self.grid_position_x_y_cord)
            self.stage_five_flag_bearer_one.draw(self.screen, self.flag_bearer_spirte, self.grid_position_x_y_cord)

    def enemyTurn(self, stage_number): # Handles the enemy turns, hard coded who is going when depending on stage progress
        if stage_number == 1:
            self.stage_one_ursa.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_one_raider.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
        elif stage_number == 2:
            self.stage_two_shielded_raider_one.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_two_shielded_raider_two.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_two_agent_one.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_two_agent_two.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
        elif stage_number == 3:
            self.stage_three_jetpack_raider_one.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_three_jetpack_raider_two.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_three_jetpack_raider_three.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_three_jetpack_raider_four.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            # Code flag bearer to reduce player defense

        elif stage_number == 4:
            self.stage_four_stalker_one.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_four_ursa_one.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_four_raider_one.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
        elif stage_number == 5:
            self.stage_five_emperor_blade_one.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_five_jetpack_raider_one.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_five_jetpack_raider_two.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            self.stage_five_jetpack_raider_three.enemyAction(self.player.tileLocation, self.battle_field_connection_grid, self.player)
            # Code flag bearer to reduce player defense
        Game.drawIcons(self)

    def startBattle(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.screen.fill((0,0,0))
                self.screen.blit(self.battle_ground_back_ground, (0, 0))
                Game.drawIcons(self)
                Game.updateOccupiedTiles(self, self.stage_number)
                if event.type == pygame.QUIT:
                    running = False
                    Game.quitGame()
                    break
                if self.player.player_turn == True:
                    self.givePlayerCardChoice(self.amount_of_update_card_choice) # give the player his cards
                    self.drawCards()
                    self.amount_of_update_card_choice += 1
                    if event.type == pygame.KEYDOWN: # Key down will control basic movement and card selection
                        if event.key == pygame.K_RETURN:
                            self.player.endTurn()
                        elif event.key == pygame.K_w:
                            self.basic_movenment_choice = 1
                            self.player.basicMovenment(self.basic_movenment_choice)
                        elif event.key == pygame.K_e:
                            self.basic_movenment_choice = 2
                            self.player.basicMovenment(self.basic_movenment_choice)
                        elif event.key == pygame.K_d:
                            self.basic_movenment_choice = 3
                            self.player.basicMovenment(self.basic_movenment_choice)
                        elif event.key == pygame.K_a:
                            self.basic_movenment_choice = 4
                            self.player.basicMovenment(self.basic_movenment_choice)
                        elif event.key == pygame.K_z:
                            self.basic_movenment_choice = 5
                            self.player.basicMovenment(self.basic_movenment_choice)
                        elif event.key == pygame.K_x:
                            self.basic_movenment_choice = 6
                            self.player.basicMovenment(self.basic_movenment_choice)
                        elif event.key == pygame.K_1:
                            self.card_slot_play = 1
                            self.playCard(self.card_slot_play, self.stage_number)
                        elif event.key == pygame.K_2:
                            self.card_slot_play = 2
                            self.playCard(self.card_slot_play, self.stage_number)
                        elif event.key == pygame.K_3:
                            self.card_slot_play = 3
                            self.playCard(self.card_slot_play, self.stage_number)
                        elif event.key == pygame.K_4:
                            self.card_slot_play = 4
                            self.playCard(self.card_slot_play, self.stage_number)
                        elif event.key == pygame.K_u:
                            self.stage_number += 1
                else: # It would have to be the enemies turn
                    Game.enemyTurn(self, self.stage_number)
                    self.player.player_turn = True # Allow the player to go after the enmeies are done
                    self.turn_number += 1
                    self.amount_of_update_card_choice = 1
            pygame.display.update()

first_game = Game()
first_game.startBattle()