import streamlit as st
from main import run_agent
from streamlit_chat import message

st.set_page_config(page_title="🧠 RAG AI Agent", page_icon="🤖", layout="wide")

# 💅 Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #141E30, #243B55);
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        background-color: #2e2e40;
        color: white;
        border: 1px solid #4B0082;
        padding: 10px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #8A2BE2, #4B0082);
        color: white;
        border-radius: 10px;
        height: 45px;
        font-weight: bold;
        border: none;
        box-shadow: 0px 0px 5px #4B0082;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .reflection-box {
        background-color: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ About the App")
st.sidebar.info("""
**Sri Indu College AI Assistant**

- 🎓 College Information Support
- 💡 Uses **Ollama API**
- 🧠 Powered by **ChromaDB + RAG**
- 🔍 Smart Question Retrieval
- 📚 Fees, Timetable, Placements
- ✨ Built by **Endurthi P.K**
""")
st.sidebar.markdown("🌟 *Ask anything from your knowledge base!*")
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Chat Section
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🎓 Sri Indu College AI Assistant")
st.caption("Ask about fees, timetable, placements, notices, and faculty details")

# Chat input
query = st.chat_input("Type your question here...") or None

# 💡 Quick Question Buttons
st.subheader("💡 Quick Questions")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎓 College information?"):
        query = "College information?"
    elif st.button("👨‍🏫 Who is the principal?"):
        query = "Who is the principal?"
    elif st.button("📍 Where is the college located?"):
        query = "Where is the college located?"
    elif st.button("📝 When are exams?"):
        query = "When are exams?"

with col2:
    if st.button("📅 What is today's timetable?"):
        query = "What is today's timetable?"
    elif st.button("🏢 Placement details?"):
        query = "Placement details?"
    elif st.button("💵 What is the fee structure?"):
        query = "What is the fee structure?"
    elif st.button("📚 What is Monday timetable?"):
        query = "What is Monday timetable?"

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("🎓 Searching college information..."):
        answer = run_agent(query)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# Display conversation
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user_{i}")
    elif msg["role"] == "assistant":
        message(msg["content"], key=f"ai_{i}")
