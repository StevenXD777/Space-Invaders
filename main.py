import pygame, sys, random
from game import Game

pygame.init()

# Identify size of the windows
width = 750
height = 700
offset = 50

# Colours
grey = (30, 29, 27)
yellow = (243, 216, 63)

# Background Settings
background = pygame.image.load("Graphics/space_background.jpg")
background = pygame.transform.scale(background, (width + offset, height + (2 * offset)))
background_position = 0
speed = 0.7

# Chosen Font and Texts for the User Interface
font = pygame.font.Font("Font/monogram.ttf", 40)
bigger_font = pygame.font.Font("Font/monogram.ttf", 55)
level_text_surface = font.render("Level", False, yellow)
game_over_surface = font.render("GAME OVER", False, yellow)
pause_text_surface = font.render("GAME PAUSED", False, yellow)
restart_surface = font.render("PRESS SPACEBAR TO RESTART", False, yellow)
score_text_surface = font.render("SCORE:", False, yellow)
highscore_text_surface = font.render("HIGH-SCORE", False, yellow)

# Set caption and window size
screen = pygame.display.set_mode((width + offset, height + (2 * offset)))
pygame.display.set_caption("Python Space Invaders")

# Implement time in game
clock = pygame.time.Clock()
time_delay = 3000
transition_time = None

# Implementing game object with all the objects within that game object
game = Game(width, height, offset)

# Creating custom event when an alien shoots a laser
shoot_laser = pygame.USEREVENT

# Game shoots lasers from aliens for this specified amount of time
pygame.time.set_timer(shoot_laser, 600)

mysteryShip = pygame.USEREVENT + 1
pygame.time.set_timer(mysteryShip, random.randint(4000, 8000))

while True:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == shoot_laser and game.run:
            game.alien_shoot_laser()

        if event.type == mysteryShip and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(mysteryShip, random.randint(4000, 8000))

        # Restarting Game
        if keys[pygame.K_SPACE] and game.run == False:
            game.select_sound.play()
            game.reset()

        # Q key to quit the game
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

        # M key to mute and unmute the game music
        if keys[pygame.K_m]:
            if game.music_running == True:
                pygame.mixer_music.pause()
                game.music_running = False
            else:    
                pygame.mixer_music.unpause()
                game.music_running = True
        
        # N debug key to remove all the aliens
        if keys[pygame.K_n]:
            game.aliens_group.empty()

        if keys[pygame.K_ESCAPE] and game.lives != 0:
            game.select_sound.play()
            if game.run == True:
                game.run = False
            elif game.run == False:
                game.run = True

        #if keys[pygame.K_ESCAPE] and game.run == False:
        #    game.run = True

    # Updating
    if game.run:
        
        # Moving Background
        background_position -= speed

        if background_position <= -(height + (2 * offset)):
            background_position = 0

        screen.blit(background, (0, background_position))
        screen.blit(background, (0, background_position + height + (2 * offset)))

        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()
        
        if len(game.aliens_group) == 0:
            if transition_time is None:
                transition_time = pygame.time.get_ticks()

            current_time = pygame.time.get_ticks()
            
            '''
            if current_time - transition_time >= time_delay:
                game.next_level()
            '''
            if current_time - transition_time < time_delay:
                # Displaying countdown message
                countdown_seconds = (time_delay - (current_time - transition_time)) // 1000 + 1
                countdown_text = bigger_font.render(f"NEXT LEVEL IN {countdown_seconds}", True, yellow)
                screen.blit(countdown_text, (235, 250))
            else:
                # Move to the next level
                game.next_level()
                transition_time = None

    # Set Screen to Grey
    #screen.fill(grey)

    

    # Drawing User interface
    pygame.draw.rect(screen, yellow, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, yellow, (25, 730), (775, 730), 3)
    
    if game.run:
        screen.blit(level_text_surface, (570, 740, 50, 50))
        formatted_level = str(game.level)
        level_surface = font.render(formatted_level, False, yellow)
        screen.blit(level_surface, (660, 740, 50, 50))
    elif game.run == False and game.lives != 0:
        screen.blit(pause_text_surface, (300, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (530, 840, 50, 50))
        screen.blit(restart_surface, (10 + offset, 740))

    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 745))
        x += 50

    screen.blit(score_text_surface, (50,15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, yellow)
    screen.blit(score_surface, (140, 15, 50, 50))
    
    screen.blit(highscore_text_surface, (550, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, yellow)
    screen.blit(highscore_surface, (585, 40, 50, 50))

    # Drawing spaceship and laser objects from game object
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)

    # Drawing obstacle object from game object
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)

    # Drawing aliens
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)

    # Drawing mysteryShip
    game.mystery_ship_group.draw(screen)

    pygame.display.update()
    clock.tick(60) # Run 60 times in a second (Frame Rate)