#This is a test file for the soon to be made main game play area
import pygame
import os
import sys
import map_constructor
import json
pygame.init()

# All the classes needed for game loop
class MainMenu:
    def __init__(self):
        # Everything below is a collection of the backgrounds and pre-loading them to prevent lag
        self.screen = pygame.display.set_mode((1600, 900))
        self.mainMenuBackground = pygame.image.load(os.path.join("main_menu","main_menu_screen.png"))
        self.mainMenuBackground = pygame.transform.scale(self.mainMenuBackground, (1600, 900))

        MainMenu.mainMenu(self)

    def mainMenu(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.screen.fill((0,0,0))
                self.screen.blit(self.mainMenuBackground, (0, 0))
                if event.type == pygame.QUIT:
                    running = False
                    Game.quitGame(self)
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePosition = pygame.mouse.get_pos()
                    targetRectStart = pygame.Rect(290, 360, 300, 225)
                    targetRectQuit = pygame.Rect(290, 600, 300, 225)
                    if targetRectStart.collidepoint(self.mousePosition):
                        Game().chooseDeity()
                    elif targetRectQuit.collidepoint(self.mousePosition):
                        running = False
                        Game().chooseDeity()
                        break

            pygame.display.update()
        pygame.quit()

# Is a class of the player's attributes and contains
class PlayerCharacter:
    def __init__(self, maxHP = 70, ATK = 10, ATKM = 0, DEF = 10, RES = 0, maxStamina = 3, deck = [], deity = None):
        self.maxHP = maxHP
        self.currentHP = maxHP
        self.ATK = ATK
        self.ATKM = ATKM
        self.DEF = DEF
        self.RES = RES
        self.maxStamina = maxStamina
        self.deity = None
        self.deck = []
        self.gold = 100
        self.playerPositionX = 0
        self.playerPositionY = 0
        self.playerMapLocation = (0, 0)

        self.characterSpirte = pygame.image.load(os.path.join("spirtes", "player", "Player.png"))
        self.characterSpirte = pygame.transform.scale(self.characterSpirte, (50, 50))

    def updateDeity(self, deitySelectionNum):
        if deitySelectionNum == 1:
            self.deity = "world breaker"
        else:
            self.deity = "lappland"
    
    def drawHealthBar(self):
        pass

    def drawUiOnMap(self):
        pass

    def drawUiInBattle(self):
        pass

    def upgradeCards(self):
        pass

    def buyCards(self):
        pass

    def sellCards(self):
        pass

    def updateHealthBar(self):
        pass

    def updateGoldCount(self):
        pass

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1600, 900))
        # This is for creating information the player is interacting with directly
        self.map = map_constructor.Map()
        self.player = PlayerCharacter()

        # This is background pictures
        self.deityBackground = pygame.image.load(os.path.join("Ui","deity_selection.png"))
        self.deityBackground = pygame.transform.scale(self.deityBackground, (1600, 900))
    
# Everything below here is related to menu navigation
    def quitGame(self):
        pygame.quit()
        sys.exit()

    def chooseDeity(self):
        running = True
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.deityBackground, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    Game.quitGame(self)
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePosition = pygame.mouse.get_pos()
                    targetRectWorldBreaker = pygame.Rect(400 - 500 // 2, 450 // 2, 500, 550)
                    targetRectLappland = pygame.Rect(1200 - 500 // 2, 450 // 2, 500, 550)
                    if targetRectWorldBreaker.collidepoint(self.mousePosition):
                        deityNumber = 1
                        running = False
                    elif targetRectLappland.collidepoint(self.mousePosition):
                        deityNumber = 2
                        running = False
            pygame.display.update()
        self.player.updateDeity(deityNumber)
        self.mapNav()

    def deckNav(self):
        pass

    def mapNav(self): # The map is going to become the main menu that the player will keep going back and fourth
        running = True
        while running:
            self.screen.fill((0,0,0))
            self.map.drawMap()

    def selectingItems(self):
        pass

# Everything below here are related to combat and enemy AI

    def enteringCombat(self):
        pass

    def combatActions(self):
        pass

    def enemyCombatActions(self):
        pass

    def generateReward(self):
        pass

    def pickUpRewards(self):
        pass

# Game loop all below
firstRun = MainMenu()