'''
Reworking the cards and hard coding what they do
Class card name
    base damage
    base cost

    def play card (player_instance, list of [enemy_instances])
        does something
'''
class CombatKnife:
    def __init__(self):
        self.ATKM_increase = 10
        self.base_cost = 1
        self.used_amount_ck = 0

    def play(self, player_instance, *list_of_enemy_instances):
        if self.used_amount_ck > 0:
            pass
        elif player_instance.current_stamina >= self.base_cost:
            player_instance.ATKM += 10
            player_instance.current_stamina -= self.base_cost
            self.used_amount_ck += 1

class SmallShield:
    def __init__(self):
        self.DEF_increase = 10
        self.base_cost = 1
        self.used_amount_ss = 0

    def play(self, player_instance, *list_of_enemy_instances):
        if self.used_amount_ss > 0:
            pass
        elif player_instance.current_stamina >= self.base_cost:
            player_instance.DEF += 10
            player_instance.current_stamina -= self.base_cost
            self.used_amount_ss += 1

class RESShield:
    def __init__(self):
        self.RES_increase = 10
        self.base_cost = 1
        self.used_amount_rs = 0

    def play(self, player_instance, *list_of_enemy_instances):
        if self.used_amount_rs > 0:
            pass
        elif player_instance.current_stamina >= self.base_cost:
            player_instance.RES += 10
            player_instance.current_stamina -= self.base_cost
            self.used_amount_rs += 1

class SwordOfVictoria:
    def __init__(self):
        self.ATKM_increase = 10
        self.DEF_increase = 10
        self.base_cost = 2
        self.used_amount_sov = 0

    def play(self, player_instance, *list_of_enemy_instances):
        if self.used_amount_sov > 0:
            pass
        elif player_instance.current_stamina >= self.base_cost:
            player_instance.ATKM += 10
            player_instance.DEF += 10
            player_instance.current_stamina -= self.base_cost
            self.used_amount_sov += 1

class M3Craw:
    def __init__(self):
        self.ATKM_increase = 20
        self.base_cost = 3
        self.used_amount_M3 = 0

    def play(self, player_instance, *list_of_enemy_instances):
        if self.used_amount_M3 > 0:
            pass
        elif player_instance.current_stamina >= self.base_cost:
            player_instance.ATKM += 20
            player_instance.current_stamina -= self.base_cost
            self.used_amount_M3 += 1

class TheYoungFang:
    def __init__(self):
        self.base_damage = 17
        self.base_cost = 1

    def play(self, player_instance, list_of_enemy_instances):
        self.no_DEF_reduction_damage = self.base_damage + player_instance.ATKM
        self.no_RES_reduction_damage = self.no_DEF_reduction_damage // 2 # This card does 50% as additional damage as magic type
        # Find player location for their x, y cord
        self.tile_location_x = player_instance.tileLocation[0]
        self.tile_location_y = player_instance.tileLocation[1]
        # Make 6 tiles locations around the player and check if the enemy is in it
        self.tile_location_w = (self.tile_location_x - 1, self.tile_location_y - 1)
        self.tile_location_e = (self.tile_location_x, self.tile_location_y - 1)
        self.tile_location_a = (self.tile_location_x - 1, self.tile_location_y)
        self.tile_location_d = (self.tile_location_x + 1, self.tile_location_y)
        self.tile_location_z = (self.tile_location_x, self.tile_location_y + 1)
        self.tile_location_x = (self.tile_location_x + 1, self.tile_location_y + 1)
        self.tile_location_weadzx = [self.tile_location_a, self.tile_location_e, self.tile_location_a, self.tile_location_d, self.tile_location_z, self.tile_location_x]

        if player_instance.current_stamina >= self.base_cost:
            for enemies in list_of_enemy_instances:
                if enemies.tile_location in self.tile_location_weadzx and enemies.is_dead == False:
                    self.damage_after_DEF = self.no_DEF_reduction_damage - enemies.DEF
                    res = enemies.RES
                    res = res // 100
                    self.damage_after_RES = self.no_RES_reduction_damage - (self.no_RES_reduction_damage*res)
                    enemies.current_hp -= max(self.damage_after_DEF, 1)
                    enemies.current_hp -= max(self.damage_after_RES, 1)

            player_instance.current_stamina -= self.base_cost

