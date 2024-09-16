from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import matplotlib.pyplot as plt
import numpy as np

# Load model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model.eval()

def predict_next_word_probs(input_text, model, tokenizer, temperature=1.0, top_k=10):
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    with torch.no_grad():
        outputs = model(input_ids)

    logits = outputs.logits[:, -1, :] / temperature
    probs = torch.softmax(logits, dim=-1).cpu().numpy().flatten()

    top_k_probs = np.argsort(probs)[-top_k:][::-1]
    top_k_tokens = [tokenizer.decode([i]).strip() for i in top_k_probs]
    top_k_values = probs[top_k_probs]

    plt.figure(figsize=(10, 5))
    plt.bar(top_k_tokens, top_k_values)
    plt.title(f"Next Word Probabilities for Input: '{input_text}'")
    plt.ylabel("Probability")
    plt.xlabel("Next Word")
    plt.xticks(rotation=45)
    plt.show()

    return list(zip(top_k_tokens, top_k_values))

input_text = "Machine learning is"
predict_next_word_probs(input_text, model, tokenizer, temperature=0.7, top_k=10)
