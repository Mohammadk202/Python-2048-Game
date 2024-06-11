import numpy as np
import pygame
import random
import sys
import json

# define sizes
WIDTH, HEIGHT = 567, 638
BOARD_WIDTH, BOARD_HEIGHT = 380, 380
X_SHIFT, X_SHIFT2, X_SHIFT3 = 90, 190, 257
Y_SHIFT, Y_SHIFT2, Y_SHIFT3 = 20, 85, 144
GAP = 8
TILE_SIZE = (BOARD_WIDTH - 5 * GAP)//4
COLS, ROWS = 4, 4

# main colors
WHITE = (255, 255, 255)
SCREEN_COLOR = (249, 246, 235)
BOARD_COLOR = (173, 157, 143)
GAME_LABEL_COLOR = (140, 123, 105)
TRANSPARENT_ALPHA = 210

# tiles colors
TILES_COLORS = {
    0: (194, 178, 166),
    2: (233, 221, 209),
    4: (232, 217, 189),
    8: (236, 161, 101),
    16: (241, 130, 80),
    32: (239, 100, 77),
    64: (240, 69, 45),
    128: (230, 197, 94),
    256: (227, 190, 78),
    512: (230, 189, 64),
    1024: (233, 185, 49),
    2048: (233, 187, 32),
    4096: (35, 32, 29),
    8192: (35, 32, 29),
}

# tiles label's colors
LABELS_COLORS = {
    0: (194, 178, 166),
    2: (99, 91, 82),
    4: (99, 91, 82),
    8: WHITE,
    16: WHITE,
    32: WHITE,
    64: WHITE,
    128: WHITE,
    256: WHITE,
    512: WHITE,
    1024: WHITE,
    2048: WHITE,
    4096: WHITE,
    8192: WHITE,
}

# Manages the game score, high score, and the number of rounds played
class ScoreManager:

    # Initializes the ScoreManager with default values and loads previous data
    def __init__(self):
        self.score = 0
        self.best = 0
        self.played_round = 0
        self.load_data()

    # Loads high score and played rounds from a JSON file
    def load_data(self):
        try:
            with open("2048.json", "r") as file:
                data = json.load(file)
                self.best = data.get("best_score", 0)
                print("Best score loaded:", self.best)
                self.played_round = data.get("played_round", 0)
                print("Round played before:", self.played_round)

        except FileNotFoundError:
            print("No previous data found. Starting with default values.")
    
    # save high score and played rounds in a JSON file
    def save_data(self):
        with open("2048.json", "w") as file:
            json.dump({"best_score": self.best, "played_round": self.played_round}, file)

    # Checks if the current score is higher than the best score and updates the JSON file
    def check_highscore(self):
        if self.score >= self.best:
            self.best = self.score
            self.save_data()
            print("New best score saved:", self.best)
                
    # Updates the number of rounds played and saves it to the JSON file
    def played_round_updater(self):
        self.played_round += 1
        self.save_data()
        print("New round played saved:", self.played_round)

    # Resets the score for a new game and increments the played rounds
    def newGame_score(self):
        self.played_round += 1
        self.score = 0
        self.save_data()
        print("Score reset to 0 and played rounds reset.")

     # Resets the score and played rounds to zero
    def reset_score(self):
        self.score = 0
        self.played_round = 0
        self.best = 0
        self.save_data()
        print("Score reset to 0 and played rounds reset 0.")

