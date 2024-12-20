import pygame
from button import Button  # Import the Button class
from constants import *
from furnitureloader import Furniture
from player import Player
import pandas as pd

class Store:
    def __init__(self, player: Player):
        self.items = self.load_store_from_excel()  # Store dictionary with furniture objects
        self.selected_item = None
        self.popup_open = False
        self.buttons = []  # List to hold Button objects
        self.player = player
        self.title = 'Store'

    def load_store_from_excel(self):
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel("data/store.xlsx")
        
        # Dictionary to hold Furniture objects
        store_dict = {}
        
        # Loop through each row and create a Furniture object
        for index, row in df.iterrows():
            furniture_name = row['furniture_name']
            image_path = row['image_path']
            offset_y = row['offset_y']
            offset_x = row['offset_x']
            price = row['price']
            
            # Load the image and scale it to fit the tile size
            image = pygame.image.load(image_path)
            preview = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            
            # Create a Furniture object and add it to the dictionary
            furniture_obj = Furniture(furniture_name, image, preview, offset_y, offset_x, price)
            store_dict[furniture_name] = furniture_obj
            
        return store_dict
    
    def draw_title(self, screen, font):
        # Render the title text
        title_surface = font.render(self.title, True, BLACK)
        title_rect = title_surface.get_rect(center=(400, 60))  # Center the title at the top of the popup
        screen.blit(title_surface, title_rect)  # Draw the title text


    def draw_popup(self, screen, font):
        # Draw the popup background
        popup_rect = pygame.Rect(150, 33, 500, 350)
        pygame.draw.rect(screen, WHITE, popup_rect)

        #title
        self.draw_title(screen, font)
        
        # Create buttons for each furniture item and draw them
        button_y = 80
        button_x = 170

        # counter so that the other buttons will go to the side
        count = 0

        self.buttons.clear()  # Clear existing buttons each time the popup is redrawn
        for name, furniture in self.items.items():

            if count < 5 and count != 0:
                # Create a new Button for each furniture item
                button_y += 10

            elif count == 5:
                button_y = 80
                button_x = 420

            elif count > 5:
                button_y += 10


            button = Button(button_x, button_y, 210, 40, BLACK, f"{furniture.name} - ${furniture.price}")

            self.buttons.append((button, furniture))
            
            # Draw the button
            button.draw(screen, font)


            button_y += 50  # Update Y position for the next button
            count += 1
        
    def handle_popup_click(self):
        # Handle button clicks
        print('pass inside popup')
        mouse_pos = pygame.mouse.get_pos()
        for button, furniture in self.buttons:
            if button.is_clicked(mouse_pos):  # Check if a button is clicked
                print('button is clicked pass')
                self.selected_item = furniture
                print(f"Selected item: {furniture.name}")

                # Add item to inventory if the player can afford it
                if self.player.can_afford(furniture.price):
                    self.player.update_inventory(furniture)
                    self.player.update_wallet(-furniture.price)
                    print(f"Added {furniture.name} to inventory. New Wallet: {self.player.wallet}")
                else:
                    print("Insufficient funds to purchase this item.")

    def toggle_popup(self):
        self.popup_open = not self.popup_open


if __name__ == '__main__':
    player = Player(3147)
    temp_list = Store(player)
    list = temp_list.load_store_from_excel()
    print(list['Chair'].price)
