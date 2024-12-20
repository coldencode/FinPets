import pygame
import sys
import os
import google.generativeai as genai
from player import Player
from dotenv import load_dotenv

# Global variable declaration
scroll_offset = 0  # Initialize scroll_offset globally

def run_chatbot(player):
    global scroll_offset  # Declare it as global to modify it inside this function

    # Initialize Pygame
    pygame.init()

    # Load environment variables from the .env file
    load_dotenv()

    # Configure the API key for Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Create the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
    )

    # Start the chat session
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are Mellow, a virtual pet who is in the application FinPet. \
                    A virtual pet application that encourages saving and less spending. \
                    Your job is to capture your owner's (the user) name and constantly remind them to save, \
                    you are always angry because your owner has not been saving at all! Always say 'Meow' \
                    at the end of your sentence. Also, the money he saves is what keeps you satisfied, \
                    as you feed off their savings, so savings are like food for you. \
                    Make sure to prompt for their name after they say hi. \
                    Here is the data you are given for this person: \
                    Savings: " + str(player.wallet)

                ],
            }
        ]
    )

    # Define constants
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (220, 220, 220)
    FONT = pygame.font.SysFont('Arial', 20)
    TEXT_BOX_HEIGHT = 40
    MAX_LINE_WIDTH = SCREEN_WIDTH - 40  # Max width for text before wrapping

    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chatbot UI")

    # Create a text input box
    input_box = pygame.Rect(20, SCREEN_HEIGHT - TEXT_BOX_HEIGHT - 10, SCREEN_WIDTH - 40, TEXT_BOX_HEIGHT)
    input_text = ''
    active = False
    chat_history = []

    # Function to wrap text to fit within the text box
    def wrap_text(text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            # Check if adding the next word exceeds the max width
            test_line = current_line + ' ' + word if current_line else word
            width = FONT.size(test_line)[0]
            
            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        # Append the last line
        if current_line:
            lines.append(current_line)
        
        return lines

    # Function to simulate sending a message to the bot
    def get_bot_response(user_message):
        # Simulating the bot's response. You can link this to your bot's API.
        response = chat_session.send_message(user_message)
        return response.text

    # Function to draw chat history with scrolling
    def draw_chat():
        global scroll_offset  # Declare scroll_offset as global to modify it
        screen.fill(WHITE)
        
        # Calculate total height of the chat history
        total_height = 0
        lines = []
        for message in chat_history[-10:]:  # Display only the last 10 messages
            wrapped_lines = wrap_text(message, MAX_LINE_WIDTH)
            for line in wrapped_lines:
                total_height += FONT.get_height() + 5  # Account for each line's height
                lines.append(line)
        
        # Draw chat history with scroll offset
        y_offset = 20 - scroll_offset
        for line in lines:
            rendered_message = FONT.render(line, True, BLACK)
            screen.blit(rendered_message, (20, y_offset))
            y_offset += FONT.get_height() + 5  # Move to the next line

        # Draw the input box
        pygame.draw.rect(screen, GRAY, input_box)
        input_surface = FONT.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))  # Slight padding in the input box
        
        # Handle scrolling
        if total_height > SCREEN_HEIGHT - TEXT_BOX_HEIGHT:
            pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 10, 0, 10, total_height))
            scroll_offset = min(scroll_offset, total_height - SCREEN_HEIGHT + TEXT_BOX_HEIGHT)
            
        pygame.display.update()

    # Main event loop
    print("Mellow is ready to talk to you! Type 'exit' to end the conversation.")
    while True:
        draw_chat()  # Draw the chat window
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip():  # Only send if the input is not empty
                            chat_history.append(f"You: {input_text}")
                            bot_response = get_bot_response(input_text)
                            chat_history.append(f"Mellow: {bot_response}")
                        input_text = ''  # Clear the input box
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
        
        # Toggle input box active state
        active = input_box.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, BLACK, input_box, 2)  # Border for the input box

# To run the chatbot
if __name__ == "__main__":
    run_chatbot(Player(1111))
