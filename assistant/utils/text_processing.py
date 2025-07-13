import fitz  # for PDF text extraction
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# ----------- Text Extraction Functions -----------

def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return ""

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

import re
def clean_text(raw_text):
    text = re.sub(r"http\S+|www\S+|@\S+|\S+\.com", "", raw_text) 
    text = re.sub(r"[\[\]\(\){}]", "", text) 
    text = re.sub(r"\s{2,}", " ", text)  
    text = re.sub(r"(Education|Skills|Experience|Projects|Certifications|Achievements|Internship)", r"\n\n\1:\n", text, flags=re.IGNORECASE)
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = text.strip()
    text = re.sub(r"([a-zA-Z])\.([A-Z])", r"\1. \2", text)
    return text
# ----------- Summary Function -----------

def generate_summary(text, max_words=150):
    text = text.strip().replace('\n', ' ')
    text=clean_text(text)
    if len(text) > 3000:
        text = text[:3000]
    summary = summarizer(text, max_length=130, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# ----------- Chunking + Indexing -----------

stored_chunks = []
stored_vectors = None

def chunk_text(text, chunk_size=300):
    words = text.split()
    if not words:
        return []
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def build_vector_index(chunks):
    global stored_chunks, stored_vectors
    if not chunks:
        print("No chunks found. Check your document content.")
        stored_chunks = []
        stored_vectors = None
        return

    stored_chunks = chunks
    embeddings = embedding_model.encode(chunks)
    if len(embeddings) == 0:
        print("No embeddings generated.")
        return

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    stored_vectors = index

# ----------- QA Function (Accurate One-Liner Answer) -----------

def answer_question(question):
    global stored_chunks, stored_vectors
    if stored_vectors is None or not stored_chunks:
        return "No document context found.", ""

    question_embedding = embedding_model.encode([question])
    D, I = stored_vectors.search(np.array(question_embedding), k=3)
    top_chunks = [stored_chunks[i] for i in I[0]]
    context = " ".join(top_chunks)[:3000]

    result = qa_pipeline(question=question, context=context)
    return result['answer'], context
