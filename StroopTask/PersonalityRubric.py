import sys
import subprocess
import spacy
from textblob import TextBlob

# Ensure the model is installed before loading
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Model not found. Installing...")
    python_executable = sys.executable
    subprocess.run([python_executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Define the Big Five and HEXACO traits
traits = {
    'OCEAN': {
        'Openness': ['creative', 'curious', 'imaginative', 'open-minded', 'inventive'],
        'Conscientiousness': ['organized', 'dependable', 'disciplined', 'responsible', 'methodical'],
        'Extraversion': ['sociable', 'talkative', 'outgoing', 'energetic', 'assertive'],
        'Agreeableness': ['kind', 'compassionate', 'trustworthy', 'cooperative', 'empathetic'],
        'Neuroticism': ['anxious', 'moody', 'irritable', 'insecure', 'sensitive']
    },
    'HEXACO': {
        'Honesty-Humility': ['sincere', 'fair', 'modest', 'humble', 'honest'],
        'Emotionality': ['sensitive', 'anxious', 'emotional', 'sentimental', 'fearful'],
        'Extraversion': ['sociable', 'bold', 'lively', 'confident', 'optimistic'],
        'Agreeableness': ['forgiving', 'tolerant', 'patient', 'understanding', 'cooperative'],
        'Conscientiousness': ['diligent', 'organized', 'thorough', 'reliable', 'perfectionist'],
        'Openness': ['curious', 'artistic', 'creative', 'imaginative', 'inquisitive']
    }
}

# Function to analyze the character's personality based on their description
def analyze_personality(description):
    doc = nlp(description)
    
    # Initialize counters for traits in both models
    ocean_scores = {trait: 0 for trait in traits['OCEAN']}
    hexaco_scores = {trait: 0 for trait in traits['HEXACO']}
    
    # Analyze sentiment for neuroticism
    sentiment = TextBlob(description).sentiment
    neuroticism_score = 1 - sentiment.polarity  # Negative polarity = more neurotic
    
    # Tokenize and analyze each word in the description
    for token in doc:
        for model in traits:
            for trait, keywords in traits[model].items():
                if token.lemma_ in keywords:
                    if model == 'OCEAN':
                        ocean_scores[trait] += 1
                    else:
                        hexaco_scores[trait] += 1

    # Assign the neuroticism score separately for OCEAN
    ocean_scores['Neuroticism'] = neuroticism_score
    
    return ocean_scores, hexaco_scores

# Example character description
character_description = """
John is a highly creative and imaginative person. He is often quiet but becomes quite talkative in social situations. 
Though kind-hearted, he tends to be anxious in stressful situations and is extremely organized when it comes to his work.
"""

# Analyze the description
ocean_result, hexaco_result = analyze_personality(character_description)

# Display the results
print("OCEAN Personality Scores:")
for trait, score in ocean_result.items():
    print(f"{trait}: {score}")

print("\nHEXACO Personality Scores:")
for trait, score in hexaco_result.items():
    print(f"{trait}: {score}")
