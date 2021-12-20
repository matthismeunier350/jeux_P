"""matthis meunier 1 phenix commence le 01/11/2021"""
from dataclasses import dataclass




from player import Player, NPC

import pygame, pytmx, pyscroll

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str




@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict() # dico qui comprend toute les donner des cles
        self.screen = screen
        self.player = player
        self.current_map = "world"
        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house_1", target_world="HOUSE_1_F",teleport_point="spawn_house_1"),
            Portal(from_world="world", origin_point="enter_house_2", target_world="HOUSE_2_F", teleport_point="spawn_house_2"),
            Portal(from_world="world", origin_point="enter_house_3", target_world="HOUSE_3_F",teleport_point="spawn_house_3"),
            Portal(from_world="world", origin_point="enter_house_4", target_world="HOUSE_4_F",teleport_point="spawn_house_4")
        ], npcs=[
            NPC('Jean', nb_points=4),
            NPC('Nicolas', nb_points=4)
        ])
        self.register_map("HOUSE_1_F", portals=[
            Portal(from_world="HOUSE_1_F", origin_point="exit_house_1", target_world="world", teleport_point="enter_house_exit_1")
        ])
        self.register_map("HOUSE_2_F", portals=[
            Portal(from_world="HOUSE_2_F", origin_point="exit_house_2", target_world="world",teleport_point="enter_house_exit_2")
        ])
        self.register_map("HOUSE_3_F", portals=[
            Portal(from_world="HOUSE_3_F", origin_point="exit_house_3", target_world="world",teleport_point="enter_house_exit_3")
        ])
        self.register_map("HOUSE_4_F", portals=[
            Portal(from_world="HOUSE_4_F", origin_point="exit_house_4", target_world="world",teleport_point="enter_house_exit_4")
        ])
        self.teleport_player("player")
        self.teleportation_npcs()
    def check_npc_collisions(self, dialogs_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialogs_box.execute()

    def check_collisions(self):
        # verrifier les portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # verrifier les collsions
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1


            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):  # charge le monde selon son nom

        # charger la map
        tmx_data = pytmx.util_pygame.load_pygame(f'{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # generer une liste qui stocke les emplacement de collision
        walls = []
        for object in tmx_data.objects:
            if object.type == "collision":
                walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        # dessiner les groupes de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)  # quel niveau de calques est le perso
        group.add(self.player)
        for npc in npcs:
            group.add(npc)

        # crer un objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]  # cherche le monde

    def get_group(self):
        return self.get_map().group  # renvoie un objet de la map

    def get_walls(self):
        return self.get_map().walls  # renvoie les mur

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)
    def teleportation_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.telecharge_points(self)
                npc.teleportation_spawn()

    def draw(self):  # dessine la map
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):  # telecharge les groupes
        self.get_group().update()
        self.check_collisions()
        
        for npc in self.get_map().npcs:
            npc.move()
