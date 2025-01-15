import pygame
import sys
import os

# Path Handling

if getattr(sys, 'frozen', False):
    # Running as a bundled executable, look for the DLL in the same directory
    dll_path = os.path.join(sys._MEIPASS, 'SDL2.dll')
    os.environ['PATH'] = os.path.dirname(dll_path) + os.pathsep + os.environ['PATH']
else:
    # Running as a script, ensure DLL is in the working directory
    dll_path = 'SDL2.dll'
    os.environ['PATH'] = os.path.dirname(dll_path) + os.pathsep + os.environ['PATH']


#
## 
### Create Window
##
#

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKER_BLUE = (135, 206, 250)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Little Guy's Adventure")

#
## 
### Load Assets
##
#

# Determine the correct path for assets
def get_asset_path(filename):
    if getattr(sys, 'frozen', False):
        # If running as a bundled executable, get the path from sys._MEIPASS
        return os.path.join(sys._MEIPASS, 'assets', filename)
    else:
        # If running as a Python script, use the script's directory
        return os.path.join(os.path.dirname(__file__), 'assets', filename)

# Load assets using the function
background = pygame.image.load(get_asset_path("Sky.png"))
player_image = pygame.image.load(get_asset_path("Little-Guy.png"))
player_image = pygame.transform.scale(player_image, (14, 32))
platform_image = pygame.image.load(get_asset_path("Ground.png"))
cloud_image = pygame.image.load(get_asset_path("Cloud.png")).convert_alpha()
earlyspacecloud_image = pygame.image.load(get_asset_path("earlyspacecloud.png")).convert_alpha()
midspacecloud_image = pygame.image.load(get_asset_path("midspacecloud.png"))
latespacecloud_image = pygame.image.load(get_asset_path("latespacecloud.png"))
ground_image = pygame.image.load(get_asset_path("groundimage.png")).convert_alpha()
ground_rect = ground_image.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
cloud_rect = cloud_image.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
earlyspacecloud_rect = earlyspacecloud_image.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
midspacecloud_rect = midspacecloud_image.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
latespacecloud_rect = latespacecloud_image.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
skytransition_background = pygame.image.load(get_asset_path("skytransition.png"))
earlyspacetransition_background = pygame.image.load(get_asset_path("earlyspacetransition.png"))
midspacetransition_background = pygame.image.load(get_asset_path("midspacetransition.png"))
latespacetransition_background = pygame.image.load(get_asset_path("latespacetransition.png"))
littleguywon = pygame.image.load(get_asset_path("littleguywon.png")).convert()
littleguywon = pygame.transform.scale(littleguywon, (SCREEN_WIDTH, SCREEN_HEIGHT))


#
## 
### Player Settings
##
#

player_pos = [100, 500]
player_speed = 5
gravity = 0.5
jump_strength = -10
velocity_y = 0
is_jumping = False

#
## 
### Platform Settings
##
#

platforms = [
    pygame.Rect(200, 450, 40, 40),
    pygame.Rect(300, 380, 40, 40),
    pygame.Rect(480, 380, 40, 40),
    pygame.Rect(580, 290, 40, 40),
    pygame.Rect(410, 200, 40, 40),
    pygame.Rect(330, 110, 40, 40),
    pygame.Rect(200, 200, 40, 40),
    pygame.Rect(40, 110, 40, 40),
    pygame.Rect(120, 33, 40, 40),
]

skytransition_platforms = [
    pygame.Rect(100, 500, 40, 40),
    pygame.Rect(200, 400, 40, 40),
    pygame.Rect(400, 400, 40, 40),
    pygame.Rect(590, 500, 40, 40),
    pygame.Rect(740, 420, 40, 40),
    pygame.Rect(630, 320, 40, 40),
    pygame.Rect(740, 240, 40, 40),
    pygame.Rect(740, 120, 40, 40),
    pygame.Rect(540, 160, 40, 40),
    pygame.Rect(340, 160, 40, 40),
    pygame.Rect(180, 120, 40, 40),
    pygame.Rect(100, 40, 40, 40),
]

earlyspacetransition_platforms = [
    pygame.Rect(100, 500, 40, 40),
    pygame.Rect(40, 400, 40, 40),
    pygame.Rect(40, 300, 40, 40),
    pygame.Rect(310, 350, 40, 40),
    pygame.Rect(580, 400, 40, 40),
    pygame.Rect(690, 320, 40, 40),
    pygame.Rect(740, 220, 40, 40),
    pygame.Rect(740, 120, 40, 40),
    pygame.Rect(470, 120, 40, 40),
    pygame.Rect(470, 35, 40, 40),
    pygame.Rect(280, 120, 40, 40),
    pygame.Rect(100, 40, 40, 40),
]