# Manages the menu display and interactions
class Menu:

     # Initializes the Menu with the screen and prepares button positions and texts
    def __init__(self, screen):
        # SCREEN
        self.screen = screen
        self.gameOver_font = pygame.font.SysFont('comicsans', 30, True)
        self.gameOver_btn_font = pygame.font.SysFont('comicsans', 18, True)

        # VARS for controling start and game over menu
        self.active = True
        self.start = True

    # GAME OVER or Start message
    def create_tryAgain_text(self,tryAgain_text):

        # TRANSPARENT SCREEN
        self.transparent_screen = pygame.Surface( (BOARD_WIDTH, BOARD_HEIGHT) )
        self.transparent_screen.set_alpha( TRANSPARENT_ALPHA )
        self.transparent_screen.fill( WHITE )
        self.screen.blit(self.transparent_screen, (X_SHIFT, Y_SHIFT3))

        # GAME OVER or Start text
        self.go_lbl = self.gameOver_font.render(tryAgain_text, 1, GAME_LABEL_COLOR)
        self.go_pos = (X_SHIFT + BOARD_WIDTH//2 - self.go_lbl.get_rect().width//2, Y_SHIFT3 + BOARD_HEIGHT//2 - self.go_lbl.get_rect().height//2 - 35)
        self.screen.blit(self.go_lbl, self.go_pos)

    # Draws the buttons on the screen
    def create_tryagain_btn(self,btn_text):
        self.tryAgain_btn = pygame.draw.rect(self.screen, GAME_LABEL_COLOR ,(X_SHIFT + BOARD_WIDTH//3, Y_SHIFT3 + BOARD_HEIGHT//2 , 125 , 40))
        self.tryAgain_text = self.gameOver_btn_font.render(btn_text, 1, WHITE)
        self.screen.blit(
            self.tryAgain_text,
            (X_SHIFT + BOARD_WIDTH//3  + 130//2 - self.tryAgain_text.get_width()//2,
              Y_SHIFT3 + BOARD_HEIGHT//2  + 40//2 - self.tryAgain_text.get_height()//2),
            )

    # method for showing start and game over menus
    def show(self):
        if self.active or self.start:
            if self.start:
              # Start label
              self.create_tryAgain_text("Lets Start The Game!")
              # Start button
              self.create_tryagain_btn("Start")
            else:
              # GAME OVER label
              self.create_tryAgain_text("Game Over!")
              # TRY AGAIN button
              self.create_tryagain_btn("Try Again")

    def hide(self, bg):
        #make game over & start menu hidden
        self.active = False #if ture shows game over menu
        self.start = False  #if true shows start menu

        pygame.draw.rect(self.screen, BOARD_COLOR, bg)

class GUI:

    def __init__(self, screen):
        # Initializes the GUI with necessary elements
        self.screen = screen
        self.FONT = pygame.font.SysFont("comicsans", 35, bold=True)
        self.score_font = pygame.font.SysFont("comicsans", 15, bold=True)
        self.btn_font = pygame.font.SysFont("comicsans", 18, bold=True)

         # Create a rectangle for the 'Try Again' button
        self.tryagain_btn_rect= pygame.draw.rect(self.screen, GAME_LABEL_COLOR ,(X_SHIFT + BOARD_WIDTH//3, Y_SHIFT3 + BOARD_HEIGHT//2 , 125 , 40))

         # Initialize the menu with the game screen
        self.menu = Menu( screen )

    # Draw the game board rectangle on the screen
    def create_board(self):
        self.board_rect = pygame.draw.rect(self.screen, BOARD_COLOR, (X_SHIFT, Y_SHIFT3, BOARD_WIDTH, BOARD_HEIGHT))

    # Draw the logo box and display the '2048' game title
    def create_logo_box(self):
        self.logo = pygame.draw.rect(self.screen, SCREEN_COLOR ,(X_SHIFT, Y_SHIFT, 95 , 45))
        self.text_logo = self.FONT.render("2048", 1, GAME_LABEL_COLOR)
        self.screen.blit(
            self.text_logo,
            (X_SHIFT + 95//2 - self.text_logo.get_width()//2,
              Y_SHIFT + 45//2 - self.text_logo.get_height()//2),
        )

    # Draw a welcome message box
    def create_welcome(self):
        self.logo = pygame.draw.rect(self.screen, SCREEN_COLOR ,(X_SHIFT, Y_SHIFT2, 95 , 42))
        self.text_welcome = self.btn_font.render("welcome!", 1, GAME_LABEL_COLOR)
        self.screen.blit(
            self.text_welcome,
            (X_SHIFT + 95//2 - self.text_welcome.get_width()//2,
              Y_SHIFT2 + 40//2 - self.text_welcome.get_height()//2),
        )

    # Draw the score box and display the current score
    def create_score_box(self,score_value):
        self.score_rect = pygame.draw.rect(self.screen, BOARD_COLOR ,(X_SHIFT2, Y_SHIFT, 90 , 43))
        self.text_score = self.score_font.render("Score:", 1, WHITE)
        self.screen.blit(
            self.text_score,
            (X_SHIFT2 + 92//2 - self.text_score.get_width()//2,
              Y_SHIFT + 42//4 - self.text_score.get_height()//2),
        )

        self.score_label = self.score_font.render(str(score_value) , 1, WHITE)
        self.screen.blit(
            self.score_label,
            (X_SHIFT2 + 92//2 - self.score_label.get_width()//2,
              Y_SHIFT + 3*42//4 - self.score_label.get_height()//2),
        )

    # Draw the best score box and display the highest score
    def create_best_box(self,best_value):
        self.score_rect = pygame.draw.rect(self.screen, BOARD_COLOR ,(X_SHIFT2 + 94, Y_SHIFT, 90 , 43))
        self.text_best = self.score_font.render("Best:", 1, WHITE)
        self.screen.blit(
            self.text_best,
            (X_SHIFT2 + 94 + 90//2 - self.text_best.get_width()//2,
              Y_SHIFT + 42//4 - self.text_best.get_height()//2),
        )
        self.best_label = self.score_font.render(str(best_value) , 1, WHITE)
        self.screen.blit(
            self.best_label,
            (X_SHIFT2 + 94 + 90//2 - self.best_label.get_width()//2,
              Y_SHIFT + 3*42//4 - self.best_label.get_height()//2),
        )

    # Draw the round number box and display the number of rounds played
    def create_round_box(self,round_played):
        self.round_rect = pygame.draw.rect(self.screen, BOARD_COLOR ,(X_SHIFT2 + 94*2, Y_SHIFT, 90 , 43))
        self.text_round = self.score_font.render("Round:", 1, WHITE)
        self.screen.blit(
            self.text_round,
            (X_SHIFT2 + 94*2 + 90//2 - self.text_round.get_width()//2,
              Y_SHIFT + 42//4 - self.text_round.get_height()//2),
        )
        self.round_label = self.score_font.render(str(round_played) , 1, WHITE)
        self.screen.blit(
            self.round_label,
            (X_SHIFT2 + 94*2 + 90//2 - self.round_label.get_width()//2,
              Y_SHIFT + 3*42//4 - self.round_label.get_height()//2),
        )

    # Draw the 'New Game' button
    def create_NewGame_btn(self):
        self.newGame_btn = pygame.draw.rect(self.screen, GAME_LABEL_COLOR ,(X_SHIFT2, Y_SHIFT2, 137 , 43))

        self.text_NewGame = self.btn_font.render("New Game", 1, WHITE)
        self.screen.blit(
            self.text_NewGame,
            (X_SHIFT2 + 137//2 - self.text_NewGame.get_width()//2,
              Y_SHIFT2 + 40//2 - self.text_NewGame.get_height()//2),
        )

    # Draw the 'Reset Game' button 
    def create_reset_btn(self):
        self.reset_btn = pygame.draw.rect(self.screen, GAME_LABEL_COLOR ,(X_SHIFT2 + 141 , Y_SHIFT2, 137 , 43))

        self.text_reset = self.btn_font.render("Reset Game", 1, WHITE)
        self.screen.blit(
            self.text_reset,
            (X_SHIFT2 + 141 + 137//2 - self.text_reset.get_width()//2,
              Y_SHIFT2 + 40//2 - self.text_reset.get_height()//2),
        )
    
    #Show initial screen elements
    def show_start(self):
        #Logo 2048 draw
        self.create_logo_box()
        #Welcome message
        self.create_welcome()
        #Score box
        self.create_score_box(score_value=0)
        #Best score box
        self.create_best_box(best_value =0)
        #NUmber of played round
        self.create_round_box(round_played = 0)
        #new game button draw
        self.create_NewGame_btn()
        #Reset game button draw
        self.create_reset_btn()
        #Board draw
        self.create_board()

    # Update score, best score, and round played display
    def update_scores(self, score_value, best_value , round_played):
        #Update score box value
        self.create_score_box(score_value)
        #Update best score box value
        self.create_best_box(best_value)
        #Update round played box value
        self.create_round_box(round_played)

    # Listen for and handle menu and button click events
    def action_listener(self, event):
        # MENU
        if self.menu.active or self.menu.start:
            if self.menu.tryAgain_btn.collidepoint(event.pos):
                self.menu.hide(self.board_rect)
                return True
        if self.newGame_btn.collidepoint(event.pos):
            return True
        elif self.reset_btn.collidepoint(event.pos):
            return True
        
        return False

class Game:

    def __init__(self, screen):
        # Initialize the game screen
        self.screen = screen
        # Initialize the game tiles with zeros
        self.tiles = np.zeros( (ROWS, COLS) )
        # Initialize the GUI
        self.gui = GUI(screen)
        # Initialize the score manager
        self.score_manager = ScoreManager()
         # Set the font for tile labels
        self.tiles_font = pygame.font.SysFont('comicsans', 40, bold=True)
        # Variables to control game state
        self.generate = False #Flag of generating new tile
        self.playing = True #Flag of game continue running

   # Draw the game board and tile values
    def draw_board(self):
        row_Shift, col_Shift = GAP, GAP
        for row in range(ROWS):
            for col in range(COLS):
                tile_num = int(self.tiles[row][col])
                
                # Draw the tile with the appropriate color
                tile_color = TILES_COLORS[tile_num]
                pygame.draw.rect(self.screen, tile_color, (X_SHIFT + col_Shift + col * TILE_SIZE, Y_SHIFT3 + row_Shift + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                # Draw the label (number) on the tile
                tile_label_color = LABELS_COLORS[tile_num]
                tile_label = self.tiles_font.render(str(tile_num), 1, tile_label_color)
                tile_label_pos = (X_SHIFT + col_Shift + col * TILE_SIZE + TILE_SIZE//2 - tile_label.get_rect().width//2, Y_SHIFT3 + row_Shift + row * TILE_SIZE + TILE_SIZE//2 - tile_label.get_rect().height//2)
                self.screen.blit(tile_label, tile_label_pos)

                col_Shift += GAP

            row_Shift += GAP
            col_Shift = GAP

    # Generate new tiles in empty positions
    def generate_tiles(self, first=False):
        empty_tiles = []

        for row in range(ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == 0: empty_tiles.append( (row, col) )
        
        empty_tile_index = random.randrange(0, len(empty_tiles))
        row, col = empty_tiles[empty_tile_index]
        ranndom_num = random.randint(1, 10)
        tile_value = 2 if first or ranndom_num <= 7 else 4
        self.tiles[row][col] = tile_value

    # Move and merge tiles based on the direction
    def __move_and_merge(self, direction, row, col):
        dx, dy = 0, 0
        if direction == 'UP': dy = -1
        elif direction == 'DOWN': dy = 1
        elif direction == 'RIGHT': dx = 1
        elif direction == 'LEFT': dx = -1

        try:
            # Move tiles
            if self.tiles[row + dy][col + dx] == 0:
                value = self.tiles[row][col]
                self.tiles[row][col] = 0
                self.tiles[row + dy][col + dx] = value
                self.generate = True
                self.__move_and_merge(direction, row + dy, col + dx)
            # Merge tiles
            elif self.tiles[row][col] == self.tiles[row + dy][col + dx]:
                self.tiles[row][col] = 0
                self.tiles[row + dy][col + dx] *= 2
                self.score_manager.score += int(self.tiles[row + dy][col + dx])
                self.generate = True
        except IndexError: return

    # Slide tiles based on the direction
    def slide_tiles(self, direction):
        
        if direction == 'UP':
            for row in range(1, ROWS):
                for col in range(COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)

        if direction == 'DOWN':
            for row in range(ROWS-2, -1, -1):
                for col in range(COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)

        if direction == 'RIGHT':
            for row in range(ROWS):
                for col in range(COLS-2, -1, -1):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)

        if direction == 'LEFT':
            for row in range(ROWS):
                for col in range(1, COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)

    # Check if the board is full
    def __is_full_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == 0: return False
        return True
    
    # Check if no more moves are available
    def __no_more_moves(self):
        # UP
        for row in range(1, ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == self.tiles[row-1][col]: return False

        # DOWN
        for row in range(ROWS-2, -1, -1):
            for col in range(COLS):
                if self.tiles[row][col] == self.tiles[row+1][col]: return False

        # RIIGHT
        for row in range(ROWS):
            for col in range(COLS-2, -1, -1):
                if self.tiles[row][col] == self.tiles[row][col+1]: return False

        # LEFT
        for row in range(ROWS):
            for col in range(1, COLS):
                if self.tiles[row][col] == self.tiles[row][col-1]: return False
        
        return True

    # Check if the game is over
    def is_game_over(self):
        if self.__is_full_board():
            return self.__no_more_moves()
        
    # Start a new game
    def new(self):
        self.tiles = np.zeros( (ROWS, COLS) )
        self.score_manager.newGame_score()
        self.generate_tiles()
        
    # Reset the game 
    def rst(self):
        self.tiles = np.zeros( (ROWS, COLS) )
        self.score_manager.reset_score()
        self.generate_tiles()

def main():

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
    pygame.display.set_caption('2048')
    pygame.display.set_icon(pygame.image.load("images/2048_logo.png"))
    screen.fill( SCREEN_COLOR )

    # Initialize the Game object
    game = Game(screen)

    # Initial GUI setup - GUI initial call
    game.gui.show_start()

    # Initial tiles displayed
    for i in range(2): game.generate_tiles(True)

    # Main game loop
    while game.playing:

        # Update & draw the game board
        game.draw_board()

        # Display the menu if active
        game.gui.menu.show()

        # Update the scores in the GUI
        game.gui.update_scores(game.score_manager.score, game.score_manager.best ,game.score_manager.played_round)

        # Event handling
        for event in pygame.event.get():

            # Handle quit event
            if event.type == pygame.QUIT:
                game.score_manager.played_round_updater()
                sys.exit()

            # Handle keydown events
            if event.type == pygame.KEYDOWN:
                
                #Slide tiles UP
                if event.key == pygame.K_UP:
                    game.slide_tiles('UP')
                    game.score_manager.check_highscore()
                    
                
                #Slide tiles DOWN
                if event.key == pygame.K_DOWN:
                    game.slide_tiles('DOWN')
                    game.score_manager.check_highscore()

                #Slide tiles RIGHT
                if event.key == pygame.K_RIGHT:
                    game.slide_tiles('RIGHT')
                    game.score_manager.check_highscore()

                #Slide tiles LEFT
                if event.key == pygame.K_LEFT:
                    game.slide_tiles('LEFT')
                    game.score_manager.check_highscore()

                # Generate new tiles if a move was made
                if game.generate:
                    game.generate_tiles()
                    game.generate = False
            
            # Handle mouse button events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                 if game.gui.newGame_btn.collidepoint(event.pos) or game.gui.menu.tryAgain_btn.collidepoint(event.pos): 
                    if game.gui.action_listener(event):
                      game.new()
                 elif game.gui.reset_btn.collidepoint(event.pos):
                    if game.gui.action_listener(event):
                       game.rst() 
                       print("btn")

            
        # Check if the game is over
        if game.is_game_over():
            game.gui.menu.active = True
            
        # game.score_manager.check_highscore()

        # Update the display
        pygame.display.update()

# Start the main function
if __name__ == "__main__":
    main()