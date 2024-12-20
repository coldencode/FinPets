import pygame
import sys
from constants import *
from furnitureloader import load_furniture_from_excel
from button import Button, WoodenButton, StreakButton
from store import Store
from player import Player
from milestone import Milestone
from chatbot import run_chatbot
from furnituregrid import FurnitureGrid
from pet_page import Pet_Page

class Game:
    def __init__(self, player: Player = None):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()  # Explicitly initialize the font module
        
        # Setup screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("FinSpace")
        
        # Fonts
        self.font = pygame.font.Font(None, 30)
        
        # Initialize grid and inventory
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        #self.inventory = load_furniture_from_excel()
        self.selected_item = None
        self.selected_tile = None  # Track selected tile on the grid
        self.highlighted_tile = None
        self.mode = 'view'  # view or build mode

        self.player = player

        # Making Pet Pages
        self.pet_index = None
        self.pet_pages = []
        for i in range(len(self.player.pets)):
            petpage = Pet_Page(self.player, i, self.screen)
            self.pet_pages.append(petpage)
            
        #self.pet_page = Pet_Page(player, 1, screen)
        self.furniture_grid = FurnitureGrid(self.player.id) # Furniture grid
        self.inventory = self.player.get_inventory()
        

        # Store-related
        self.store = Store(self.player)
        self.wallet = CURRENCY

        # Milestone
        self.check_point = Milestone(self.player, self.screen)
        
        # Load background image and scale it down by 2x
        self.background_image = pygame.image.load('background_trees.png')  # Replace with the path to your background image
        bg_width, bg_height = self.background_image.get_size()
        scaled_bg_width = bg_width // 2
        scaled_bg_height = bg_height // 2
        self.background_image = pygame.transform.scale(self.background_image, (scaled_bg_width, scaled_bg_height))
        
        # Calculate the position to offset the background into the window (center it)
        self.bg_x = (SCREEN_WIDTH - scaled_bg_width) // 2
        self.bg_y = (SCREEN_HEIGHT - scaled_bg_height) // 2
        
        # Calculate grid position to center it
        self.GRID_X = (SCREEN_WIDTH - (GRID_SIZE * TILE_SIZE)) // 2
        self.GRID_Y = (SCREEN_HEIGHT - (GRID_SIZE * TILE_SIZE)) // 2
        
        # Button instances
        self.view_button = WoodenButton(20, 20, 70, 40, 'View')
        self.build_button = WoodenButton(20, 70, 70, 40,'Build')
        self.store_button = WoodenButton(20, 120, 70, 40, 'Store')
        self.exit_button = WoodenButton(20, 170, 70, 40, 'Exit')
        self.place_button = WoodenButton(20, 220, 70, 40,'Place')
        self.remove_button = WoodenButton(20, 270, 70, 40, 'Pick')
        self.check_point_button = StreakButton(850,20,68, 40)
        self.interact_button = WoodenButton(20,320,70,40,'Pat')

    def check_furniture(self, furniture, x, y, value):
        if furniture.height > 0 or furniture.width > 0:
            for i in range(furniture.height):  # Loop through the height
                for j in range(furniture.width):  # Loop through the width
                    self.furniture_grid[(x + j),(y - i)] = value

    def draw_grid(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                # Draw grid slots
                pygame.draw.rect(self.screen, (255, 255, 255), (self.GRID_X + x * TILE_SIZE, self.GRID_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def draw_inventory(self):
        for i, item in enumerate(self.inventory):
            inv_rect = pygame.Rect(SCREEN_WIDTH - 150, 20 + i * (TILE_SIZE + 5), TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 255), inv_rect, 2)  # Draw the slot border

            if item:
                self.screen.blit(item.preview, inv_rect.topleft)  # Blit the furniture image to the inventory slot
            else:
                empty_text = self.font.render(" ", True, (0, 0, 0))
                self.screen.blit(empty_text, (inv_rect.x + 5, inv_rect.y + 5))

    # Function to draw the highlighted tile
    def draw_highlight(self):
        if self.highlighted_tile:
            x, y = self.highlighted_tile
            highlight_rect = pygame.Rect(self.GRID_X + x * TILE_SIZE, self.GRID_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(self.screen, GREEN, highlight_rect, 3)  # Draw a green border around the highlighted tile
        
    def draw_currency(self):
        """Draw the currency using an image and text at the top-left corner."""
        # Load the currency image (e.g., a coin or wallet icon)
        currency_image = pygame.image.load('assets/main_menu/currency.png')  # Replace with your image path

        # Define the position for the image
        box_x = 620
        box_y = 8

        # Blit the currency image to the screen
        self.screen.blit(currency_image, (box_x, box_y))  # Position the image next to the text

        # Render the currency text
        currency_text = self.font.render(f"${self.player.wallet}", True, WHITE)

        # Position the currency text next to the image
        text_x = box_x + (currency_image.get_width() - currency_text.get_width() )// 2 + 15  # Offset the text next to the image
        text_y = box_y + (currency_image.get_height() - currency_text.get_height()) // 2  # Center the text vertically

        # Draw the currency text
        self.screen.blit(currency_text, (text_x, text_y))

    # Function to draw furniture on the grid
    def draw_furniture(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                furniture = self.furniture_grid[(x,y)]
                if furniture == PLACEHOLDER:
                    continue
                elif furniture:
                    # Get the correct top position for the furniture (aligned at the bottom of the tile)
                    furniture_height = furniture.image.get_height()
                    furniture_top = (y + 1) * TILE_SIZE - furniture_height  # Align the bottom of the furniture with the tile

                    # Calculate the position based on the grid offset
                    furniture_rect = pygame.Rect(
                        self.GRID_X + x * TILE_SIZE,  # Offset the x position by the grid's center position
                        self.GRID_Y + furniture_top,  # Offset the y position by the grid's center position
                        TILE_SIZE,
                        furniture_height
                    )

                    # Draw the furniture (image) in the calculated position
                    self.screen.blit(furniture.image, furniture_rect.topleft)

    def remove_furniture_from_grid(self, x, y):
        """Removes furniture from the grid and adds it to the inventory."""
        furniture = self.furniture_grid[(x,y)]
        if furniture and furniture != PLACEHOLDER:
            # Add the item back to the inventory
            self.player.update_inventory(furniture)
            # Clear the grid position where the furniture was
            self.furniture_grid[(x,y)] = None

    def run(self):
        # Main game loop
        running = True
        while running:
            self.screen.fill((200, 200, 200))  # Background color

            # Draw the background map
            self.screen.blit(self.background_image, (self.bg_x, self.bg_y))  # Offset the background to the center of the window

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player.save_player_data()
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:  # Press SPACE to simulate a day
                        self.mode = 'view'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.mode == 'pet_page' and self.pet_pages[self.pet_index].chat_button.is_clicked(mouse_pos):
                        run_chatbot(self.player)
                    if self.mode == 'pet_page' and self.pet_pages[self.pet_index].store_button.is_clicked(mouse_pos):
                        self.mode = 'pet_store'
                    if self.mode in ['pet_page','pet_store'] and self.pet_pages[self.pet_index].return_button.is_clicked(mouse_pos):
                        self.mode = 'view'

                    # Button interactions
                    if self.view_button.is_clicked(mouse_pos):
                        print("Switched to View Mode")  # Debugging output
                        self.mode = 'view'
                    elif self.build_button.is_clicked(mouse_pos):
                        print("Switched to Build Mode")  # Debugging output
                        self.mode = 'build'
                    elif self.store_button.is_clicked(mouse_pos):
                        self.mode = 'store'
                    if self.mode == 'store':
                        self.store.handle_popup_click()
                    if self.check_point_button.is_clicked(mouse_pos):
                        print('Switched to Milestone')
                        self.mode = 'check_point'
                    if self.mode == 'check_point':
                        self.check_point.draw_base()
                        self.check_point.draw_map()

                    

                    # Handle grid tile selection in Build Mode
                    if self.mode == 'build':
                        x, y = (mouse_pos[0] - self.GRID_X) // TILE_SIZE, (mouse_pos[1] - self.GRID_Y) // TILE_SIZE
                        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                            self.selected_tile = (x, y)  # Set the selected tile
                            # If the same tile is clicked again, deselect it
                            if self.highlighted_tile == (x, y):
                                self.selected_tile = None
                                self.highlighted_tile = None
                            else:
                                self.highlighted_tile = (x, y)  # Highlight the new tile

                    if self.mode == 'build' and self.interact_button.is_clicked(mouse_pos):
                        if self.selected_tile:
                            x, y = self.selected_tile
                            furniture = self.furniture_grid[(x,y)]
                            if furniture and furniture.name == "White_Cat":
                                self.pet_index = 0
                                self.mode = "pet_page"
                            elif furniture and furniture.name == "Orange_Cat":
                                self.pet_index = 1
                                self.mode = "pet_page"

                    # Handle Place Button in Build Mode
                    if self.mode == 'build' and self.place_button.is_clicked(mouse_pos):
                        if self.selected_tile is None:
                            print("Tile is not selected!")
                            break
                        x, y = self.selected_tile
                        if self.selected_item and self.selected_item.validate_placement(x, y, self.furniture_grid):
                            if self.furniture_grid[(x,y)] is None:  # Place furniture only if the slot is empty
                                print(f"Placing item: {self.selected_item}")  # Debugging output
                                # Place the selected Furniture object in the grid
                                self.check_furniture(self.selected_item, x, y, PLACEHOLDER)
                                self.furniture_grid[(x,y)] = self.selected_item
                                for row in self.furniture_grid:
                                    print(row)
                                # Remove the item from the inventory
                                self.player.remove_item_from_inventory(self.selected_item)
                                # Reset selected tile
                                self.selected_item = None
                            else:
                                print(f"Failed to place item: {self.selected_item} because {self.selected_tile}")  # Debugging output
                        else:
                            print(f"Item is being blocked by items nearby or selected item is None")

                    # Handle Remove Button in Build Mode
                    if self.mode == 'build' and self.remove_button.is_clicked(mouse_pos):
                        print(f"Removing item at {self.selected_tile}")  # Debugging output
                        if self.selected_tile:
                            x, y = self.selected_tile

                            temp_furniture = self.furniture_grid[(x,y)]
                            if temp_furniture and temp_furniture != 'X':
                                self.remove_furniture_from_grid(x, y)  # Remove from grid and add back to inventory
                                self.check_furniture(temp_furniture, x, y, None)
                                self.selected_item = None  # Reset selected item after removal


                    # Handle inventory item selection in Build Mode
                    if self.mode == 'build':
                        for i in range(INVENTORY_SIZE):
                            inv_rect = pygame.Rect(SCREEN_WIDTH - 150, 20 + i * (TILE_SIZE + 5), TILE_SIZE, TILE_SIZE)
                            if inv_rect.collidepoint(mouse_pos) and self.inventory[i]:
                                self.selected_item = self.inventory[i]  # Select the item from inventory
                                print(f"Selected item: {self.selected_item}")  # Debugging output

                    if self.mode == 'store' and self.exit_button.is_clicked(mouse_pos):
                        self.mode = 'view'
                        print('Exited Store')

                    # Exit button
                    if self.mode == 'build' and self.exit_button.is_clicked(mouse_pos):
                        self.mode = 'view'  # Return to View Mode
                        print("Exited Build Mode")  # Debugging output
                elif event.type == pygame.KEYDOWN and self.mode == 'check_point':
                    if event.key == pygame.K_SPACE:  # Press SPACE to simulate a day
                        self.player.streaks += 1
                    if event.key == pygame.K_c:  # Press C to claim reward(s)
                        self.check_point.claim_rewards()
            
            self.draw_furniture()

            # Draw buttons
            if self.mode == 'pet_page':
                self.pet_pages[self.pet_index].draw_pet_page()
            if self.mode == 'pet_store':
                self.pet_pages[self.pet_index].draw_pet_store()
                

            if self.mode == 'build': 
            # Draw grid and furniture
                self.interact_button.draw(self.screen, self.font)
                self.remove_button.draw(self.screen, self.font)
                self.place_button.draw(self.screen, self.font)
                self.exit_button.draw(self.screen, self.font)

                self.draw_grid()
                self.draw_inventory()
                self.draw_furniture()
                self.draw_highlight()  # Draw the highlighted tile if there is one

            if self.mode == 'store':
                self.exit_button.draw(self.screen, self.font)
                self.store.draw_popup(self.screen, self.font)
                self.draw_inventory()

            
            if self.mode not in ['check_point','pet_page', 'pet_store']:
                self.store_button.draw(self.screen, self.font)
                self.build_button.draw(self.screen, self.font)
                self.view_button.draw(self.screen, self.font)
                self.check_point_button.draw(self.screen, self.font)

            if self.mode == 'check_point':
                self.check_point.draw_base()
                self.check_point.draw_map()

            if self.mode not in ['build', 'pet_page', 'pet_store']:
                self.draw_currency()

            # Update the display
            pygame.display.update()
        

        self.furniture_grid.save_to_excel((FURNITURE_GRID_DIRECTORY + str(self.player.id) + ".xlsx"))
        pygame.quit()

# Initialize the game and run it
if __name__ == "__main__":
    game = Game(Player(1111))
    game.run()
    print("Done!")
