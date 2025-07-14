# Smart Assistant for Document Summarization, QA & Quiz Evaluation

An AI-powered assistant built with Django and Groq LLM that can:
- Auto-summarize uploaded documents (≤150 words)
- Answer questions based on document context
- Provide one-line justified answers
- Generate quizzes and evaluate your answers with scores

---

## Features

- Upload PDF/TXT documents
- Auto-summary using **Groq (DeepSeek R1 Distill LLaMA 70B)**
- Ask Anything mode using context-aware retrieval
- FAISS vector index on document chunks
- Context retrieval with `MiniLM` sentence embeddings
- Quiz Mode: 3 questions generated from your uploaded document
- Evaluation with:
  - Score (0–100)
  - Justification
  - Correct Answer
- Clean Bootstrap UI
- Reset chat/quiz anytime

---

## 🛠️ Tech Stack

| Layer         | Tools Used                                    |
|---------------|------------------------------------------------|
| Backend       | Python, Django                                 |
| Frontend      | HTML, CSS, Bootstrap                           |
| Embeddings    | `all-MiniLM-L6-v2` via HuggingFace             |
| LLM (QA+Summary) | `deepseek-r1-distill-llama-70b` via **Groq API** |
| Quiz + Evaluation | LangChain + Prompt Engineering             |
| Vector Search | FAISS                                          |
| Document Parsing | PyMuPDF                                     |

---

##  Project Structure


```
smart-assistant/
├── assistant/
│ ├── templates/
│ │ ├── upload.html
│ │ ├── summary.html
│ │ ├── ask.html
│ │ └── quiz.html
│ ├── utils/
│ │ └── text_processing.py
│ ├── views.py
│ ├── models.py
│ └── urls.py
├── vectorstore/
│ └── db_faiss/
├── media/
│ └── (Uploaded PDFs)
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md 

```
---

##  Local Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/singhadi01/smart-assistant.git
cd smart-assistant
```

### 2. Create and Activate Virtual Environment

```
python -m venv env
env\Scripts\activate     # For Windows
# OR
source env/bin/activate  # For macOS/Linux
```
### 3. Install Dependencies
```pip install -r requirements.txt```

### 4. Add your Groq API Key
```Create a file named .env and add:
GROQ_API_KEY=your_groq_api_key_here
```
### 4. Run Django Server
```python manage.py runserver```

---

## Screenshots
<img width="1911" height="760" alt="image" src="https://github.com/user-attachments/assets/59eb6b1c-a26a-47e6-b0b3-1ffb54d0185a" />
<img width="1911" height="956" alt="image" src="https://github.com/user-attachments/assets/afc24ec9-73de-4c71-8ff1-3615587497e4" />
<img width="1902" height="773" alt="image" src="https://github.com/user-attachments/assets/25922fb6-4677-4900-9c66-5cf2f37a6a2c" />
<img width="1907" height="950" alt="image" src="https://github.com/user-attachments/assets/2bf18f62-0ae9-469b-8d3f-d25d62ad3c5d" />
<img width="1907" height="985" alt="image" src="https://github.com/user-attachments/assets/6dd8ccca-8ce7-4126-9f28-3028d6e219c4" />


---

## Author

**Aditya Singh**  
 Email: [singhaditya270305@gmail.com](mailto:singhaditya270305@gmail.com)  
GitHub: [singhadi01](https://github.com/singhadi01)
© 2025 — Smart Assistant Project

