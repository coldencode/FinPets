import pygame
from constants import *
import pandas as pd
from PIL import Image

class Pet:
    def __init__(self, pet, goal, saved, goal_name, days):
        self.pet_type = pet
        self.saved = saved
        self.target = goal
        self.goal_name = goal_name
        self.days = days

        self.directory = PETS_DIRECTORY + self.pet_type + "/"
        self.mood = self.update_mood()    # Initialize mood and set the pet's image based on the player's wallet & savings
        self.frames = self.load_gif(self.mood)  # Load the GIF frames based on the pet's mood
        self.current_frame = 0  # Start with the first frame
        self.frame_time = 150  # Delay between frames (milliseconds)
        self.last_update = pygame.time.get_ticks()  # Store the time of the last frame update

    def load_gif(self, mood, size = (256,256)):
        """
        Loads a GIF file and returns a list of frames.
        """
        gif_path = self.directory + str(mood) + ".gif"
        gif = Image.open(gif_path)  # Open GIF using Pillow
        frames = []

        # Loop through each frame of the GIF and convert to Pygame-compatible surfaces
        for frame in range(gif.n_frames):
            gif.seek(frame)  # Seek to the current frame
            frame_image = gif.convert("RGBA")  # Convert to RGBA for transparency support
            frame_surface = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, 'RGBA')

            # # Resize the pet
            frame_surface = pygame.transform.smoothscale(frame_surface, size)

            frames.append(frame_surface)

        return frames

    def update_mood(self):
        """
        Update the pet's mood based on the player's savings (wallet).
        """
        if self.saved <= self.target * (SAVINGS_RATE):  # If player has very low funds
            ret = "dead"
        elif self.saved <= self.target * (SAVINGS_RATE * 2):  # Low funds, but not too bad
            ret = "sad"
        elif self.saved <= self.target * (SAVINGS_RATE * 3):  # Average savings
            ret = "happy"
        else:  # High funds, pet is very happy
            ret = "super_happy"
        return ret

    def display(self, screen, x,y):
        """
        Display the pet's current frame at the bottom right of the screen.
        """
        screen_width, screen_height = screen.get_size()
        
        # Calculate where to display the pet (bottom right corner)
        pet_x = screen_width - x
        pet_y = screen_height - y
        
        # Display the current frame
        screen.blit(self.frames[self.current_frame], (pet_x, pet_y))

    def update_pet(self):
        """
        Check and update the pet's mood whenever the player's wallet changes.
        """
        new_mood = self.update_mood()

        # If the mood has changed, reload the GIF frames
        if new_mood != self.mood:
            self.mood = new_mood
            self.frames = self.load_gif(self.mood)
            self.current_frame = 0  # Reset to the first frame

    def animate(self):
        """
        Update the pet's frame to animate the GIF.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_time:  # Check if it's time to update the frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # Cycle through frames
            self.last_update = now  # Reset the last update time

# All students have the same info

if __name__ == '__main__':
    print('Pet Class Initialized!')
    testpet = Pet("white_cat", 7000, 100, "Macbook Pro", 3)
    # Test example (you'd use this in your main game loop, not directly like this)
