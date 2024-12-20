import pygame
from sys import exit
from button import*
from create_furniture import create_furniture
from player import Player
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Pet_Page:
    def __init__(self, player: Player, index, screen: pygame.Surface):
        """
        Initialises the Milestone assets.
        """
        self.player = player
        self.screen = screen
        self.pet = self.player.pets[index]


        # Fonts
        self.font = pygame.font.Font(None, 30)

        # Load assets
        self.pet_page_surface = pygame.image.load("assets/pet_page/ground.png").convert_alpha()
        self.pet_store = pygame.image.load("assets/pet_page/pet_store.png")

        image_name = str(index) + ".png"
        self.pet_rank = pygame.image.load("assets/pet_page/" + image_name).convert_alpha()
        self.wooden_loading_bar = pygame.image.load("assets/pet_page/wooden_loading_bar_1.png").convert_alpha()


        # Buttons
        self.store_button = LongButton(700, 20, 200, 40, 'Shop')
        self.chat_button = LongButton(700, 90, 200, 40, 'Chat')
        self.return_button = LongButton(700, 160, 200, 40, 'Return')

        self.ratio = self.pet.saved / self.pet.target

       
        # Label
        pygame.display.set_caption("Pet Page")

    def draw_pet_page(self):
        self.screen.blit(self.pet_page_surface, (-1300,-1200))
        self.pet.display(self.screen, 600, 360)
        self.pet.animate()
        self.screen.blit(self.pet_rank, (0,0))
        self.store_button.draw(self.screen,self.font)
        self.chat_button.draw(self.screen, self.font)
        self.return_button.draw(self.screen, self.font)

        self.draw_health_bar()

    def draw_pet_store(self):
        self.screen.blit(self.pet_store,(0,0))
        self.return_button.draw(self.screen, self.font)

    def draw_health_bar(self):
        pygame.draw.rect(self.screen, 'brown', (270, 256, 250, 40), 20, 50)
        pygame.draw.rect(self.screen, 'green', (270, 256, 250*self.ratio, 40),20,50)
        self.screen.blit(self.wooden_loading_bar, (270, 250))
        # Render the goal name text
        goal_name = self.font.render(self.pet.goal_name, False, BLACK)
        ratio = str(self.pet.saved) + " / " + str(self.pet.target)
        progress = self.font.render(ratio, False, BLACK)

        # Calculate position to center the text
        text_rect = goal_name.get_rect(
            center=(270 + 125, 232))  # 125 is half of the health bar width, 20 is half the height
        text_rect2 = progress.get_rect(
            center=(270+125,320)
        )

        # Blit the goal name text at the calculated position
        self.screen.blit(goal_name, text_rect)
        self.screen.blit(progress, text_rect2)


if __name__ == '__main__':
    pygame.init()
    player = Player(9615)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    test = Pet_Page(player, 0, screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
#                 test.player.save_player_data()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if test.chat_button.is_clicked(mouse_pos):
                    print('Switching to Chatbot')

        test.draw_pet_page()
        pygame.display.update()

#         # Drawing the milestone map and streak information
#         test.draw_base()  # Draw base UI elements
#         test.draw_map()  # Draw the milestone rewards
#         pygame.display.update()