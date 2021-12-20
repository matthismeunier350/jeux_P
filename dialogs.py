import pygame

class Dialogs:

    x_position = 60
    y_position = 470

    def __init__(self):
        self.box = pygame.image.load('dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box,(700, 100))
        self.texts = ["Bonjour, ça va ?", "bien", "Bonne aventure"]
        self.text_index = 0
        self.font = pygame.font.Font('dialogs/dialog_font.ttf', 18)
        self.lire = False

    def execute(self):
        if self.lire:
            self.text_suivant()
        else:
            self.lire = True
            self.text_index = 0


    def affichage(self, screen):
        if self.lire:
            screen.blit(self.box,(self.x_position, self.y_position))
            text = self.font.render(self.texts[self.text_index], False, (0, 0, 0))
            screen.blit(text, (self.x_position+60, self.y_position+30))

    def text_suivant(self):
        self.text_index += 1

        if self.text_index >=len(self.texts):
            self.lire = False



