# 🤖 AI Agent Portfolio

Welcome to the **AI Agent Portfolio**!  
This project is a modular, local-first AI agent framework designed to help you build, evaluate, and interact with AI-powered chatbots and knowledge systems. 🚀

---

## 📚 Table of Contents

- [🖼️ How it looks like](#-how-it-looks-like)
- [✨ Features](#-features)
- [🛠️ Technologies Used](#-technologies-used)
- [🚀 Getting Started](#-getting-started)
- [📚 Create Knowledge Base](#-create-knowledge-base)
- [💻 Running the Project Locally](#-running-the-project-locally)
- [📂 Project Structure](#-project-structure)
- [🤔 How It Works](#-how-it-works)
- [📝 License](#-license)

---

## 🖼️ How it looks like

<img width="1289" height="685" alt="Screenshot 2025-07-24 at 8 02 35 p m" src="https://github.com/user-attachments/assets/6c390815-a71a-42c5-8ab8-b03e6bd1b8f2" />

---

## ✨ Features

- Modular chat agent framework 🤝
- RAG (Retrieval-Augmented Generation) support 📖
- Local vector store with ChromaDB 🗃️
- Easy-to-extend tools and controllers 🛠️
- Knowledge base integration 🧠
- Email collection and storage 📧

---

## 🛠️ Technologies Used

- **Python 3.12** 🐍
- **ChromaDB** for vector storage 🗂️
- **OpenAI / Gemini /LLM APIs** (if integrated) 🤖
- **LangChain** for RAG 🦜
- **Gradio** for UI 🎨
- **NLTK** for text processing 📝
- **MongoDB** for storing user details 📝

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai_agent.git
cd ai_agent
```

### 2. Install Dependencies

We recommend using [uv](https://github.com/astral-sh/uv) for fast environment management and dependency installation.

1. **Install uv** (if you don't have it):

   ```bash
   brew install uv
   ```

2. **Create a virtual environment:**

   ```bash
   uv venv .venv
   ```

3. **Activate the environment:**

   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install all dependencies:**

   ```bash
   uv pip install -r requirements.txt
   ```

   Or, if you use `pyproject.toml`:

   ```bash
   uv sync .
   ```

---

## 📚 Create Knowledge Base

1. Create a new folder in the `knowledge` directory.
2. Create new files in the folder.
3. Add the content of the file to the knowledge base.

---

## 💻 Running the Project Locally

### Run the Main Application

```bash
python main.py
```

- The main entry point is `main.py`.

### Environment Variables

- You will need to set the following environment variables:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `MONGO_URI`
- `MONGO_DB_CLIENT`
- `MONGO_DB_COLLECTION`

If you want to deploy in huggingface, you will need to set the following environment variables:

- `HF_TOKEN`

---

## 📂 Project Structure

```
ai_agent/
  ├── app/                # Setup of gradio UI
  ├── chat/               # Chat agent, RAG, tools, and evaluation modules
  ├── chroma_store/       # Local vector database (ChromaDB)
  ├── knowledge/          # Knowledge base files (txt)
  ├── main.py             # Project entry point
  ├── requirements.txt    # Python dependencies
  └── pyproject.toml      # Project metadata
```

---

## 🤔 How It Works

1. **Knowledge Ingestion:**  
   The system loads knowledge from text files and stores embeddings in ChromaDB.

2. **Chat & RAG:**  
   The chat agent uses retrieval-augmented generation to answer questions, pulling relevant context from the knowledge base.

3. **Extensible Tools:**  
   Easily add new tools or evaluators in the `chat/` directory to expand your agent’s capabilities.

---

## 📝 License

MIT License.  
Feel free to use, modify, and share! 🌟

---

> Made with ❤️ by Diego Araque
