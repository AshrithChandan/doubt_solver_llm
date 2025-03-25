# inference/ask.py
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Dynamically find latest model version
def get_latest_model_path():
    base_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    folders = [f for f in os.listdir(base_dir) if f.startswith("fine_tuned_model")]
    if not folders:
        raise FileNotFoundError(f"No fine-tuned models found in {base_dir}")
    latest = sorted(folders)[-1]
    return os.path.join(base_dir, latest)


MODEL_PATH = get_latest_model_path()

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH).to(device)

# Set up pipeline
qa = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device == "cuda" else -1)

# Chat loop
print("🧠 Doubt Solver LLM - Ask your questions (type 'exit' to quit):")
while True:
    question = input("\nQ: ")
    if question.lower() in ["exit", "quit"]:
        break
    prompt = f"### Question:\n{question}\n\n### Answer:\n"
    answer = qa(prompt, max_length=128, do_sample=True, temperature=0.7)[0]['generated_text']
    print("A:", answer.split("### Answer:\n")[-1].strip())
