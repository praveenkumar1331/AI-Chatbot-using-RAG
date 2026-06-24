
# 🧠 LangGraph RAG AI Agent 

A Retrieval-Augmented Generation (RAG) AI Agent built with a LangGraph-style workflow and powered by **Google Gemini 2.0 Flash**.  
This project answers user questions from a local text knowledge base and includes an intelligent **reflection step** to verify answer quality.

---

## 🚀 Features
- 🧩 **LangGraph-style pipeline**: plan → retrieve → answer → reflect  
- 📚 **RAG workflow** using **ChromaDB** and **SentenceTransformer embeddings**  
- ⚡ **Gemini 2.0 Flash** integration (fast, latest model)  
- 💬 **Streamlit UI** for interactive chatting  
- 🪞 **Reflection mechanism** ensures response relevance and completeness  

---

## 🏗️ Project Structure
Ai-Rag_Agent/
│
├── main.py # Core RAG agent logic
├── app.py # Streamlit front-end
├── data/ # Folder for .txt knowledge files
├── chroma_db/ # Auto-created Chroma vector store
├── .env # Store your Gemini API key
└── requirements.txt # All dependencies

yaml
Copy code

---

## ⚙️ Installation

### 1️⃣ Create virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate
2️⃣ Install dependencies
bash
Copy code
pip install google-generativeai langchain chromadb sentence-transformers python-dotenv streamlit streamlit-chat
3️⃣ Set environment variable
Create a .env file in the root directory:

ini
Copy code
GEMINI_API_KEY=your_api_key_here
▶️ Running the App
💻 Command-line mode
bash
Copy code
python main.py
Ask any question (e.g., "What is renewable energy?") and the agent will retrieve, answer, and reflect.

🌐 Streamlit UI mode
bash
Copy code
streamlit run app.py
Visit http://localhost:8501 and chat with your AI Agent interactively.

📁 Adding Knowledge
Place your .txt files in the data/ folder, e.g.:

kotlin
Copy code
data/
 ├── renewable_energy.txt
 ├── artificial_intelligence.txt
The agent automatically indexes and retrieves from these files.

🧠 Workflow Overview
Plan: Decide to retrieve context.

Retrieve: Fetch top-k similar docs from Chroma.

Answer: Generate response using Gemini 2.0 Flash.

Reflect: Validate answer completeness & accuracy.

🧑‍💻 Author
Endurthi Praveen Kumar
Built with ❤️ using Python, Streamlit, and Gemini.

yaml
Copy code

---

# 🧩 **2️⃣ Agent Explanation Report (for submission)**

---

### **Title:** LangGraph RAG AI Agent using Gemini 2.0 Flash

#### **Objective**
The goal of this project was to develop a lightweight AI agent capable of answering questions from a local knowledge base using a Retrieval-Augmented Generation (RAG) workflow. The system had to use a LangGraph-style architecture to separate the reasoning process into structured steps.

---

#### **Implementation Summary**
The agent was implemented using a **custom LangGraph-style state machine** consisting of four nodes:
- **Plan:** interprets the query and determines retrieval needs.  
- **Retrieve:** uses **ChromaDB** and **SentenceTransformer embeddings** to fetch the most relevant documents.  
- **Answer:** sends the query and retrieved context to **Gemini 2.0 Flash** for answer generation.  
- **Reflect:** performs self-evaluation on the generated answer to ensure it is relevant and complete.

The application supports two modes:
- **Command-line interface (CLI)** for testing and debugging.
- **Streamlit UI** for a visually appealing and interactive user experience.

---

#### **Technologies Used**
- **Python 3.11**
- **Google Gemini 2.0 Flash API**
- **LangChain / ChromaDB**
- **SentenceTransformers (MiniLM-L6-v2)**
- **Streamlit** for UI
- **dotenv** for environment variable management

---

#### **Results**
The system successfully retrieves relevant information and generates accurate responses with reflection feedback.  
It was tested with a small text dataset (e.g., renewable energy, AI, climate change).  
Response time averages **1–2 seconds**, demonstrating the performance advantage of Gemini 2.0 Flash.

---

#### **Conclusion**
This project fulfills the task requirements by:
- Implementing a modular **LangGraph-inspired RAG workflow**,  
- Using **Gemini 2.0 Flash** as a powerful and fast LLM, and  
- Providing a clean, user-friendly **Streamlit interface**.

The design is scalable for larger datasets and can be extended with additional reflection or evaluation nodes.

