import pygame
import random
import time

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Map color names to RGB values
color_map = {
    "RED": RED,
    "GREEN": GREEN,
    "BLUE": BLUE,
    "YELLOW": YELLOW
}

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Stroop Task')

# Set up fonts
font = pygame.font.SysFont('Arial', 80)
small_font = pygame.font.SysFont('Arial', 40)

# Define words and possible colors for the task
words = ["RED", "GREEN", "BLUE", "YELLOW"]
colors = [RED, GREEN, BLUE, YELLOW]

# Stroop task variables
num_trials = 10
reaction_times = []
correct_responses = 0
trial_data = []

# Instructions screen
def show_instructions():
    screen.fill(WHITE)
    instructions = [
        "Stroop Task Instructions:",
        "1. If the word matches the ink color, press 'Y'.",
        "2. If the word does NOT match the ink color, press 'N'.",
        "Press any key to begin."
    ]
    for i, line in enumerate(instructions):
        instruction_text = small_font.render(line, True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 100 + i * 50))
    
    pygame.display.flip()
    
    # Wait for the user to press a key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False

# Stroop trial function
def stroop_trial(word, color):
    global correct_responses
    
    # Show the word on the screen in the specified color
    screen.fill(WHITE)
    text = font.render(word, True, color)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()

    # Record the start time
    start_time = time.time()

    # Wait for the user to press Y or N
    response = None
    while response is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    response = "Y"
                elif event.key == pygame.K_n:
                    response = "N"

    # Calculate reaction time
    reaction_time = time.time() - start_time
    reaction_times.append(reaction_time)

    # Determine if the response is correct
    is_congruent = (word.upper() == list(color_map.keys())[list(color_map.values()).index(color)])
    correct_response = "Y" if is_congruent else "N"
    is_correct = (response == correct_response)

    if is_correct:
        correct_responses += 1

    # Store the trial data
    trial_data.append({
        "word": word,
        "color": color,
        "response": response,
        "reaction_time": reaction_time,
        "correct": is_correct
    })

    # Pause briefly between trials
    pygame.time.wait(500)

# Display results at the end
def show_results():
    screen.fill(WHITE)
    
    accuracy = correct_responses / num_trials * 100
    avg_reaction_time = sum(reaction_times) / len(reaction_times)

    results = [
        f"Results:",
        f"Accuracy: {accuracy:.2f}%",
        f"Average Reaction Time: {avg_reaction_time:.2f} seconds",
    ]
    for i, line in enumerate(results):
        result_text = small_font.render(line, True, BLACK)
        screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, 150 + i * 50))
    
    pygame.display.flip()

    # Wait for the user to close the window
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

# Main loop
def main():
    show_instructions()

    for trial in range(num_trials):
        word = random.choice(words)
        color = random.choice(colors)
        stroop_trial(word, color)

    show_results()

    pygame.quit()

if __name__ == "__main__":
    main()
