import pygame
import pymunk
import pymunk.pygame_util

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
cannonball_visible = False  # Initially hidden

# Pymunk Space Setup
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Load Images
cannon_image = pygame.image.load('canon.png')
cannon_ball_image = pygame.image.load('cannon_ball.png')

background_image = pygame.image.load('bg4.jpg')

# Resize Images
background_image = pygame.transform.scale(background_image, (800, 600))
cannon_ball_image = pygame.transform.scale(cannon_ball_image, (50, 50))
cannon_image = pygame.transform.scale(cannon_image, (200, 200))


# Ground
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, 500), (800, 580), 5)
ground_shape.friction = 1
space.add(ground_body, ground_shape)

# Create Cannonball (Initially Hidden)
cannonball_body = None
cannonball_shape = None

# Create Cannon
def create_cannon(x, y):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (60, 60))
    space.add(body, shape)
    return body, shape

cannon_body, cannon_shape = create_cannon(10, 500)


# Function to create a new cannonball when clicked
def create_cannonball(x, y):
    global cannonball_body, cannonball_shape, cannonball_visible

    # Remove existing ball from space if any
    if cannonball_body:
        space.remove(cannonball_body, cannonball_shape)

    # Create a new ball
    cannonball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    cannonball_body.position = x, y
    cannonball_shape = pymunk.Circle(cannonball_body, 20)
    cannonball_shape.elasticity = 0.2
    cannonball_shape.friction = 0.2
    cannonball_shape.collision_type = 1  # Collision type for cannonball
    space.add(cannonball_body, cannonball_shape)

    cannonball_visible = True  # Make ball visible

# Draw function
def draw_objects():
    global game_over, game_won
    screen.blit(background_image, (0, 0))

    # Draw Cannonball only if it's visible
    if cannonball_visible and cannonball_body:
        ball_pos = cannonball_body.position
        screen.blit(cannon_ball_image, (ball_pos.x - 25, ball_pos.y - 25))

    # Draw Cannon
    cannon_pos = cannon_body.position
    screen.blit(cannon_image, (cannon_pos.x - 20, cannon_pos.y - 20))

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Allow launching only if game is not over and not won
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Create and launch cannonball
            create_cannonball(150, 500)
            cannonball_body.velocity = ((mouse_pos[0] - 150) * 4, (mouse_pos[1] - 500) * 4)
           

    
    space.step(1 / 60.0)
    draw_objects()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
