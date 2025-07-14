import os
from django.shortcuts import render, redirect
from .forms import DocumentUploadForm
from .models import UploadedDocument
import re

from .utils.text_processing import (
    extract_text_from_file,
    extract_text_from_pdf,
    generate_summary,
    chunk_text,
    build_faiss_index,
    answer_question,
    generate_quiz_questions,
    evaluate_user_answer,
    load_vectorstore
)

VECTOR_DB_PATH = "vectorstore/db_faiss"


def home(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            file_path = os.path.join('media', doc.file.name)
            documents = extract_text_from_pdf(file_path) 
            build_faiss_index(documents)
            summary = generate_summary(file_path)
            preview_text = " ".join([doc.page_content for doc in documents])[:1000]
            request.session['uploaded'] = True
            return render(request, 'summary.html', {
                'file_url': doc.file.url,
                'filename': doc.file.name,
                'summary': summary,
                'full_text': preview_text
            })
    else:
        form = DocumentUploadForm()

    return render(request, 'home.html', {'form': form})


def ask_anything(request):
    answer = None
    context = ""
    question = ""

    if request.method == 'POST':
        question = request.POST.get('question', "").strip()

        if not question:
            return render(request, 'ask.html', {
                'error': "Please enter a question.",
                'question': "",
                'answer': None,
                'justification': ""
            })

        try:
            answer, context = answer_question(question)
        except Exception as e:
            return render(request, 'ask.html', {
                'error': f"Error answering question: {str(e)}",
                'question': question,
                'answer': None,
                'justification': ""
            })

    return render(request, 'ask.html', {
        'question': question,
        'answer': answer,
        'justification': "Answer based on your uploaded document." if answer else "",
        'error': None if answer else "No relevant answer found."
    })


def reset_chat(request):
    request.session["qa_history"] = []
    return redirect("ask")

def quiz_view(request):
    try:
        faiss_db = load_vectorstore()
        context_text = " ".join([doc.page_content for doc in faiss_db.similarity_search("generate quiz", k=3)])
    except:
        return render(request, "quiz.html", {"error": "Please upload and summarize a document first."})

    if request.method == "POST":
        questions = request.session.get("quiz_questions", [])
        results = []
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f"answer{i+1}", "").strip()
            result = evaluate_user_answer(question, user_answer, context_text)
            results.append(result)
        return render(request, "quiz.html", {"results": results})
    questions = generate_quiz_questions(context_text)
    request.session["quiz_questions"] = questions
    return render(request, "quiz.html", {"questions": questions})