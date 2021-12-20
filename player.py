import pygame

from animation import Animation


class Entity(Animation):

    def __init__(self, name, x, y):
        super().__init__(name)

        self.image = self.get_image(0, 0)  # taille de l'image
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()  # creer un rectangle autour du personnage
        self.position = [x, y]
        self.name = name
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
       


        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()



    # deplacement a droite
    def move_right(self):
        self.change_animation('right')
        self.position[0] += 2


    # deplacement a gauche
    def move_left(self):
        self.position[0] -= 2
        self.change_animation('left')

    # deplacement en haut
    def move_up(self):
        self.position[1] -= 2
        self.change_animation('up')

    # deplacement en bas
    def move_down(self):
        self.position[1] += 2
        self.change_animation('down')

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    # remet le perso a son ancien position avant la collision
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    # découpe l'image en les perso anime
    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image


class Player(Entity):# herite des caractéristique de Entity
    def __init__(self):
        super().__init__('Player_P', 0, 0)

class NPC(Entity):# herite de la classe entyti
    def __init__(self, name, nb_points):
        super().__init__(name,0, 0)
        self.nb_points = nb_points
        self.name = name
        self.points = []
        self.current_point = 0

    def move(self):
        debut_point = self.current_point
        cible_point = self.current_point + 1

        if cible_point>= self.nb_points:
            cible_point=0
        debut_rect = self.points[debut_point]
        cible_rect = self.points[cible_point]

        if debut_rect.y < cible_rect.y and abs(debut_rect.x - cible_rect.x) < 3: # compare les coordonnée du rect de base et celui de la cible si c'est en dessu le npc doit se daplacer vers le bas
            self.move_down()

        elif debut_rect.y > cible_rect.y and abs(debut_rect.x - cible_rect.x) < 3: # compare les coordonnée du rect de base et celui de la cible si c'est en dessu le npc doit se daplacer vers le bas
            self.move_up()

        elif debut_rect.x > cible_rect.x and abs(debut_rect.y - cible_rect.y) < 3: # compare les coordonnée du rect de base et celui de la cible si c'est en dessu le npc doit se daplacer vers le bas
            self.move_left()

        elif debut_rect.x > cible_rect.x and abs(debut_rect.y - cible_rect.y) < 3: # compare les coordonnée du rect de base et celui de la cible si c'est en dessu le npc doit se daplacer vers le bas
            self.move_left()

        if self.rect.colliderect(cible_rect):
            self.current_point = cible_point

    def teleportation_spawn(self):
        localisation = self.points[self.current_point]
        self.position[0] = localisation.x
        self.position[1] = localisation.y
        self.save_location()

    def telecharge_points(self, map):
        for nb in range(1, self.nb_points + 1):
            point = map.get_object(f"{self.name}_path{nb}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
