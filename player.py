import pandas as pd
import random
import pygame
from pet import Pet
from constants import *
from furnitureloader import Furniture
from petloader import load_pet_info
import os

# Function to generate a new unique player ID
def generate_new_id():
    return random.randint(1000, 9999)

class Player:
    def __init__(self, id=None):
        # Initializing variables (when player is New)
        self.id = id if id else generate_new_id()  # Assign the ID or generate a new one
        self.wallet = 1000  # Starting money (default)
        self.excel_inv = ['Chair'] # Start with a Chair
        self.savings = 0
        self.pet_type = "white_cat"
        self.pets = load_pet_info()
        self.streaks = 0
        self.milestones = 1

        

        # Check if player exists in the Excel file
        self.check_info(self.id)
        self.inventory = self.convert_excel_inventory()


    def check_info(self, player_id):
        # Check if the ids.xlsx file exists
        df = pd.read_excel(PLAYERS_DIRECTORY)

        # Check if player ID exists in the DataFrame
        player_exists = df[df['PlayerID'] == player_id]

        if not player_exists.empty:
            # Player exists, load their wallet and inventory
            player_index = df[df['PlayerID'] == player_id].index[0]
            self.wallet = df.at[player_index, 'Wallet']
            self.excel_inv = (
                df.at[player_index, 'Inventory'].split(", ")
                if isinstance(df.at[player_index, 'Inventory'], str) and df.at[player_index, 'Inventory']
                else []
            )
            self.savings = df.at[player_index, 'Savings']
            self.streaks = int(df.at[player_index, 'Streaks'])
            self.milestones = int(df.at[player_index, 'Milestones']) # Milestone = Streaks claimed

            print(f"Loaded player {player_id}: Wallet = {self.wallet}, Inventory = {self.excel_inv}")
        else:
            # Player does not exist, create a new row in the DataFrame
            self.create_new_player(player_id, df)

    def create_new_player(self, player_id, df):
        # If player doesn't exist, create a new row with initial values
        new_row = pd.DataFrame([{
            "PlayerID": player_id, 
            "Wallet": self.wallet, 
            "Inventory": 'Chair',  # Empty inventory at the beginning
            "Savings": self.savings,
            "Pet" : self.pet_type, # Default Pet
            "Streaks" : self.streaks,
            "Milestones" : self.milestones

        }])

        # Use pd.concat() to append the new row to the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

        # Save the updated DataFrame back to the Excel file
        df.to_excel(PLAYERS_DIRECTORY, index=False)
        print(f"Created new player {player_id}: Wallet = {self.wallet}, Inventory ={self.excel_inv}")

    def update_wallet(self, amount):
        # Update the player's wallet and save to the Excel file
        self.wallet += amount
        self.save_player_data()

    def update_inventory(self, item):
        # Add the item to the player's inventory and save to the Excel file
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                self.inventory[i] = item
                break
        self.excel_inv.append(item.name)
        self.save_player_data()
    
    def remove_item_from_inventory(self, item):
        for i in range(len(self.inventory)):
            if self.inventory[i] == item:
                self.inventory[i] = None
                break
        self.excel_inv.remove(item.name)
        self.save_player_data()


    def save_player_data(self):
        # Load the existing data
        df = pd.read_excel(PLAYERS_DIRECTORY)
        player_index = df[df['PlayerID'] == self.id].index[0]

        # Update wallet and inventory in the DataFrame
        df.at[player_index, 'Wallet'] = self.wallet
        df.at[player_index, 'Inventory'] = ", ".join(self.excel_inv)
        df.at[player_index, 'Savings'] = self.savings
        df.at[player_index, 'Pet'] = self.pet_type
        df.at[player_index, 'Streaks'] = self.streaks
        df.at[player_index, 'Milestones'] = self.milestones

        # Save the updated data back to the Excel file
        df.to_excel(PLAYERS_DIRECTORY, index=False)

    def can_afford(self, price):
        # Check if player can afford the item
        return self.wallet >= price
    
    def get_inventory(self):
        return self.inventory
    
    def convert_excel_inventory(self):
        """
        Converts list into readable dictionary
        """
        # Reference the list of furnitures
        furniture_data = pd.read_excel("data/furniture.xlsx")

        # Create a dictionary to hold the inventory details
        inventory_list = [None] * INVENTORY_SIZE
    
        for item in self.excel_inv:
            print(item)
            # Find the corresponding row in the furniture data
            furniture_row = furniture_data[furniture_data['furniture_name'] == item]
            
            if not furniture_row.empty:
                # Extract the item details
                furniture_name = furniture_row.iloc[0]['furniture_name']
                image_path = furniture_row.iloc[0]['image_path']
                offset_y = furniture_row.iloc[0]['offset_y']
                offset_x = furniture_row.iloc[0]['offset_x']
                
                # Create a Furniture object
                furniture_obj = Furniture(furniture_name, 
                                        pygame.image.load(image_path),  # Load the image
                                        pygame.transform.scale(pygame.image.load(image_path), (TILE_SIZE, TILE_SIZE)), 
                                        offset_y, offset_x)

                # Add the Furniture object to the dictionary
                for i in range(INVENTORY_SIZE):
                    if inventory_list[i] is None:
                        inventory_list[i] = furniture_obj
                        break
                #print(inventory_list)
            else:
                print(f"Item {item} not found in furniture data.")
    
        return inventory_list



if __name__ == '__main__':
    # Test example

    player = Player(3147)  # Create a new player or load an existing one based on the ID
    print(player.excel_inv)
    print(player.pet.mood)
    print(player.pet.player_savings)
    print(player.pet.player_savings <= player.pet.player_wallet*(SAVINGS_RATE))

    print(f"Streaks: {player.streaks}")


