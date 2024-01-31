import pygame, sys, random, math


def random_color():
    return (random.randint(100,255), random.randint(100,255),random.randint(100,255), 160)
def random_color_2():
    return (random.randint(25,200), random.randint(25,200),random.randint(25,200), 180)

class Food(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Food,self).__init__()
        self.color = color
       
        self.radius = random.randint(5, 7)
        self.z = self.radius
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, (self.color), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(20,760 ), random.randint(10,580)))
    def relocate(self):
        self.rect.center = ((random.randint(20,760 ), random.randint(20,560)))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Enemy,self).__init__()
        self.color = color
       
        self.radius = random.randint(10, 30)
        self.mass = self.radius*2
        self.z = self.radius
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, (self.color), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(10,790 ), random.randint(10,590)))
    def move(self):
        speed= (self.mass/self.mass**1.44)*5
        self.del_x = random.randint(-5,5)
        self.del_y = random.randint(-5,5)
        if (self.rect.left+self.del_x*speed) <= -10+self.radius or (self.rect.right + self.del_x*speed) >= 790-self.radius:
            self.del_x *= -1
           
        if (self.rect.top + self.del_y*speed) <= 10 +self.radius or (self.rect.bottom+self.del_y*speed) >= 590-self.radius:
            self.del_y *= -1
        self.rect.centerx += self.del_x*speed
        self.rect.centery += self.del_y*speed
    def colide(self, dif):
        if self.radius > dif.radius:
            if math.dist((self.rect.center), (dif.rect.center)) <= (self.radius-dif.radius ):
                return True
        elif self.radius < dif.radius:
            if math.dist((self.rect.center), (dif.rect.center)) <= (dif.radius- self.radius):
                return True
        else:
            return False
    def grow(self, dif):
        if self.radius >= 175:
            return

        else:
            if isinstance(dif, Enemy):
                self.radius += dif.radius/12
                self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
                self.image = self.image.convert_alpha()
                pygame.draw.circle(self.image, (self.color), (self.radius, self.radius), self.radius)
                self.rect = self.image.get_rect(center = (self.rect.center))
            else:
                self.radius += dif.radius/2
                self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
                self.image = self.image.convert_alpha()
                pygame.draw.circle(self.image, (self.color), (self.radius, self.radius), self.radius)
                self.rect = self.image.get_rect(center = (self.rect.center))

class Player(Enemy):
    def __init__(self, color):
        super().__init__(color)
        self.radius = (11)
        self.z = self.radius
        self.mass = self.radius*2
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, (self.color), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (300, 400))
    def move(self):
        mx, my = pygame.mouse.get_pos()
        (x,y) = self.rect.center
        hyp = math.dist(self.rect.center, (mx, my))
        distx = mx - self.rect.centerx
        disty = my - self.rect.centery
        if hyp == 0:
            hyp = 0.0001
        dx = distx/hyp
        dy = disty/hyp
        speed= (self.mass/self.mass**1.44)*5
        self.rect.centerx += dx*speed
        self.rect.centery += dy*speed
           


           

       














# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agario")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = "red"

# Create clock to later control frame rate
clock = pygame.time.Clock()
enemys = pygame.sprite.Group()
for i in range(0,10):
    enemys.add(Enemy(random_color_2()))
meals = pygame.sprite.Group()
for i in range(0,25):
    meals.add(Food(random_color()))
player = Player((255,255,255,255))
p = pygame.sprite.Group()
p.add(player)
objects = pygame.sprite.Group()
objects.add(meals, enemys, p )

# Main game loop
running = True
while running:
   
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False


    # Fill the screen with a color (e.g., white)
    screen.fill("blue")
    # objects = sorted(objects, key=lambda sprite: sprite.radius, reverse=True)
    # for i, sprite in enumerate(objects):
    #         sprite.z = i
    player.move()
    for e in enemys:
       
        e.move()
    for e in enemys:
        for o in objects:
            if isinstance(o,Enemy) and e.colide(o) == True:
                if e.radius > o.radius:
                    e.grow(o)
                    o.kill()
                elif o.radius > e.radius:
                    o.grow(e)
                    e.kill()
            elif isinstance(o,Food) and e.colide(o) == True:
                e.grow(o)
                o.relocate()
            elif isinstance(o,Food) and player.colide(o) == True:
                player.grow(o)
                o.relocate()
            elif player.colide(e) == True:
                if e.radius > player.radius:
                    e.grow(player)
                    player.kill()
                    running = False
                    print("                                                              Game OVer\n                                                              player has lost")
                   
                   
                elif player.radius > e.radius:
                    player.grow(e)
                    e.kill()
                    if len(enemys) == 0:
                        running = False
                        print("                                                              Game OVer\n                                                              player Has won")
               
               
               
               
     

    p.draw(screen)
    enemys.draw(screen)
    meals.draw(screen)
    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()

