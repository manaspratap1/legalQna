import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

with open("mv_act.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

sentences = sent_tokenize(full_text)
chunks = []
chunk = ""

for sentence in sentences:
    if len(chunk) + len(sentence) <= 500:
        chunk += " " + sentence
    else:
        chunks.append(chunk.strip())
        chunk = sentence

if chunk:
    chunks.append(chunk.strip())

with open("chunks.txt", "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(c + "\n---\n")

print(f"✅ Split into {len(chunks)} chunks. Saved to chunks.txt")
