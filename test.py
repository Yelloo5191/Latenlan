import pygame

# Initialize Pygame
pygame.init()

# Set the display size
screen = pygame.display.set_mode((640, 480))

# Set the clock object to help track time
clock = pygame.time.Clock()

# Set the initial position and velocity of the game object
x = 0
y = 0
vx = 100
vy = 100

# Set the initial time
current_time = pygame.time.get_ticks()


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the elapsed time since the last frame
    elapsed_time = pygame.time.get_ticks() - current_time
    current_time = pygame.time.get_ticks()

    # Update the position of the game object based on its velocity and the elapsed time
    x += vx * elapsed_time / 1000
    y += vy * elapsed_time / 1000

    # Draw the game object at the updated position
    pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 10)
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)
