import os

import numpy as np
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


emb = CohereEmbeddings(model="embed-english-v3.0")
sents = [
    "The cat sat on the sofa.",
    "A kitten is resting on the couch.",
    "Quarterly revenue grew by 12 percent.",
]
vecs = np.array(emb.embed_documents(sents))
print("dimension:", vecs.shape[1])


def cosine(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


print("related  :", cosine(vecs[0], vecs[1]))
print("unrelated:", cosine(vecs[0], vecs[2]))