class Blueberry:
    def __init__(self):
        self.base_damage = 18
        self.base_cost = 1

    def play(self, player_instance, list_of_enemy_instances):
        self.no_RES_reduction_damage = self.base_damage + player_instance.ATKM
        # Find player location for their x, y cord
        self.tile_location_x = player_instance.tileLocation[0]
        self.tile_location_y = player_instance.tileLocation[1]
        # Make 6 tiles locations around the player and check if the enemy is in it
        self.tile_location_w = (self.tile_location_x - 1, self.tile_location_y - 1)
        self.tile_location_e = (self.tile_location_x, self.tile_location_y - 1)
        self.tile_location_a = (self.tile_location_x - 1, self.tile_location_y)
        self.tile_location_d = (self.tile_location_x + 1, self.tile_location_y)
        self.tile_location_z = (self.tile_location_x, self.tile_location_y + 1)
        self.tile_location_x = (self.tile_location_x + 1, self.tile_location_y + 1)
        self.tile_location_weadzx = [self.tile_location_a, self.tile_location_e, self.tile_location_a, self.tile_location_d, self.tile_location_z, self.tile_location_x]

        if player_instance.current_stamina >= self.base_cost:
            for enemies in list_of_enemy_instances:
                if enemies.tile_location in self.tile_location_weadzx and enemies.is_dead == False:
                    res = enemies.RES
                    res = res // 100
                    self.damage_after_RES = self.no_RES_reduction_damage - (self.no_RES_reduction_damage*res)
                    enemies.current_hp -= max(self.damage_after_RES, 1)
                    if enemies.current_hp <= 0:
                        player_instance.current_stamina += self.base_cost

            player_instance.current_stamina -= self.base_cost

class DarkChocolate:
    def __init__(self):
        self.base_damage = 18
        self.base_cost = 1

    def play(self, player_instance, list_of_enemy_instances):
        self.no_DEF_reduction_damage = self.base_damage + player_instance.ATKM
        # Find player location for their x, y cord
        self.tile_location_x = player_instance.tileLocation[0]
        self.tile_location_y = player_instance.tileLocation[1]
        # Make 6 tiles locations around the player and check if the enemy is in it
        self.tile_location_w = (self.tile_location_x - 1, self.tile_location_y - 1)
        self.tile_location_e = (self.tile_location_x, self.tile_location_y - 1)
        self.tile_location_a = (self.tile_location_x - 1, self.tile_location_y)
        self.tile_location_d = (self.tile_location_x + 1, self.tile_location_y)
        self.tile_location_z = (self.tile_location_x, self.tile_location_y + 1)
        self.tile_location_x = (self.tile_location_x + 1, self.tile_location_y + 1)
        self.tile_location_weadzx = [self.tile_location_a, self.tile_location_e, self.tile_location_a, self.tile_location_d, self.tile_location_z, self.tile_location_x]

        if player_instance.current_stamina >= self.base_cost:
            for enemies in list_of_enemy_instances:
                if enemies.tile_location in self.tile_location_weadzx and enemies.is_dead == False:
                    self.damage_after_DEF = self.no_DEF_reduction_damage - enemies.DEF
                    enemies.current_hp -= max(self.damage_after_DEF, 1)
                    if enemies.current_hp <= 0:
                        player_instance.current_stamina += self.base_cost

            player_instance.current_stamina -= self.base_cost

