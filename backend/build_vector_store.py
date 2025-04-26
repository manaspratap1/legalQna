from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load chunks
with open("chunks.txt", "r", encoding="utf-8") as f:
    chunks = f.read().split("\n---\n")

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks, show_progress_bar=True)

# Save chunks for later retrieval
with open("chunk_texts.txt", "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(c + "\n<CHUNK>\n")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, "vector_index.faiss")

print("✅ FAISS index saved as vector_index.faiss")
