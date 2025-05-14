#  si besoin faire un venv python -m venv monrag et pip install ollama
import ollama

modelname = 'granite3-moe' # (llama, mistral... )
ollama.pull(modelname)
    
while True:      
    prompt = input("what do you want to know? -> ")
    response = ollama.chat(model=modelname,messages=[{ "role": "user", "content": prompt}])
    print("\n\n", response["message"]["content"])
