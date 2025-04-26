import pdfplumber

with pdfplumber.open("mv_act.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

with open("mv_act.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("✅ Extracted text saved to mv_act.txt")
