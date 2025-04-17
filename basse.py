import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os

model = SentenceTransformer("all-mpnet-base-v2")
dimensions = 768
Index = faiss.IndexFlatL2(dimensions)
database = "database.faiss"
retrieve = 0

def file_checker():
    global retrieve , Index
    if retrieve == 0:
        if os.path.exists(database) and os.path.getsize(database) != 0:
            Index = faiss.read_index(database)
            retrieve = 1

def create_vectors(text:str):
    global retrieve
    file_checker()
    vector = model.encode(text)
    Index.add(np.array([vector]))
    faiss.write_index(Index,database)
    retrieve = 1
    return text

def retrieve_indexes(query:list):
    file_checker()
    if retrieve == 1:
        vector = model.encode(query)
        D, I = Index.search(np.array(vector),k=3)
        return I.tolist()
    else :
        return str("Database Do not Exist")


