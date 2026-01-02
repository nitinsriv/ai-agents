import os
import asyncio
from typing import List
from pdfminer.high_level import extract_text
import openai

openai_api_key = os.environ.get('OPENAI_API_KEY')
if not openai_api_key:
    print('Warning: OPENAI_API_KEY not set; embeddings and chat calls will fail until set.')
openai.api_key = openai_api_key

# simple in-memory store
STORE = []  # list of dicts: {id, text, embedding, source}

async def embed_text(text: str) -> List[float]:
    resp = openai.Embedding.create(model='text-embedding-3-small', input=text)
    return resp['data'][0]['embedding']

import math

def cosine(a, b):
    dot = 0.0
    la = 0.0
    lb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        la += x * x
        lb += y * y
    return dot / (math.sqrt(la) * math.sqrt(lb) + 1e-10)

async def load_pdfs_and_index(dir_path: str):
    if not os.path.exists(dir_path):
        print('PDF directory not found:', dir_path)
        return
    for fn in os.listdir(dir_path):
        if not fn.lower().endswith('.pdf'): continue
        path = os.path.join(dir_path, fn)
        text = extract_text(path)
        # naive chunking
        for i in range(0, len(text), 1000):
            chunk = text[i:i+1000]
            emb = await embed_text(chunk)
            STORE.append({'id': f'{fn}-{i}', 'text': chunk, 'embedding': emb, 'source': fn})

async def answer_question(question: str, top_k: int = 4) -> str:
    if not STORE:
        return 'No documents indexed.'
    qemb = await embed_text(question)
    sims = [{'item': item, 'score': cosine(qemb, item['embedding'])} for item in STORE]
    sims.sort(key=lambda x: x['score'], reverse=True)
    top = '\n\n---\n\n'.join([s['item']['text'] for s in sims[:top_k]])
    prompt = f"Use the following extracted document snippets to answer the question. If not contained, say you don't know.\n\nContext:\n{top}\n\nQuestion: {question}\n\nAnswer:"
    resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'user','content':prompt}], max_tokens=512)
    return resp['choices'][0]['message']['content']