midspacetransition_platforms = [
    pygame.Rect(100, 570, 40, 40),
    pygame.Rect(340, 570, 40, 40),
    pygame.Rect(400, 390, 40, 40),
    pygame.Rect(590, 570, 40, 40),
    pygame.Rect(740, 490, 40, 40),
    pygame.Rect(630, 390, 40, 40),
    pygame.Rect(170, 390, 40, 40),
    pygame.Rect(40, 240, 40, 40),
    pygame.Rect(270, 210, 40, 40),
    pygame.Rect(500, 210, 40, 40),
    pygame.Rect(730, 210, 40, 40),
    pygame.Rect(730, 90, 40, 40),
    pygame.Rect(500, 15, 40, 40),
    pygame.Rect(270, 15, 40, 40),
    pygame.Rect(40, 15, 40, 40),
]

latespacetransition_platforms = [
    pygame.Rect(100, 540, 40, 40),
    pygame.Rect(200, 400, 40, 40),
    pygame.Rect(300, 260, 40, 40),
    pygame.Rect(560, 460, 40, 40),
    pygame.Rect(740, 420, 40, 40),
    pygame.Rect(740, 270, 40, 40),
    pygame.Rect(740, 150, 40, 40),
    pygame.Rect(740, 30, 40, 40),
    pygame.Rect(510, 30, 40, 40),
    pygame.Rect(280, 30, 40, 40),
    pygame.Rect(30, 30, 40, 40)
]

littleguywon_platforms = [
    pygame.Rect(0, 0, 0, 0)
]

littleguywonplatform_y = SCREEN_HEIGHT - 32
littleguywonplatform_rect = pygame.Rect(0, littleguywonplatform_y, SCREEN_WIDTH, 40)

#
## 
### Frame Rate
##
#

clock = pygame.time.Clock()

#
## 
### Main Menu
##
#

