# le texte du RAG :  https://newsroom.ibm.com/
# 2024-10-21-ibm-introduces-granite-3-0-high-performing-ai-models-built-for-business
# l'inspiration : youtube chaine, vidéo lien Youtube Decoder : RAG from the Ground Up with Python and Ollama
# https://www.youtube.com/watch?v=V1Mz8gMBDMo

# Les imports (si besoin faire un venv python -m venv monrag et pip install ollama, numpy)
import time, os, json, ollama, numpy as np 
from numpy.linalg import norm

current_dir = os.path.dirname(__file__) 

# ceci pour reformatter le texte correctement et éviter les coupures de ligne 
def parse_text(filename): 
    with open(filename,encoding="utf-8-sig") as f:
        paragraphs = []
        buffer = []
        for line in f.readlines():
            line = line.strip()
            if line:
                buffer.append(line)
            elif len(buffer):
                paragraphs.append(" ".join(buffer))
                buffer = []
        if len(buffer): 
            paragraphs.append(" ".join(buffer))
        return paragraphs
    
# get embeddings, s'il existent on les load, sinon on les génère, c'est un peu long.
def get_embeddings(filename,model,chunks):
    # on vérifie si on a déja sauvé les embeddings, 
    if (embeddings := load_embeddings(filename)) is not False:
        return embeddings
    # sinon on les refait
    embeddings = [ollama.embeddings(model=model, prompt=chunk)["embedding"]for chunk in chunks ]
    # et on les sauve
    save_embeddings(filename,embeddings)
    return embeddings

# si on a déja fait les embeddings on les reprend du fichier
def load_embeddings(filename):
    # check if file exists
    if not os.path.exists(filename):
        return False
    # dump embedings to json:
    with open(filename, "r") as f:
        return json.load(f)    

# On sauve les embeddings si on vient de les calculer
def save_embeddings(file_emb,embeddings):
    
    # create dir if did not exist :
    path_emb = "/".join(file_emb.split("/")[:-1])
    if not os.path.exists(path_emb):
        os.makedirs(path_emb)
    # dump embedings to json:
    with open(file_emb, "w") as f:
        json.dump(embeddings,f)

def find_most_similar(needle, haystack):
    needle_norm = norm(needle)
    similarity_scores = [np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

def main(): 
    # this workshop will be using IBM Granite
    modelname = 'granite3-moe'
    # open ragfile and rearrange for paragraphs
    ragfile = current_dir+"/my_info.txt"
  
    paragraphs= parse_text(ragfile)

    file_emb = ragfile.split(".")[0]+".json"

    start = time.perf_counter()
    # on charge les embeddings (s'ils sont déjà fait on les reprend du fichier, sinon on les 
    # crée et on les mets dans un fichier : 
    embeddings = get_embeddings(file_emb,modelname,paragraphs)
    print(time.perf_counter() - start)
    
    # les embeddinsgs sont prêt, on passe en mode prompt 
    SYSTEM_PROMPT = """You are a helpful reading assistant who answers questions. Answer  
        being as concise as possible. If you're unsure, just say that you don't know.
         """
    
    prompt = input("what do you want to know? -> ")
    
    prompt_embedding = ollama.embeddings(modelname, prompt=prompt)["embedding"]
    # find most similar to each other
    most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:5]

    response = ollama.chat(
        model=modelname,
        messages=[{
                "role": "system",
                "content": SYSTEM_PROMPT
                + "\n".join(paragraphs[item[1]] for item in most_similar_chunks),
            },
            {"role": "user", "content": prompt},],
        )
    print("\n\n")
    print(response["message"]["content"])

if __name__ =="__main__":
    main()