import numpy as np
from sentence_transformers import SentenceTransformer
from ingestion import run

# ----------------------------
# LOAD EMBEDDING MODEL
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------
# SIMPLE VECTOR STORE (IN MEMORY)
# ----------------------------
class SimpleVectorStore:
    def __init__(self):
        self.vectors = []
        self.texts = []
        self.sources = []
        self.chunk_ids = []

    def add(self, embeddings, chunks):
        for emb, chunk in zip(embeddings, chunks):
            self.vectors.append(emb)
            self.texts.append(chunk["text"])
            self.sources.append(chunk["source"])
            self.chunk_ids.append(chunk["chunk_id"])

    def search(self, query_embedding, k=4):
        scores = []

        for vec in self.vectors:
            # cosine similarity
            score = np.dot(query_embedding, vec) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(vec)
            )
            scores.append(score)

        top_k_idx = np.argsort(scores)[::-1][:k]

        results = []
        for idx in top_k_idx:
            results.append({
                "text": self.texts[idx],
                "source": self.sources[idx],
                "chunk_id": self.chunk_ids[idx],
                "score": float(scores[idx])
            })

        return results


# ----------------------------
# BUILD INDEX
# ----------------------------
def build_index(chunks):
    print("Embedding chunks...")

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    store = SimpleVectorStore()
    store.add(embeddings, chunks)

    return store


# ----------------------------
# RETRIEVAL FUNCTION
# ----------------------------
def retrieve(store, query, k=4):
    query_emb = model.encode(query)

    return store.search(query_emb, k=k)


# ----------------------------
# TESTING
# ----------------------------
def test(store):
    queries = [
        "What is Docker used for?",
        "How does Kubernetes scaling work?",
        "Docker container security best practices"
    ]

    for q in queries:
        print("\n" + "=" * 60)
        print("QUERY:", q)

        results = retrieve(store, q)

        for r in results:
            print("\n--- RESULT ---")
            print("SOURCE:", r["source"])
            print("CHUNK ID:", r["chunk_id"])
            print("SCORE:", round(r["score"], 4))
            print(r["text"][:300])


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    docs, chunks = run()

    print(f"\nLoaded {len(chunks)} chunks")

    store = build_index(chunks)

    test(store)