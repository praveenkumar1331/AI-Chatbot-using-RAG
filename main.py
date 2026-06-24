import os
import glob
import time
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

# ─────────────────────────────
#  Load environment variables
# ─────────────────────────────
load_dotenv()
OLLAMA_MODEL = "tinyllama"

# ─────────────────────────────
#  Simple classes and helpers
# ─────────────────────────────
class SimpleDoc:
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata


END = "__END__"


class SimpleStateGraph:
    """Lightweight sequential graph executor (plan → retrieve → answer → reflect)."""

    def __init__(self):
        self.nodes, self.edges, self.entry = {}, {}, None

    def add_node(self, name, func):
        self.nodes[name] = func

    def add_edge(self, from_node, to_node):
        self.edges[from_node] = to_node

    def set_entry_point(self, name):
        self.entry = name

    def compile(self):
        graph = self

        class Runner:
            def __init__(self, g):
                self.g = g

            def invoke(self, state):
                cur = self.g.entry
                visited = set()
                while cur and cur != END:
                    if cur in visited:
                        raise RuntimeError(f"Cycle detected at node {cur}")
                    visited.add(cur)
                    node = self.g.nodes[cur]
                    print(f"➡️ Executing node: {cur}")
                    try:
                        state = node(state)
                    except Exception as e:
                        print(f"⚠️ Error in node {cur}: {e}")
                        state["error"] = str(e)
                        break
                    cur = self.g.edges.get(cur, None)
                return state

        return Runner(graph)

# ─────────────────────────────
#  Data loading + vector store
# ─────────────────────────────
def load_documents(data_path="data"):
    docs = []

    for file in glob.glob(f"{data_path}/*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

            # split by lines / sections
            chunks = text.split("\n\n")

            for i, chunk in enumerate(chunks):
                chunk = chunk.strip()
                if chunk:
                    docs.append(
                        SimpleDoc(
                            page_content=chunk,
                            metadata={
                                "source": os.path.basename(file),
                                "chunk_id": i
                            }
                        )
                    )

    return docs


def build_vector_store(docs, persist_dir="chroma_db"):
    client = PersistentClient(path=persist_dir)
    collection_name = "rag_documents"
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    # Always recreate collection for latest data
    try:
        client.delete_collection(collection_name)
        print("🗑️ Old collection deleted")
    except:
        pass

    print("⚙️ Creating new Chroma collection")
    collection = client.create_collection(collection_name)

    texts = [d.page_content for d in docs]
    metadatas = [d.metadata for d in docs]
    ids = [f"doc_{i}" for i in range(len(texts))]

    embeddings = embedder.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    ).tolist()

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )

    print(f"✅ Added {len(texts)} documents to Chroma.")

    return {
        "client": client,
        "collection": collection,
        "embedder": embedder
    }


def similarity_search(vectordb, query, k=3):
    collection, embedder = vectordb["collection"], vectordb["embedder"]
    q_emb = embedder.encode([query], convert_to_numpy=True).tolist()[0]
    results = collection.query(query_embeddings=[q_emb], n_results=k, include=["documents", "metadatas"])
    docs = [SimpleDoc(page_content=t, metadata=m) for t, m in zip(results["documents"][0], results["metadatas"][0])]
    return docs


# ─────────────────────────────
#  Ollama Api helper using SDK
# ─────────────────────────────
def generate_ollama_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"].strip()
    except Exception as e:
        return f"⚠️ Ollama error: {e}"
# ─────────────────────────────
#  LangGraph-style workflow
# ─────────────────────────────
def plan(state):
    print("🧭 PLAN: Interpreting the query…")
    state["needs_retrieval"] = True
    return state


def retrieve(state):
    print("🔍 RETRIEVE: Fetching similar documents...")
    
    vectordb = state["vectordb"]
    query = state["query"]

    docs = similarity_search(vectordb, query, k=1)

    if docs:
        state["context"] = docs[0].page_content.strip()
    else:
        state["context"] = ""

    print(f"✅ Retrieved {len(docs)} docs.")
    return state


def answer(state):
    print("💬 ANSWER: Returning direct result...")

    context = state.get("context", "").strip()

    if not context:
        state["answer"] = "Sorry, this information is not available."
    else:
        state["answer"] = context

    return state



def reflect(state):
    print("🔎 REFLECT: Checking answer quality…")
    prompt = (
        f"Question: {state['query']}\n"
        f"Answer: {state['answer']}\n"
        "Evaluate whether the answer is relevant and complete in one short paragraph."
    )

    state["reflection"] = generate_ollama_response(prompt)
    print("✅ Reflection generated.")
    return state


# ─────────────────────────────
#  Build & run workflow
# ─────────────────────────────
def build_graph(vectordb):
    graph = SimpleStateGraph()
    graph.add_node("plan", plan)
    graph.add_node("retrieve", retrieve)
    graph.add_node("answer", answer)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


def run_agent(query):
    print(f"\n💡 Running Agent for Query: {query}")
    docs = load_documents()
    vectordb = build_vector_store(docs)
    graph_runner = build_graph(vectordb)
    state = {"query": query, "vectordb": vectordb}
    final_state = graph_runner.invoke(state)
    return final_state.get("answer", "No answer")


if __name__ == "__main__":
    q = input("Ask a question: ")
    a = run_agent(q)
    print("\nANSWER:\n", a)
