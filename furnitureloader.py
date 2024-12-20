import pandas as pd
import pygame
from PIL import Image
from constants import *

# Furniture class to store furniture objects
class Furniture:
    def __init__(self, name, image, preview, offset_y=0, offset_x=0, price=0):
        self.name = name
        self.image = image  # Store the furniture's image as a Pygame surface
        self.preview = preview # For the inventory preview scaled into the slot
        
        self.price = price


        self.height = self.image.get_height() // TILE_SIZE - offset_y
        self.width = self.image.get_width() // TILE_SIZE - offset_x
        
    def validate_placement(self, x, y, furniture_grid):
        border_y = y - self.height + 1
        border_x = x + self.width
        if border_y < 0 or border_x > 10:
            print(f"Border! y:{border_y} x:{border_x}")
            return False
        if self.height == 1 and self.width == 1:
            return True
        if self.height > 1:
            for i in range(self.height-1):
                i += 1
                if furniture_grid[(x,y-i)] is not None:
                    return False
        if self.width > 1:
            for i in range(self.height-1):
                i += 1
                if furniture_grid[(x+i,y)] is not None:
                    return False
        return True

    def __repr__(self):
        """Return a string representation of the Furniture object for debugging."""
        return f"{self.name}"

    def __str__(self):
        """Return a user-friendly string representation of the Furniture object."""
        return f"Furniture: {self.name}"


def load_furniture_from_excel():
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel("data/furniture.xlsx")
    print(df)
    
    # List to hold Furniture objects
    furniture_list = []
    
    # Loop through each row and create a Furniture object
    for index, row in df.iterrows():
        furniture_name = row['furniture_name']
        image_path = row['image_path']
        offset_y = row['offset_y'] # If the furniture is calculated is 2 pixels, but is technically 1, (e.g. chair)
        offset_x = row['offset_x']
        
        # Load the image and scale it to fit the tile size
        image = pygame.image.load(image_path)
        preview = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        
        # Create a Furniture object and add it to the list
        furniture_list.append(Furniture(furniture_name, image, preview, offset_y, offset_x))
    
    return furniture_list
    
class FurnitureWithAnimation(Furniture):
    def __init__(self, name, gif_path, preview, offset_y=0, offset_x=0, price=0, frame_time=100):
        super().__init__(name, None, preview, offset_y, offset_x, price)  # Call the parent class constructor
        
        self.directory = gif_path
        self.frame_time = frame_time  # Delay between frames (in milliseconds)
        self.frames = self.load_gif()  # Load the frames of the GIF
        self.current_frame = 0  # Start with the first frame
        self.last_update = pygame.time.get_ticks()  # Store the time of the last frame update

    def load_gif(self):
        """
        Loads a GIF file and returns a list of frames.
        """
        gif = Image.open(self.directory)  # Open GIF using Pillow
        frames = []

        # Loop through each frame of the GIF and convert to Pygame-compatible surfaces
        for frame in range(gif.n_frames):
            gif.seek(frame)  # Seek to the current frame
            frame_image = gif.convert("RGBA")  # Convert to RGBA for transparency support
            frame_surface = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, 'RGBA')
            frames.append(frame_surface)

        return frames

    def update(self):
        """
        Update the current frame of the animation.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_time:  # Check if it's time to update the frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # Cycle through frames
            self.last_update = now  # Reset the last update time

    def display(self, screen, x, y):
        """
        Display the current frame of the animated furniture.
        """
        # Update the animation
        self.update()

        # Display the current frame at the given (x, y) position
        screen.blit(self.frames[self.current_frame], (x, y))

    def __repr__(self):
        """Return a string representation of the animated furniture."""
        return f"FurnitureWithAnimation(name='{self.name}')"

    def __str__(self):
        """Return a user-friendly string representation of the animated furniture."""
        return f"Animated Furniture: {self.name}"


if __name__ == '__main__':
    temp_list = load_furniture_from_excel()
    print(temp_list[23].width)