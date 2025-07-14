import os
from typing import List
from dotenv import load_dotenv, find_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import re

load_dotenv(find_dotenv())
PDF_DIR = "media/"
DB_PATH = "vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm_model = ChatGroq(model="deepseek-r1-distill-llama-70b")

PROMPT_TEMPLATE = """
Answer the following question based on the context below.

Context:
{context}

Question:
{question}

Answer in one sentence:
"""

QUIZ_GENERATION_PROMPT = """You are a helpful assistant. Generate exactly 3 quiz questions based ONLY on the content below.

Rules:
- Do NOT include answers.
- Do NOT use <think> or internal reasoning steps.
- Output only the questions, numbered 1 to 3.
- Keep each question short and fact-based.

Content:
{context}
"""

EVALUATION_PROMPT = """
You are an AI evaluator. Your task is to assess the student's answer based solely on the given context.

Instructions:
- Give a numeric score from 0 to 100 that teels how much the student's answer match exact answer
- Extract the correct answer from the context.
- Provide a short justification.
- DO NOT hallucinate or assume anything beyond the context.

Respond ONLY in the following format:

Score (0-100): <numeric score>
Correct Answer: <correct answer>
Justification: <explanation>

Question: {question}
Student Answer: {user_answer}
Reference Context: {context}
"""

PROMPT_TEMPLATE = """
Answer the following question based on the context below.

Context:
{context}

Question:
{question}

Answer in one sentence:
"""

# Document Processing Functions

def extract_text_from_pdf(file_path: str) -> List[Document]:
    loader = PyMuPDFLoader(file_path)
    return loader.load()

def build_faiss_index(documents: List[Document]):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    faiss_db = FAISS.from_documents(chunks, embedding_model)
    faiss_db.save_local(DB_PATH)

def load_vectorstore():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("FAISS index not found. Please upload and process a document first.")
    return FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)


# Answering and Summarizing

def answer_question(question: str):
    try:
        faiss_db = load_vectorstore()
        docs = faiss_db.similarity_search(question, k=3)
        context = " ".join([doc.page_content for doc in docs])

        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        chain = prompt | llm_model | StrOutputParser()

        answer = chain.invoke({"context": context, "question": question})
        if hasattr(answer, "content"):
            answer = answer.content
        else:
            answer = str(answer)

        cleaned_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
        return cleaned_answer , context
    except Exception as e:
        return f"Error: {str(e)}", ""
        
def generate_summary(file_path: str):
    docs = extract_text_from_pdf(file_path)
    text = " ".join([doc.page_content for doc in docs])
    words = text.split()
    if len(words) > 1500:
        text = " ".join(words[:1500])

    summary_prompt = (
    "You are an expert summarizer.\n"
    "Summarize the following content in clear, concise ~150 words:\n\n"
    f"{text}"
)
    result = llm_model.invoke(summary_prompt)
    if hasattr(result, "content"):
            result = result.content
    else:
        result = str(result)
    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL).strip()
    return result

def extract_text_from_file(file_path):
    documents = extract_text_from_pdf(file_path)
    return " ".join([doc.page_content for doc in documents])

from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(documents, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True
    )
    chunks = splitter.split_documents(documents)
    
    for i, chunk in enumerate(chunks):
        chunk.metadata["paragraph"] = i + 1
    return chunks

def generate_quiz_questions(context_text: str) -> List[str]:
    prompt = ChatPromptTemplate.from_template(QUIZ_GENERATION_PROMPT)
    chain = prompt | llm_model | StrOutputParser()
    raw = chain.invoke({"context": context_text})
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    return [q.strip().split(". ", 1)[-1] for q in raw.strip().split("\n") if q.strip()]

def evaluate_user_answer(question: str, user_answer: str, context_text: str) -> dict:
    prompt = ChatPromptTemplate.from_template(EVALUATION_PROMPT)
    chain = prompt | llm_model | StrOutputParser()
    result_text = chain.invoke({"question": question, "user_answer": user_answer, "context": context_text})
    
    score_match = re.search(r"Score \(0-100\):\s*(\d{1,3})", result_text)
    correct_match = re.search(r"Correct Answer:\s*(.+)", result_text)
    justification = result_text.split("Justification:", 1)[-1].strip()

    return {
        "question": question,
        "user_answer": user_answer,
        "score": score_match.group(1) if score_match else "N/A",
        "correct_answer": correct_match.group(1).strip() if correct_match else "N/A",
        "justification": justification
    }