from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer
import faiss
import numpy as np
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

index = faiss.read_index("vector_index.faiss")

with open("chunk_texts.txt", "r", encoding="utf-8") as f:
    chunks = f.read().split("\n<CHUNK>\n")
    
retriever = SentenceTransformer("all-MiniLM-L6-v2")
generator = T5ForConditionalGeneration.from_pretrained("t5-base")
tokenizer = T5Tokenizer.from_pretrained("t5-base")

with open("greeting_responses.json", "r", encoding="utf-8") as f:
    greeting_responses = json.load(f)

class Query(BaseModel):
    question: str

def answer_question(question, top_k=3):
    q_embedding = retriever.encode([question])
    D, I = index.search(np.array(q_embedding), top_k)
    context = " ".join([chunks[i] for i in I[0]])
    prompt = f"question: {question} context: {context}"
    input_ids = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).input_ids
    output = generator.generate(input_ids, max_length=500)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer

@app.post("/ask")
def ask(query: Query):
    question = query.question.lower().strip()

    if question in greeting_responses:
        return {
            "question": query.question,
            "answer": greeting_responses[question]
        }

    result = answer_question(query.question)
    return {
        "question": query.question,
        "answer": result
    }
