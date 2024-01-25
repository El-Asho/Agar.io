import pygame
import sys
import random,  math

pygame.init()
screen_width = 1100
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Tutorial")
WHITE = (0, 0, 150)
screen.fill(WHITE)
pygame.display.flip()
clock = pygame.time.Clock()

 
clock.tick(60)


class Food(pygame.sprite.Sprite):

    def __init__(self,color):
        super(Food,self).__init__()
        self.radius = 5
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(10,1090),random.randint(10,690)))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Enemy,self).__init__()
        self.radius = random.randint(10,30)
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA,16)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(10,790),random.randint(10,590)))
        self.speed = 25/self.radius
        self.delta_x = random.choice([-1,1])
        self.delta_y = random.choice([-1,1])

    def move(self):
            self.rect.centerx += (self.delta_x*self.speed)
            self.rect.centery += (self.delta_y*self.speed)
            if self.rect.centerx >=1100:
                self.delta_x = -1
            elif self.rect.centerx <=0:
                self.delta_x = 1
            elif self.rect.centery >= 700:
                self.delta_y = -1
            elif self.rect.centery <=0:
                self.delta_y = 1
    def collide(self,o):
        return math.dist(self.rect.center, o.rect.center) < self.radius + o.radius
    def grow(self,radius):
        self.radius+=radius

        
                
       



    
class Player(Enemy):
    def __init__(self,color):
        super(Player,self).__init__(color)
        self.radius = 25
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA,16)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image,color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (180,180))
meals = pygame.sprite.Group() # Group is a high powered list
food_num = 40
for num in range(100):
    meals.add(Food("red"))
meals.draw(screen)
enemies = pygame.sprite.Group()
for num in range(3):
    enemies.add(Enemy("black"))
enemies.draw(screen)
players = pygame.sprite.Group()
players.add(Player("white"))
players.draw(screen)
running = True
while running:
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False 

    screen.fill("blue")

    for enemy in enemies: 
        enemy.move()
        
        for objects in meals:
            if enemy != 0 and enemy.collide(objects):
                distance = math.dist(enemy.rect.center, objects.rect.center)
                if type(objects) == Food:
                    if distance < enemy.radius + objects.radius:
                        enemy.grow(5)
                        objects.kill
        for objects in players:
            distance = math.dist(enemy.rect.center, objects.rect.center)
            if type(objects) == Player:
                if distance < enemy.radius + objects.radius:
                    if enemy.radius < objects.radius:
                        enemy.kill()
                    elif enemy.radius > objects.radius:
                        objects.kill()
    meals.draw(screen)
    enemies.draw(screen)



    pygame.display.flip()

