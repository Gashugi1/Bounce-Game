import pygame
import random
import sys
import os

# Initialize Pygame and set up the game window
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obstacle Avoidance Game")
clock = pygame.time.Clock()

# Define colors
BACKGROUND_COLOR = (255, 255, 255)  # White background
SPHERE_COLOR = (255, 215, 0)        # Gold sphere
OBSTACLE_COLOR = (0, 0, 0)          # Black obstacles
TEXT_COLOR = (0, 0, 0)              # Black text

# Gravity and physics
GRAVITY = 0.4
JUMP_STRENGTH = 12

# Load high score from file
if os.path.exists('high_score.txt'):
    with open('high_score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# Load background image for the main menu
try:
    background_image = pygame.image.load('3d_sphere.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error:
    background_image = None
    print("Warning: '3d_sphere.png' not found. Main menu will have a solid background.")

# Font setup
font = pygame.font.SysFont(None, 36)
menu_font = pygame.font.SysFont(None, 72)

# Sphere class representing the player
class Sphere:
    def __init__(self):
        self.radius = 30
        self.x = WIDTH // 4
        self.y = HEIGHT - self.radius
        self.vel_y = 0
        self.on_ground = True
        self.speed = 7

    def move(self, keys_pressed):
        # Horizontal movement
        if keys_pressed[pygame.K_LEFT] and self.x - self.radius > 0:
            self.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.x + self.radius < WIDTH:
            self.x += self.speed

        # Jumping
        if keys_pressed[pygame.K_UP] and self.on_ground:
            self.vel_y = -JUMP_STRENGTH
            self.on_ground = False

        # Apply gravity and ground collision
        self.vel_y += GRAVITY
        self.y += self.vel_y
        if self.y + self.radius >= HEIGHT: 
            self.y = HEIGHT - self.radius #prevents from sinking in the ground
            self.vel_y = 0
            self.on_ground = True

    def draw(self, surface):
        pygame.draw.circle(surface, SPHERE_COLOR, (int(self.x), int(self.y)), self.radius)

    def reset(self): #resets sphere's attributes to their initial values, useful after collision
        self.__init__()

# Obstacle class representing the moving obstacles
class Obstacle:
    def __init__(self, speed_multiplier=1):
        self.width = random.randint(20, 40)
        self.height = random.randint(20, 50)
        self.x = WIDTH
        self.y = HEIGHT - self.height
        self.speed = random.randint(3, 6) * speed_multiplier

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, OBSTACLE_COLOR, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)  #: Returns a Rect object representing the obstacle's current position and size.

    def off_screen(self):
        return self.x + self.width < 0

# Function to check collision between sphere and obstacle
def check_collision(sphere, obstacle):
    sphere_rect = pygame.Rect(
        sphere.x - sphere.radius,
        sphere.y - sphere.radius,
        sphere.radius * 2,
        sphere.radius * 2
    )
    return sphere_rect.colliderect(obstacle.get_rect()) #colliderect : A Pygame method that checks if two rectangles overlap.

# Main menu function
def main_menu():
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return  # Start the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Draw the background image or solid color if image not found
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)

        # Render texts
        title_text = menu_font.render("Obstacle Avoidance Game", True, TEXT_COLOR)
        start_text = font.render("Press 'S' to Start or 'Q' to Quit", True, TEXT_COLOR)
        message_text = font.render("Good luck making it to 50 points", True, TEXT_COLOR)
        high_score_text = font.render(f"High Score: {high_score}", True, TEXT_COLOR)

        # Positioning and Displaying Texts
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(message_text, message_rect)
        screen.blit(high_score_text, high_score_rect)

        pygame.display.flip() #Updates the entire display with everything that has been drawn since the last flip.

        clock.tick(60)

# Main game function
def main():
    global high_score
    game_active = True

    while True:
        if game_active:
            main_menu()  # Show the main menu before starting the game

            # Initialize game variables
            player = Sphere()
            obstacles = []
            score = 0
            lives = 2
            spawn_timer = 0
            speed_multiplier = 0.8

            running = True
            while running:
                dt = clock.tick(60) / 1000

                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Player movement
                keys_pressed = pygame.key.get_pressed()
                player.move(keys_pressed) #Calls the move method of the Sphere class, passing in the current keyboard states to update the player's position accordingly

                # Update obstacle spawn timing and difficulty
                spawn_timer += dt
                if score // 10 + 1 > speed_multiplier: 
                    speed_multiplier = score // 10 + 1
                current_spawn_interval = max(0.5, 1.0 - (score // 10) * 0.1)

                if spawn_timer > current_spawn_interval:
                    obstacles.append(Obstacle(speed_multiplier))
                    spawn_timer = 0

                # Move obstacles and check for off-screen obstacles
                for obstacle in obstacles[:]:
                    obstacle.move()
                    if obstacle.off_screen():
                        obstacles.remove(obstacle)
                        score += 1

                # Check for collisions
                collision_occurred = False
                for obstacle in obstacles:
                    if check_collision(player, obstacle):
                        lives -= 1
                        obstacles.remove(obstacle)
                        collision_occurred = True
                        if lives == 0:
                            running = False
                        break

                # Draw game screen
                screen.fill(BACKGROUND_COLOR)
                player.draw(screen)
                for obstacle in obstacles:
                    obstacle.draw(screen)
                score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
                lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
                screen.blit(score_text, (10, 10))
                screen.blit(lives_text, (10, 40))
                pygame.display.flip()

                # Reset player position if collision occurred
                if collision_occurred and lives > 0:
                    player.reset()
                    obstacles.clear()
                    spawn_timer = 0
                    speed_multiplier = 1

            # Update high score if necessary
            if score > high_score:
                high_score = score
                with open('high_score.txt', 'w') as file:
                    file.write(str(high_score))

            # Game over screen with restart and quit options
            game_over_font = pygame.font.SysFont(None, 72)
            game_over_text = game_over_font.render("Game Over", True, TEXT_COLOR)
            final_score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
            high_score_text = font.render(f"High Score: {high_score}", True, TEXT_COLOR)
            restart_text = font.render("Press R to Restart or Q to Quit", True, TEXT_COLOR)

            # Display game over screen
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
            final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            screen.fill(BACKGROUND_COLOR)
            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, final_score_rect)
            screen.blit(high_score_text, high_score_rect)
            screen.blit(restart_text, restart_rect)
            pygame.display.flip()

            # Wait for restart or quit input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game_active = True
                            waiting = False
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
        else:
            pygame.quit()
            sys.exit()

# Run the game
if __name__ == "__main__":
    main()
