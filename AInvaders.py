import pygame
import sys
import os
import random

# initialize Pygame
pygame.init()
# Set up some constants
WIDTH, HEIGHT = 1980, 1080
WHITE = (255, 255, 255)

# Load all frames from the space folder into a list
background_frames = []
for file in sorted(os.listdir('space')):
    if file.endswith('.png'):  # Assuming the frames are png files
        image = pygame.image.load(os.path.join('space', file))
        # Scale the image to fill the screen
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        background_frames.append(image)

# Initialize the current frame index
current_frame = 0




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - self.rect.height)
        self.invincible = True  # Player is initially invincible
        self.invincible_timer = pygame.time.get_ticks()  # Start the invincibility timer


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x - 5 >= 0:  # Check if player is not out of bounds on the left
                self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            if self.rect.x + 5 <= WIDTH - self.rect.width:  # Check if player is not out of bounds on the right
                self.rect.x += 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)


import random

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('alien.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = random.choice([-1, 1])  # Randomly choose initial direction
        self.vertical_speed = HEIGHT / (10 * 60 * 20)  # Number of pixels to move each frame (reduce speed)

    def update(self):
        self.rect.x += 2 * self.direction
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction *= -1  # Change direction
            self.rect.x += 2 * self.direction  # Move alien back on screen
            self.rect.y += self.vertical_speed  # Move down

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 5  # Move upwards

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create sprite groups
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()

# Create aliens
for i in range(5):
    for j in range(5):
        alien = Alien(50 + i*100, 50 + j*30)  # Decrease the `y` coordinate even more
        aliens.add(alien)


# Main game loop
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)

    # Fill the screen with a color
    screen.fill(WHITE)

    # Draw the current frame of the background animation
    screen.blit(background_frames[current_frame], (0, 0))

    # Update the current frame index to animate the background
    current_frame = (current_frame + 1) % len(background_frames)

    # Update and draw player
    player.update()
    player.draw(screen)

    # Update and draw aliens
    for alien in aliens:
        alien.update()
        alien.draw(screen)

    # Update and draw bullets
    for bullet in bullets:
        bullet.update()
        bullet.draw(screen)

    # Check for collisions
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True, pygame.sprite.collide_rect)
    for bullet, alien_list in collisions.items():
        print(f'Bullet hit {len(alien_list)} aliens!')
        for alien in alien_list:
            # Generate random x and y coordinates for the new alien
            new_alien_x = random.randint(0, WIDTH)
            new_alien_y = random.randint(0, HEIGHT/2)  # To prevent spawning aliens too close to the bottom
            # Create a new alien at the random position
            new_alien = Alien(new_alien_x, new_alien_y)
            # Add the new alien to the aliens group
            aliens.add(new_alien)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True, pygame.sprite.collide_rect)
    for bullet, alien_list in collisions.items():
        print(f'Bullet hit {len(alien_list)} aliens!')


    # Check if all aliens are destroyed
    if not aliens:
        print('Player won!')
        pygame.quit()
        sys.exit()

    # Update the display
    pygame.display.flip()
