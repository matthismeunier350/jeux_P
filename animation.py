import pygame


class Animation(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()

        self.sprite_sheet = pygame.image.load(f'PNJ/{name}.png')
        self.index = 0
        self.clock = 0
        # decoupe les images et les met dans un dico
        self.images = {'down': self.images(0),
                       'left': self.images(33),
                       'right': self.images(65),
                       'up': self.images(96),
                       }
        self.speed = 2

    def images(self, y):
        images = []
        for i in range(0,3):
            x=i*33
            image = self.get_image(x,y)
            images.append(image)

        return images


    def change_animation(self, name):
        self.image = self.images[name][self.index]  # quand on donne la clès l'image change
        self.image.set_colorkey((0, 0, 0))

        self.clock += self.speed * 8

        if self.clock >= 100:

            self.index += 1
            if self.index >= len(self.images[name]):
                self.index = 0
            self.clock = 0


    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
