# Jira Acceptance Criteria Generation Agent

AI-powered Jira Acceptance Criteria Generator using:

- FastAPI (Backend)
- Streamlit (Frontend)
- Ollama (Local LLM)
- Qwen / Llama Models

---

## Project Structure

```text
Jira-Acceptance-Criteria-Generation/

├── backend/
│   ├── app.py
│   ├── llm.py
│   ├── prompts.py
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
│
└── README.md
```

---

## Features

- Generate Jira Acceptance Criteria from User Stories
- Given / When / Then format
- Multiple User Story Support
- Local LLM using Ollama
- FastAPI REST API
- Streamlit UI

---

## Prerequisites

- Python 3.12+
- Ollama

Install a model:

```bash
ollama pull llama3.1:8b
```

Verify installation:

```bash
ollama list
```

---

## Run Backend

```bash
cd backend

uvicorn app:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Run Frontend

```bash
cd frontend

streamlit run streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## API Example

### Endpoint

```http
POST /generate
```

### Request

```json
{
  "stories": [
    "As a user I want to login using email and password",
    "As an admin I want to deactivate users"
  ]
}
```

### Response

```json
{
  "results": [
    {
      "story": "As a user I want to login using email and password",
      "acceptance_criteria": "..."
    }
  ]
}
```

---

## Example User Story

```text
As a user I want to reset my password.
```

### Generated Output

```text
Given a registered user

When the user requests password reset

Then a reset link should be sent to the registered email
```

---

## Future Enhancements

- Jira Integration
- Test Case Generation
- Risk Analysis
- Story Classification
- Export to PDF
- RAG using BRD/SRS Documents
- Multi-Model Support

---

## Author

Biswayan Paul
