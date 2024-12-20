import pygame
from sys import exit
from button import Button
from create_furniture import create_furniture
from player import Player
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, MAX_MILESTONES

class Milestone:
    def __init__(self, player: Player, screen: pygame.Surface):
        """
        Initialises the Milestone assets.
        """
        self.player = player
        self.milestone_rewards = [1, 2, 3, 4, 5, 6, 7]  # Fixed milestones
        self.screen = screen
        self.font = pygame.font.Font('assets/milestone/Pixeltype.ttf', 50)
        self.font_small = pygame.font.Font('assets/milestone/Pixeltype.ttf', 22)
        self.claimed_rewards = []  # Link to EXCEL or player data (should be persistent)
        pygame.display.set_caption("Milestone Map")
        self.prize_rewards = {
            1: "Stool",
            2: "Chair",
            3: "Stool",
            4: "Drawer",
            5: "Stool",
            6: "Chair",
            7: "Stool"
        } 

        # Load assets
        milestone_surface = pygame.image.load("assets/milestone/milestone_map_w_trails.png").convert_alpha()
        self.milestone_surface = pygame.transform.scale(milestone_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.closed_chest_image = pygame.image.load("assets/milestone/chest_close.png").convert_alpha()
        self.open_chest_image = pygame.image.load("assets/milestone/chest_open.png").convert_alpha()

    def draw_base(self):
        """ Draw the base UI including back button and streak counter. """
        back_to_home = Button(10, 10, 40, 40, "black", "<")
        self.screen.blit(self.milestone_surface, (0, 0))
        streak_surface = self.font.render(f"Streak: {self.player.streaks} days", False, "Black")
        self.screen.blit(streak_surface, (60, 20))  # Display streak
        back_to_home.draw(self.screen, self.font)

    def draw_map(self):
        """ Draw the reward chests on the milestone map. """
        prize_placements = {
            1: (38, 195),
            2: (140, 140),
            3: (125, 314),
            4: (295, 149),
            5: (435, 180),
            6: (585, 320),
            7: (740, 166)
        }

        for milestone in prize_placements.keys():
            prize_width, prize_height = prize_placements.get(milestone, (None, None))
            if self.player.milestones+1 >= MAX_MILESTONES+1:
                self.screen.blit(self.open_chest_image, (prize_width, prize_height))
            elif int(milestone) < self.player.milestones+1:
                if prize_width is not None and prize_height is not None:
                    self.screen.blit(self.open_chest_image, (prize_width, prize_height))
            else:
                if prize_width is not None and prize_height is not None:
                    self.screen.blit(self.closed_chest_image, (prize_width, prize_height))
                    milestone_text = self.font_small.render(f"Claim reward at {milestone} days!", False, "white")
                    self.screen.blit(milestone_text, (prize_width - 45, prize_height - 30))

    def claim_rewards(self):
        """ Claim rewards for milestones met, and update the player's inventory. """
        if self.player.milestones+1 > MAX_MILESTONES:
            print("You have claimed all prizes already!")
        elif self.prize_rewards[self.player.milestones+1] and self.player.milestones+1 <= self.player.streaks:
            furniture = create_furniture(self.prize_rewards[self.player.milestones+1])
            # Override
            self.player.update_inventory(furniture)
            print(f"Reward claimed for {self.player.milestones+1} days: {self.prize_rewards[self.player.milestones+1]}!")
            self.prize_rewards[self.player.milestones+1] = None
            self.player.milestones += 1
            
        else:
            self.debug()
            print("prize are claimed already")

    def increment_streaks(self):
        self.player.streaks += 1


    def update_claimed_rewards(self, new_claims):
        """ Update the list of claimed rewards from player data or a file. """
        # Ideally, this would save/load from player data (Excel, JSON, or a database)
        self.claimed_rewards.extend(new_claims)

    def debug(self):
        print(f"Streaks~{self.player.streaks}~{type({self.player.streaks})}")
        print(f"Milestones~{self.player.milestones}~{type({self.player.milestones})}")

# if __name__ == '__main__':
#     pygame.init()
#     player = Player(5031)
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     font = pygame.font.Font('assets/milestone/Pixeltype.ttf', 50)

#     test = Milestone(player, screen)
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 test.player.save_player_data()
#                 exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:  # Press SPACE to simulate a day
#                     test.increment_streaks()
#                     test.debug()
#                 if event.key == pygame.K_c:  # Press C to claim reward(s)
#                     test.claim_rewards()
#                     test.debug()

#         # Drawing the milestone map and streak information
#         test.draw_base()  # Draw base UI elements
#         test.draw_map()  # Draw the milestone rewards
#         pygame.display.update()

