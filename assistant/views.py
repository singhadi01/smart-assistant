from django.shortcuts import render,redirect
from .forms import DocumentUploadForm
from .models import UploadedDocument
from .utils.text_processing import extract_text_from_file, generate_summary, chunk_text, build_vector_index, answer_question


import os

def home(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            file_path = os.path.join('media', doc.file.name)

            full_text = extract_text_from_file(file_path)
            summary = generate_summary(full_text)
            
            chunks = chunk_text(full_text)
            build_vector_index(chunks)
            request.session['uploaded'] = True
            
            return render(request, 'summary.html', {
                'file_url': doc.file.url,
                'filename': doc.file.name,
                'summary': summary,
                'full_text': full_text[:1000]  
            })
    else:
        form = DocumentUploadForm()
    return render(request, 'home.html', {'form': form})

from .utils.text_processing import answer_question
global_text = None
chunks_built = False

def ask_anything(request):
    global global_text, chunks_built
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
        if not global_text or not chunks_built:
            try:
                doc = UploadedDocument.objects.latest('id')
                import os
                file_path = os.path.join('media', doc.file.name)
                global_text = extract_text_from_file(file_path)

                chunks = chunk_text(global_text)
                build_vector_index(chunks)
                chunks_built = True
            except Exception as e:
                return render(request, 'ask.html', {
                    'error': f"Error loading document: {e}",
                    'question': question,
                    'answer': None,
                    'justification': ""
                })

        answer, context = answer_question(question)

    return render(request, 'ask.html', {
        'question': question,
        'answer': answer,
        'justification': "Answer based on your uploaded document." if answer else "",
        'error': None if answer else "No relevant answer found."
    })

def reset_chat(request):
    request.session["qa_history"] = []
    return redirect("ask")