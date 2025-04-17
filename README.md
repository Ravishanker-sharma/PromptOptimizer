# 🤖 PromptOptimizer - AI That Learns *You*

PromptOptimizer is an intelligent AI assistant framework designed to learn and adapt to each user's behavior and communication style over time. It silently analyzes the user's word choices, tone, formatting, and preferences to optimize prompts and deliver highly personalized responses.

Developed by **CODEX-RaviSharma**, this system combines vector search, behavior profiling, and modular agents powered by Google's Gemini API and FAISS to create a continuously learning assistant experience.

---

## 🔍 Key Features

- **Personalized Prompt Optimization**: Learns how you write, think, and ask — and then refines your inputs to generate more precise AI responses.
- **Silent Behavior Tracking**: Continuously stores new insights about the user from each interaction in a PostgreSQL-backed vector database.
- **Modular Agents**: Utilizes sub-agents like `Behaviour_finder` to retrieve prior user behavior without interrupting the experience.
- **Vector Search Integration**: Fast retrieval of behavioral patterns using FAISS and sentence-transformer embeddings.
- **Asynchronous Interaction Flow**: Built with an `async` runner that ensures smooth streaming responses.

---

## 🧠 Architecture Overview
```bash
User Query
↓
Behaviour_finder Agent (fetches past behavior via vector search)
↓
Root Agent (refines the prompt, stores new insights)
↓
Gemini Model (generates the final response)
↓
Final Answer (sent back to user)
```
---

## 📁 Project Structure
```bash
. ├── agent.py # Main agent setup and response handling logic
  ├── behave.py # Behaviour_finder sub-agent logic
  ├── database.py # Vector + PostgreSQL database interactions
  ├── basse.py # FAISS vector embedding and similarity search
  ├── postgresSQL.py # PostgreSQL utility functions
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/PromptOptimizer.git
cd PromptOptimizer
```
## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```
## Make sure you have the following in your environment:

✅ Python 3.8+

✅ PostgreSQL server running

✅ .env file with appropriate environment variables

## 2. Configure PostgreSQL
Update the connection details inside database.py:

```bash
dbname = "vectordata"
user = "postgres"
password = "12345678"
host = "localhost"
port = "5432"
```
✅ Ensure the table textdata is created automatically when the system initializes.

## 🚀 Usage
You can interact with the system by calling the call_agent() or using a terminal command function with a user query:
```bash
# Terminal command for ADK UI kit -- Best
adk web {directory_name}
```

```bash
from agent import call_agent
import asyncio

response = asyncio.run(call_agent("Help me write a professional email."))
print(response)
```
### Each new message:

🔍 Triggers the behavior agent to fetch past behavioral data

✨ Refines your prompt based on that data

🧠 Stores new information if discovered

🤖 Returns a highly personalized AI response

## 🧰 Tools & Libraries Used
Google ADK

FAISS - Facebook AI Similarity Search

SentenceTransformers

PostgreSQL


## 📌 Notes
🔒 This system never reveals that it's learning from the user

🧠 It stores only new behavioral insights on each query

♻️ Designed for long-term personalization and evolving user experiences

## 👨‍💻 Developed By
Ravishanker Sharma
~ CODEX ~

