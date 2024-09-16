import pygame
import random
import time
import sys
import subprocess
import spacy
from textblob import TextBlob

# Initialize pygame
pygame.init()

# Ensure spaCy model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Model not found. Installing...")
    python_executable = sys.executable
    subprocess.run([python_executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Try to import transformers, use TextBlob as fallback
try:
    from transformers import pipeline
    sentiment_pipeline = pipeline("sentiment-analysis")
    use_transformers = True
except ImportError:
    print("Warning: transformers library not found. Using TextBlob for sentiment analysis instead.")
    use_transformers = False

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
pygame.display.set_caption('Stroop Task V3')

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

# Personality traits
class Personality:
    def __init__(self):
        self.openness = random.uniform(0, 1)
        self.conscientiousness = random.uniform(0, 1)
        self.extraversion = random.uniform(0, 1)
        self.agreeableness = random.uniform(0, 1)
        self.neuroticism = random.uniform(0, 1)

    def update(self, feedback):
        adjustment = 0.05 if feedback == 'positive' else -0.05
        self.agreeableness = max(0, min(1, self.agreeableness + adjustment))
        self.neuroticism = max(0, min(1, self.neuroticism - adjustment))

personality = Personality()

# Emotion recognition function
def detect_emotion(text):
    if use_transformers:
        result = sentiment_pipeline(text)[0]
        return result['label']
    else:
        # Fallback to TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return 'POSITIVE'
        elif polarity < -0.1:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'

# Generate response based on personality and emotion
def generate_response(emotion, performance):
    if emotion == 'POSITIVE':
        if personality.extraversion > 0.7:
            return "Great job! You're doing amazing!"
        else:
            return "Well done."
    elif emotion == 'NEGATIVE':
        if personality.agreeableness > 0.7:
            return "Don't worry, you're still doing well. Keep going!"
        else:
            return "Focus and try to improve."
    else:
        if personality.openness > 0.7:
            return "Interesting performance. Let's see how you do in the next round!"
        else:
            return "Let's continue with the next trial."

# Instructions screen
def show_instructions():
    screen.fill(WHITE)
    instructions = [
        "Stroop Task Instructions:",
        "1. If the word matches the ink color, press 'Y'.",
        "2. If the word does NOT match the ink color, press 'N'.",
        "3. You can provide feedback after each trial.",
        "Press any key to begin."
    ]
    for i, line in enumerate(instructions):
        instruction_text = small_font.render(line, True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 100 + i * 50))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False

# Stroop trial function
def stroop_trial(word, color):
    global correct_responses
    
    screen.fill(WHITE)
    text = font.render(word, True, color)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()

    start_time = time.time()

    response = None
    while response is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    response = "Y"
                elif event.key == pygame.K_n:
                    response = "N"

    reaction_time = time.time() - start_time
    reaction_times.append(reaction_time)

    is_congruent = (word.upper() == list(color_map.keys())[list(color_map.values()).index(color)])
    correct_response = "Y" if is_congruent else "N"
    is_correct = (response == correct_response)

    if is_correct:
        correct_responses += 1

    trial_data.append({
        "word": word,
        "color": color,
        "response": response,
        "reaction_time": reaction_time,
        "correct": is_correct
    })

    # Display feedback and get user emotion
    screen.fill(WHITE)
    feedback_text = "Correct!" if is_correct else "Incorrect."
    feedback_render = small_font.render(feedback_text, True, BLACK)
    screen.blit(feedback_render, (screen_width // 2 - feedback_render.get_width() // 2, screen_height // 2 - feedback_render.get_height() // 2))
    pygame.display.flip()

    pygame.time.wait(1000)

    screen.fill(WHITE)
    emotion_prompt = small_font.render("How do you feel? (Type your response)", True, BLACK)
    screen.blit(emotion_prompt, (screen_width // 2 - emotion_prompt.get_width() // 2, screen_height // 2 - emotion_prompt.get_height() // 2))
    pygame.display.flip()

    user_emotion = ""
    waiting_for_emotion = True
    while waiting_for_emotion:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_emotion = False
                elif event.key == pygame.K_BACKSPACE:
                    user_emotion = user_emotion[:-1]
                else:
                    user_emotion += event.unicode
        
        screen.fill(WHITE)
        screen.blit(emotion_prompt, (screen_width // 2 - emotion_prompt.get_width() // 2, screen_height // 2 - emotion_prompt.get_height() // 2 - 50))
        emotion_text = small_font.render(user_emotion, True, BLACK)
        screen.blit(emotion_text, (screen_width // 2 - emotion_text.get_width() // 2, screen_height // 2 + emotion_text.get_height() // 2))
        pygame.display.flip()

    emotion = detect_emotion(user_emotion)
    response = generate_response(emotion, is_correct)

    screen.fill(WHITE)
    response_text = small_font.render(response, True, BLACK)
    screen.blit(response_text, (screen_width // 2 - response_text.get_width() // 2, screen_height // 2 - response_text.get_height() // 2))
    pygame.display.flip()

    pygame.time.wait(2000)

    # Update personality based on performance
    personality.update('positive' if is_correct else 'negative')

# Display results at the end
def show_results():
    screen.fill(WHITE)
    
    accuracy = correct_responses / num_trials * 100
    avg_reaction_time = sum(reaction_times) / len(reaction_times)

    results = [
        f"Results:",
        f"Accuracy: {accuracy:.2f}%",
        f"Average Reaction Time: {avg_reaction_time:.2f} seconds",
        f"Openness: {personality.openness:.2f}",
        f"Conscientiousness: {personality.conscientiousness:.2f}",
        f"Extraversion: {personality.extraversion:.2f}",
        f"Agreeableness: {personality.agreeableness:.2f}",
        f"Neuroticism: {personality.neuroticism:.2f}"
    ]
    for i, line in enumerate(results):
        result_text = small_font.render(line, True, BLACK)
        screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, 100 + i * 40))
    
    pygame.display.flip()

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