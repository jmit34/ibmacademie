# Les imports (si besoin faire un venv python -m venv monrag et pip install ollama, numpy)
import ollama

def main():
    # this workshop will be using IBM Granite
    modelname = 'granite3-moe'

    SYSTEM_PROMPT = """You are a helpful reading assistant who answers questions 
        based on snippets of text provided in context. Answer only using the context provided, 
        being as concise as possible. Please if you're not sure just say that you don't know.
        Context: """
    
    while True: 
        prompt = input("what do you want to know? -> ")
        response = ollama.chat(
            model=modelname,
            messages=[
                {"role": "system","content": SYSTEM_PROMPT},
                { "role": "user", "content": prompt}
            ],)
        print("\n\n")
        print(response["message"]["content"])

if __name__ =="__main__":
    main()