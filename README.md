# Smart Assistant for Document Summarization & QA

An AI-powered assistant built with Django that reads PDF or TXT documents and enables:
- Automatic Summarization (≤150 words)
- Contextual Question Answering
- Justified answers with document references
- Interactive chat history

---
 
### Features

- Upload structured documents (PDF or TXT)
- Auto-summary using `sshleifer/distilbart-cnn-12-6`
- Ask Anything mode for document-based QA
- FAISS vector search over document chunks
- Context retrieval with `MiniLM` sentence embeddings
- QA using `distilbert-base-uncased-distilled-squad`
- Chat history display
- Clean UI with Bootstrap
- Reset chat functionality

---

##  Tech Stack

| Layer       | Tools Used                                  |
|-------------|----------------------------------------------|
| Backend     | Python, Django                              |
| Frontend    | HTML, CSS, Bootstrap                        |
| NLP Models  | `transformers`, `sentence-transformers`     |
| Embeddings  | `all-MiniLM-L6-v2`                          |
| Summarizer  | `sshleifer/distilbart-cnn-12-6`             |
| QA Model    | `distilbert-base-uncased-distilled-squad`   |
| Vector Search | FAISS                                     |
| PDF Parsing | PyMuPDF (`fitz`)                            |

---

## Project Structure
```
smart-assistant/
├── assistant/
│ ├── templates/
│ │ ├── upload.html
│ │ ├── summary.html
│ │ └── ask.html
│ ├── utils/
│ │ └── text_processing.py
│ ├── views.py
│ ├── models.py
│ └── urls.py
├── media/
│ └── (Uploaded files)
├── manage.py
├── requirements.txt
├── .gitignore

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

### 4. Run Django Server
```python manage.py runserver```

---

## Screenshots
<img width="1904" height="791" alt="image" src="https://github.com/user-attachments/assets/cece0392-4c8a-490a-9cdd-784627f75ae4" />
<img width="1903" height="883" alt="Screenshot 2025-07-13 142039" src="https://github.com/user-attachments/assets/e1358f49-31a4-408c-951e-4b0a0e793cfc" />
<img width="1911" height="897" alt="Screenshot 2025-07-13 142104" src="https://github.com/user-attachments/assets/9012c4b9-3ded-4b21-9531-13be60a8b02f" />
<img width="1906" height="803" alt="Screenshot 2025-07-13 142159" src="https://github.com/user-attachments/assets/85e97e4b-ab41-4534-9415-4551fe31d8f8" />

---

## Author

**Aditya Singh**  
 Email: [singhaditya270305@gmail.com](mailto:singhaditya270305@gmail.com)  
GitHub: [singhadi01](https://github.com/singhadi01)
© 2025 — Smart Assistant Project