class MagicSword:
    def __init__(self):
        self.base_damage = 12
        self.base_cost = 2

    def play(self, player_instance, list_of_enemy_instances):
        self.no_RES_reduction_damage = self.base_damage + player_instance.ATKM
        # Find player location for their x, y cord
        self.tile_location_x = player_instance.tileLocation[0]
        self.tile_location_y = player_instance.tileLocation[1]
        # Make 6 tiles locations around the player and check if the enemy is in it
        self.tile_location_w = (self.tile_location_x - 1, self.tile_location_y - 1)
        self.tile_location_e = (self.tile_location_x, self.tile_location_y - 1)
        self.tile_location_a = (self.tile_location_x - 1, self.tile_location_y)
        self.tile_location_d = (self.tile_location_x + 1, self.tile_location_y)
        self.tile_location_z = (self.tile_location_x, self.tile_location_y + 1)
        self.tile_location_x = (self.tile_location_x + 1, self.tile_location_y + 1)
        self.tile_location_weadzx = [self.tile_location_a, self.tile_location_e, self.tile_location_a, self.tile_location_d, self.tile_location_z, self.tile_location_x]

        if player_instance.current_stamina >= self.base_cost:
            for enemies in list_of_enemy_instances:
                if enemies.tile_location in self.tile_location_weadzx and enemies.is_dead == False:
                    res = enemies.RES
                    res = res // 100
                    self.damage_after_RES = self.no_RES_reduction_damage - (self.no_RES_reduction_damage*res)
                    enemies.current_hp -= max(self.damage_after_RES, 1)

            player_instance.current_stamina -= self.base_cost

class PileDriver:
    def __init__(self):
        self.base_damage = 4
        self.damage_instance = 3
        self.base_cost = 2

    def play(self, player_instance, list_of_enemy_instances):
        self.no_DEF_reduction_damage = self.base_damage + player_instance.ATKM
        # Find player location for their x, y cord
        self.tile_location_x = player_instance.tileLocation[0]
        self.tile_location_y = player_instance.tileLocation[1]
        # Make 6 tiles locations around the player and check if the enemy is in it
        self.tile_location_w = (self.tile_location_x - 1, self.tile_location_y - 1)
        self.tile_location_e = (self.tile_location_x, self.tile_location_y - 1)
        self.tile_location_a = (self.tile_location_x - 1, self.tile_location_y)
        self.tile_location_d = (self.tile_location_x + 1, self.tile_location_y)
        self.tile_location_z = (self.tile_location_x, self.tile_location_y + 1)
        self.tile_location_x = (self.tile_location_x + 1, self.tile_location_y + 1)
        self.tile_location_weadzx = [self.tile_location_a, self.tile_location_e, self.tile_location_a, self.tile_location_d, self.tile_location_z, self.tile_location_x]

        if player_instance.current_stamina >= self.base_cost:
            for enemies in list_of_enemy_instances:
                if enemies.tile_location in self.tile_location_weadzx and enemies.is_dead == False:
                    self.damage_after_DEF = self.no_DEF_reduction_damage - enemies.DEF
                    for i in range(self.damage_instance):
                        enemies.current_hp -= max(self.damage_after_DEF, 1)

            player_instance.current_stamina -= self.base_cost

class GalacticBaseballer:
    def __init__(self):
        self.base_damage = 30
        self.base_cost = 3

    def play(self, player_instance, list_of_enemy_instances):
        self.no_DEF_reduction_damage = self.base_damage + player_instance.ATKM
        # Find player location for their x, y cord
        self.tile_location_x = player_instance.tileLocation[0]
        self.tile_location_y = player_instance.tileLocation[1]
        # Make 6 tiles locations around the player and check if the enemy is in it
        self.tile_location_w = (self.tile_location_x - 1, self.tile_location_y - 1)
        self.tile_location_e = (self.tile_location_x, self.tile_location_y - 1)
        self.tile_location_a = (self.tile_location_x - 1, self.tile_location_y)
        self.tile_location_d = (self.tile_location_x + 1, self.tile_location_y)
        self.tile_location_z = (self.tile_location_x, self.tile_location_y + 1)
        self.tile_location_x = (self.tile_location_x + 1, self.tile_location_y + 1)
        self.tile_location_weadzx = [self.tile_location_a, self.tile_location_e, self.tile_location_a, self.tile_location_d, self.tile_location_z, self.tile_location_x]

        if player_instance.current_stamina >= self.base_cost:
            for enemies in list_of_enemy_instances:
                if enemies.tile_location in self.tile_location_weadzx and enemies.is_dead == False:
                    self.damage_after_DEF = self.no_DEF_reduction_damage - enemies.DEF
                    enemies.current_hp -= max(self.damage_after_DEF, 1)

            player_instance.current_stamina -= self.base_cost