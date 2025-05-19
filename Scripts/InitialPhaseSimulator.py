import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ship Simulation")

# Colors
WHITE = (255, 255, 255)
BROWN = (150, 75, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 0, 255)
BLACK = (0, 0, 0)

# Define Ship Class
class Ship:
    def __init__(self, x, y, speed, controls):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 60
        self.height = 120
        self.controls = controls

        self.boundary_distance = 70
        self.boundary_color = WHITE
        self.touched = False

        self.ship_points = [
            [self.x, self.y + self.height],
            [self.x, self.y + self.height - 75 - 45],
            #[self.x + self.width // 2, self.y - 10 - 45],
            [self.x + self.width, self.y + self.height - 75 - 45],
            [self.x + self.width, self.y + self.height]
        ]

        self.bound_ship_points = [
            [self.x - self.boundary_distance, self.y],
            #[self.x + self.width // 2, self.y - 10 - 45 - self.boundary_distance],
            [self.x + self.width + self.boundary_distance, self.y],
            [self.x + self.width + self.boundary_distance, self.y + self.height + self.boundary_distance],
            [self.x - self.boundary_distance, self.y + self.height + self.boundary_distance]
            # (self.x + self.width + self.boundary_distance, self.y + self.height - 75 - 45)
            # (self.x - self.boundary_distance, self.y + self.height - 75 - 45),
        ]
    def move(self, keys):
        if keys[self.controls[0]]:
            self.x -= self.speed
        if keys[self.controls[1]]:
            self.x += self.speed
        if keys[self.controls[2]]:
            self.y -= self.speed
        if keys[self.controls[3]]:
            self.y += self.speed

    def draw(self):
        ship_points = [
            [self.x,self.y+self.height],
            [self.x, self.y + self.height - 75 - 45],
            #[self.x + self.width // 2, self.y - 10 - 45],
            [self.x + self.width, self.y + self.height - 75 - 45],
            [self.x + self.width,self.y + self.height]
        ]

        bound_ship_points = [
            [self.x - self.boundary_distance, self.y - self.boundary_distance],
            #[self.x + self.width // 2, self.y - 10 - 45 - self.boundary_distance],
            [self.x + self.width + self.boundary_distance, self.y -self.boundary_distance],
            [self.x + self.width + self.boundary_distance, self.y + self.height + self.boundary_distance],
            [self.x - self.boundary_distance, self.y + self.height + self.boundary_distance]
            #(self.x + self.width + self.boundary_distance, self.y + self.height - 75 - 45)
            #(self.x - self.boundary_distance, self.y + self.height - 75 - 45),
        ]

        #pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
        pygame.draw.polygon(screen, BROWN, ship_points)

        #camera
        pygame.draw.circle(screen, RED, (self.x + self.width // 4 - 15, self.y + self.height // 4 + 30), 10)
        pygame.draw.circle(screen, RED, (self.x + self.width // 4 + 45, self.y + self.height // 4 + 30), 10)
        pygame.draw.circle(screen, RED, (self.x + self.width // 4 + 15, self.y + self.height // 4 -25), 10)
        #laser
        pygame.draw.rect(screen, GREEN, (self.x + self.width // 2 - 2, self.y, 4, 25))  # Middle one
        pygame.draw.rect(screen, GREEN, (self.x + self.width // 4 - 5, self.y + 90, 4, 25))
        pygame.draw.rect(screen, GREEN, (self.x + 3 * self.width // 4 + 2, self.y + 90, 4, 25))
        #boundary
        pygame.draw.lines(screen, self.boundary_color, True, bound_ship_points, 2)


        #pygame.draw.line(screen, self.boundary_color, line1_coords[:2], line1_coords[2:], 2)
        #pygame.draw.line(screen, self.boundary_color, line2_coords[:2], line2_coords[2:], 2)

    def check_collision(self, other_ships):
        distances = []
        for other_ship in other_ships:
            other_bound_ship_points = [
                [other_ship.x - other_ship.boundary_distance, other_ship.y],
                # [other_ship.x + other_ship.width // 2, other_ship.y - 10 - 45 - other_ship.boundary_distance],
                [other_ship.x + other_ship.width + other_ship.boundary_distance, other_ship.y],
                [other_ship.x + other_ship.width + other_ship.boundary_distance, other_ship.y + other_ship.height + other_ship.boundary_distance],
                [other_ship.x - other_ship.boundary_distance, other_ship.y + other_ship.height + other_ship.boundary_distance]]
            if other_ship == self:
                continue

            # Create lists to store distances


            for x1, y1 in self.ship_points:
                for x2, y2 in other_bound_ship_points:
                    # Calculate the distance between points (x1, y1) and (x2, y2)
                    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                    distances.append(distance)
            # print(distances)
            # Check if any distance is less than the sum of radii
            flag = False
            for distance in distances:

                if distance < self.boundary_distance:
                    flag = True

                    # Ships are touching, set boundary color to red
            if flag == True:
                self.boundary_color = RED
                self.touched = True
                other_ship.boundary_color = RED
                other_ship.touched = True
                return  # Exit the function early if one collision is detected

        self.boundary_color = WHITE
        self.touched = False
        # No collision detected, set boundary color to white
        # for other_ship in other_ships:
        #     if other_ship == self:
        #         continue
        #
        #     # Calculate the distance between the centers of the ships
        #     distance = math.sqrt((self.x - other_ship.x) ** 2 + (self.y - other_ship.y) ** 2)
        #     if distance < (self.boundary_distance + other_ship.boundary_distance):
        #         # Ships are touching, set boundary color to red
        #         self.boundary_color = RED
        #         self.touched = True
        #         return
        #
        # self.boundary_color = WHITE
        # self.touched = False

# Create ships with controls

ship1 = Ship(200, 400, 1.1, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN))
ship2 = Ship(750, 400, 1.1, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s))
ship3 = Ship(500, 400, 1.1, (pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k))
ship4 = Ship(1000, 400, 1.1, (pygame.K_f, pygame.K_h, pygame.K_t, pygame.K_g))


# Water settings
water_color = BLACK
water_height = 50
water_speed = 0

# Red circle settings
red_circle_radius = 20
red_circle_x = screen_width // 2
red_circle_y = red_circle_radius * 2
red_circle_displayed = False

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get key presses for each ship
    keys1 = pygame.key.get_pressed()
    keys2 = pygame.key.get_pressed()
    keys3 = pygame.key.get_pressed()
    keys4 = pygame.key.get_pressed()

    # Move each ship based on key presses
    ship1.move(keys1)
    ship2.move(keys2)
    ship3.move(keys3)
    ship4.move(keys4)

    # Check for collision between ships
    ship1.check_collision([ship2, ship3, ship4])
    ship2.check_collision([ship1, ship3, ship4])
    ship3.check_collision([ship1, ship2, ship4])
    ship4.check_collision([ship1, ship2, ship3])


    # Clear the screen with the water background
    screen.fill(water_color)

    # Draw ships
    ship1.draw()
    ship2.draw()
    ship3.draw()
    ship4.draw()

    # Update the water position to create a flowing effect
    water_height += water_speed
    if water_height > screen_height:
        water_height = 0

    # Draw the water surface
    pygame.draw.rect(screen, water_color, (0, screen_height - water_height, screen_width, water_height))

    # Display red circle if ships are touching
    if ship1.touched or ship2.touched or ship3.touched or ship4.touched:
        pygame.draw.circle(screen, RED, (red_circle_x, red_circle_y), red_circle_radius)
        red_circle_displayed = True
    else:
        red_circle_displayed = False

    # Update the display
    pygame.display.flip()

    clock.tick(60)  # Limit the frame rate to 60 FPS
