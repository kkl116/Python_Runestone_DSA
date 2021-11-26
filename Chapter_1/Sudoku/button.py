import pygame 

class Button():
    def __init__(self, pos, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.x, self.y = pos
        self.image = pygame.transform.scale(image, (int(width * scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.clicked = False 
        self.action = None
    
    def draw(self, surface):
        action = False 
        #get mouse pos 
        pos = pygame.mouse.get_pos()
        #check if pos is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                self.clicked = True 
                action = True 

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False

        #draw button on window 
        surface.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()

        return action