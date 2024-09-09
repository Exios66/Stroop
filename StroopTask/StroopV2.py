import pygame
import random
import time
import numpy as np

# Initialize pygame
pygame.init()

# Define colors for light and dark modes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define color names to RGB values
color_map = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "PURPLE": (128, 0, 128),
    "ORANGE": (255, 165, 0),
    "PINK": (255, 192, 203),
    "CYAN": (0, 255, 255),
}

# List of words (colors) and their corresponding RGB values
words = list(color_map.keys())
colors = list(color_map.values())

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Stroop Task')

# Set up fonts
font = pygame.font.SysFont('Arial', 80)
small_font = pygame.font.SysFont('Arial', 40)

# Stroop task variables
num_trials = 20  # Increased number of trials for better analysis
reaction_times = []
correct_responses = 0
trial_data = []

# Mode (dark or light)
current_mode = "light"

# Toggle between dark and light mode
def toggle_mode():
    global current_mode
    if current_mode == "light":
        current_mode = "dark"
    else:
        current_mode = "light"

# Instructions screen
def show_instructions():
    background_color = WHITE if current_mode == "light" else BLACK
    text_color = BLACK if current_mode == "light" else WHITE
    screen.fill(background_color)

    instructions = [
        "Stroop Task Instructions:",
        "1. If the word matches the ink color, press 'Y'.",
        "2. If the word does NOT match the ink color, press 'N'.",
        "3. Press 'T' to toggle dark/light mode.",
        "Press any key to begin."
    ]
    for i, line in enumerate(instructions):
        instruction_text = small_font.render(line, True, text_color)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 100 + i * 50))
    
    pygame.display.flip()

    # Wait for the user to press a key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    toggle_mode()
                    show_instructions()  # Re-show instructions with new mode
                else:
                    waiting = False

# Stroop trial function
def stroop_trial(word, color):
    global correct_responses

    # Determine background and text color based on mode
    background_color = WHITE if current_mode == "light" else BLACK
    text_color = BLACK if current_mode == "light" else WHITE

    # Show the word on the screen in the specified color
    screen.fill(background_color)
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
                elif event.key == pygame.K_t:
                    toggle_mode()
                    stroop_trial(word, color)  # Re-run the trial in the new mode

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

# Enhanced analysis of reaction times
def analyze_reaction_times():
    all_reactions = np.array(reaction_times)
    correct_reactions = np.array([t['reaction_time'] for t in trial_data if t['correct']])
    incorrect_reactions = np.array([t['reaction_time'] for t in trial_data if not t['correct']])

    analysis = {
        "average": np.mean(all_reactions),
        "median": np.median(all_reactions),
        "fastest": np.min(all_reactions),
        "slowest": np.max(all_reactions),
        "correct_avg": np.mean(correct_reactions) if len(correct_reactions) > 0 else None,
        "incorrect_avg": np.mean(incorrect_reactions) if len(incorrect_reactions) > 0 else None
    }
    return analysis

# Display results at the end
def show_results():
    background_color = WHITE if current_mode == "light" else BLACK
    text_color = BLACK if current_mode == "light" else WHITE
    screen.fill(background_color)
    
    accuracy = correct_responses / num_trials * 100
    reaction_analysis = analyze_reaction_times()

    results = [
        f"Results:",
        f"Accuracy: {accuracy:.2f}%",
        f"Average Reaction Time: {reaction_analysis['average']:.2f} seconds",
        f"Median Reaction Time: {reaction_analysis['median']:.2f} seconds",
        f"Fastest Response: {reaction_analysis['fastest']:.2f} seconds",
        f"Slowest Response: {reaction_analysis['slowest']:.2f} seconds",
        f"Correct Responses Avg Time: {reaction_analysis['correct_avg']:.2f} seconds" if reaction_analysis['correct_avg'] else "N/A",
        f"Incorrect Responses Avg Time: {reaction_analysis['incorrect_avg']:.2f} seconds" if reaction_analysis['incorrect_avg'] else "N/A"
    ]
    for i, line in enumerate(results):
        result_text = small_font.render(line, True, text_color)
        screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, 100 + i * 50))
    
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