def main_menu():
    font = pygame.font.Font(None, 74)
    header_font = pygame.font.Font(None, 80)
    BUTTON_COLOR = (50, 150, 255)
    BUTTON_HOVER_COLOR = (30, 130, 230)
    BUTTON_OUTLINE_COLOR = WHITE

    play_text = font.render("Play", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    header_text = header_font.render("Little Guy's Adventure", True, WHITE)
    shadow_text = header_font.render("Little Guy's Adventure", True, (50, 50, 50))
    play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 70)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 70)

    # Load the background image
    background_image = pygame.image.load(get_asset_path('imageinmenu.png'))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw header shadow and text with outline
        shadow_offset = 5
        screen.blit(shadow_text, (SCREEN_WIDTH // 2 - shadow_text.get_width() // 2 + shadow_offset, 45 + shadow_offset))
        outline_offset = 2
        for dx, dy in [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]:
            outline_text = header_font.render("Little Guy's Adventure", True, BLACK)
            screen.blit(outline_text, (SCREEN_WIDTH // 2 - outline_text.get_width() // 2 + dx, 45 + dy))
        screen.blit(header_text, (SCREEN_WIDTH // 2 - header_text.get_width() // 2, 45))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw Play button
        if play_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, play_button)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, play_button)
        pygame.draw.rect(screen, BUTTON_OUTLINE_COLOR, play_button, 3)
        screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2, play_button.centery - play_text.get_height() // 2))

        # Draw Quit button
        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, quit_button)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, quit_button)
        pygame.draw.rect(screen, BUTTON_OUTLINE_COLOR, quit_button, 3)
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.collidepoint(mouse_pos):
                        reset_game()
                        game_loop()
                    if quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()


#
## 
### Game Loop
##
#

# Initialize prev_background and prev_platforms outside the game loop
prev_background = None
prev_platforms = None

def reset_game():
    global player_pos, velocity_y, is_jumping, background, platforms, prev_background, prev_platforms, ground_rect, in_skytransition

    player_pos = [100, 500]
    velocity_y = 0
    is_jumping = False
    background = pygame.image.load(get_asset_path("Sky.png"))
    platforms = [
        pygame.Rect(200, 450, 40, 40),
        pygame.Rect(300, 380, 40, 40),
        pygame.Rect(480, 380, 40, 40),
        pygame.Rect(580, 290, 40, 40),
        pygame.Rect(410, 200, 40, 40),
        pygame.Rect(330, 110, 40, 40),
        pygame.Rect(200, 200, 40, 40),
        pygame.Rect(40, 110, 40, 40),
        pygame.Rect(120, 33, 40, 40),
    ]

    prev_background = None
    prev_platforms = None
    ground_rect = ground_image.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    in_skytransition = False

def game_loop():
    global player_pos, velocity_y, is_jumping, background, platforms, prev_background, prev_platforms, ground_rect, in_skytransition, in_secondtransition

    player_height = player_image.get_height()
    on_last_platform = False
    in_skytransition = False
    in_secondtransition = False
    in_thirdtransition = False
    in_fourthtransition = False

    while True:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and not is_jumping:
            velocity_y = jump_strength
            is_jumping = True

        # Apply gravity
        velocity_y += gravity
        player_pos[1] += velocity_y
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 14, 32)

        is_on_platform = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                if velocity_y > 0: 
                    velocity_y = 0
                    is_jumping = False
                    player_pos[1] = platform.top - player_height 

                # Check for last platform in any scene
                if platform == platforms[-1]: 
                    on_last_platform = True
                else:
                    on_last_platform = False

                is_on_platform = True
                on_last_platform = is_on_platform and platform == platforms[-1] 
                break

        
        # Check collision with the ground (only for the original scene, not the transition)
        if background != earlyspacetransition_background and background != skytransition_background and background != midspacetransition_background and background != latespacetransition_background:
            if player_rect.colliderect(ground_rect):
                velocity_y = 0
                is_jumping = False
                player_pos[1] = ground_rect.top - player_height

        if player_rect.colliderect(littleguywonplatform_rect):
            player_rect.bottom = littleguywonplatform_rect.top
            velocity_y = 0

        # Check if player falls below the screen
        if player_pos[1] > SCREEN_HEIGHT:
            if in_fourthtransition:
                reset_game()
                in_fourthtransition = False
            elif in_thirdtransition:
                reset_game()
                in_thirdtransition = False
            elif in_secondtransition:
                reset_game()
                in_secondtransition = False
            elif in_skytransition:
                reset_game()
                in_skytransition = False
            else:
                game_end()


        # Handle transition to the skytransition background
        if on_last_platform and velocity_y < 0 and background == latespacetransition_background: 
            prev_background = background
            prev_platforms = platforms
            background = littleguywon
            platforms = littleguywon_platforms
            player_pos = [0, 0]
            velocity_y = 0
            is_jumping = False
            in_skytransition = False 
            in_secondtransition = False 
            in_thirdtransition = False
            in_fourthtransition = True
            on_last_platform = False
            game_end()

        elif on_last_platform and velocity_y < 0 and background == midspacetransition_background: 
            prev_background = background
            prev_platforms = platforms
            background = latespacetransition_background
            platforms = latespacetransition_platforms
            player_pos = [100, SCREEN_HEIGHT - 100] 
            velocity_y = 0
            is_jumping = False
            in_skytransition = False 
            in_secondtransition = False 
            in_thirdtransition = False
            in_fourthtransition = True
            on_last_platform = False

        elif on_last_platform and velocity_y < 0 and background == earlyspacetransition_background: 
            prev_background = background
            prev_platforms = platforms
            background = midspacetransition_background
            platforms = midspacetransition_platforms
            player_pos = [100, SCREEN_HEIGHT - 100] 
            velocity_y = 0
            is_jumping = False
            in_skytransition = False 
            in_secondtransition = False 
            in_thirdtransition = True 
            in_fourthtransition = False
            on_last_platform = False

        elif on_last_platform and velocity_y < 0 and background == skytransition_background:
            # Save the current scene state before transitioning
            prev_background = background
            prev_platforms = platforms

            # Transition to the new scene
            background = earlyspacetransition_background
            platforms = earlyspacetransition_platforms
            player_pos = [100, SCREEN_HEIGHT - 100]
            velocity_y = 0
            is_jumping = False
            in_skytransition = False
            in_secondtransition = True
            in_thirdtransition = False
            in_fourthtransition = False
            on_last_platform = False

        elif on_last_platform and velocity_y < 0 and not in_skytransition:
            # Save the current scene state before transitioning
            prev_background = background
            prev_platforms = platforms

            # Transition to the new scene
            background = skytransition_background
            platforms = skytransition_platforms
            player_pos = [100, SCREEN_HEIGHT - 100]
            velocity_y = 0
            is_jumping = False
            in_skytransition = True
            in_secondtransition = False
            in_thirdtransition = False
            in_fourthtransition = False
            on_last_platform = False
        

        # Prevent player from going out of bounds on the x-axis
        if player_pos[0] < 0:
            player_pos[0] = 0
        elif player_pos[0] > SCREEN_WIDTH - 50:
            player_pos[0] = SCREEN_WIDTH - 50

        # Draw platforms
        if background != earlyspacetransition_background and background != skytransition_background and background != midspacetransition_background and background != latespacetransition_background:
            for platform in platforms:
                screen.blit(platform_image, platform.topleft)

        # Draw player
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        # Only draw the ground if not in the skytransition or second transition scene
        if background == littleguywon:
            screen.blit(littleguywon, (0, 0))
        if background != earlyspacetransition_background and background != skytransition_background and background != midspacetransition_background and background != latespacetransition_background and background != littleguywon:
            screen.blit(ground_image, ground_rect.topleft)

        if background == latespacetransition_background:
            for platform in latespacetransition_platforms:
                screen.blit(latespacecloud_image, platform.topleft)
        elif background == midspacetransition_background:
            for platform in midspacetransition_platforms:
                screen.blit(midspacecloud_image, platform.topleft)
        elif background == earlyspacetransition_background:
            for platform in earlyspacetransition_platforms:
                screen.blit(earlyspacecloud_image, platform.topleft)
        elif background == skytransition_background:
            for platform in skytransition_platforms:
                screen.blit(cloud_image, platform.topleft)

        pygame.display.flip()
        clock.tick(60)



# Inside game_end, call reset_game before the retry
def game_end():
    font = pygame.font.Font(None, 74)
    header_font = pygame.font.Font(None, 80)
    BUTTON_COLOR = (50, 150, 255)
    BUTTON_HOVER_COLOR = (30, 130, 230)
    BUTTON_OUTLINE_COLOR = WHITE

    retry_text = font.render("Retry", True, WHITE)
    menu_text = font.render("Menu", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    header_text = header_font.render("Game Over", True, WHITE)
    shadow_text = header_font.render("Game Over", True, (50, 50, 50))

    retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 70)
    menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 70)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 70)

    while True:
        screen.fill(DARKER_BLUE)  # Fill the screen with the background color
        
        if background == littleguywon:
            # Draw the littleguywon background (assuming you already have it as a surface or image)
            screen.blit(littleguywon, (0, 0))

            # Create the "Little Guy Won!" text with shadow and outline
            won_text = header_font.render("Little Guy Won!", True, WHITE)
            shadow_won_text = header_font.render("Little Guy Won!", True, BLACK)
            
            # Position the text at the center of the screen
            won_text_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            shadow_won_text_rect = shadow_won_text.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 2 - 98))  # Shadow offset

            # Draw the shadow first (behind the text)
            screen.blit(shadow_won_text, shadow_won_text_rect)
            
            # Draw the actual "Little Guy Won!" text
            screen.blit(won_text, won_text_rect)

        else:
            # Draw header shadow and text with outline for "Game Over"
            shadow_offset = 5
            screen.blit(shadow_text, (SCREEN_WIDTH // 2 - shadow_text.get_width() // 2 + shadow_offset, 45 + shadow_offset))
            outline_offset = 2
            for dx, dy in [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]:
                outline_text = header_font.render("Game Over", True, BLACK)
                screen.blit(outline_text, (SCREEN_WIDTH // 2 - outline_text.get_width() // 2 + dx, 45 + dy))
            screen.blit(header_text, (SCREEN_WIDTH // 2 - header_text.get_width() // 2, 45))

            # Draw Retry button
            mouse_pos = pygame.mouse.get_pos()
            if retry_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, retry_button)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, retry_button)
            pygame.draw.rect(screen, BUTTON_OUTLINE_COLOR, retry_button, 3)
            screen.blit(retry_text, (retry_button.centerx - retry_text.get_width() // 2, retry_button.centery - retry_text.get_height() // 2))

        # Draw Menu button
        mouse_pos = pygame.mouse.get_pos()
        if menu_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, menu_button)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, menu_button)
        pygame.draw.rect(screen, BUTTON_OUTLINE_COLOR, menu_button, 3)
        screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2))

        # Draw Quit button
        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, quit_button)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, quit_button)
        pygame.draw.rect(screen, BUTTON_OUTLINE_COLOR, quit_button, 3)
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

        pygame.display.flip()

        # Handle user input for buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if retry_button.collidepoint(mouse_pos):
                        reset_game()  # Reset game state here
                        game_loop()   # Restart the game
                    if menu_button.collidepoint(mouse_pos):
                        main_menu()
                    if quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()


# Start the game by showing the main menu
main_menu()
