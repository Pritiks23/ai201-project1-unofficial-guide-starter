from sentence_transformers import SentenceTransformer
from llm import generate_answer
import numpy as np

# ----------------------------
# EMBEDDING MODEL
# ----------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------
# LOAD CHUNKS
# ----------------------------
# Expecting: [{"text": ..., "source": ..., "chunk_id": ...}, ...]
# You should pass this from ingestion OR save/load JSON
from ingestion import run

docs, CHUNKS = run()

texts = [c["text"] for c in CHUNKS]
metas = [{"source": c["source"], "chunk_id": c["chunk_id"]} for c in CHUNKS]

print(f"Loaded {len(CHUNKS)} chunks for retrieval")


# ----------------------------
# PRECOMPUTE EMBEDDINGS
# ----------------------------
print("Embedding chunks...")
chunk_embeddings = embed_model.encode(texts, normalize_embeddings=True)


# ----------------------------
# RETRIEVAL (COSINE SIMILARITY)
# ----------------------------
def retrieve(query, k=4):
    query_emb = embed_model.encode(query, normalize_embeddings=True)

    # cosine similarity via dot product (because normalized)
    scores = np.dot(chunk_embeddings, query_emb)

    top_k_idx = np.argsort(scores)[::-1][:k]

    results = []
    for idx in top_k_idx:
        results.append({
            "text": texts[idx],
            "source": metas[idx]["source"],
            "chunk_id": metas[idx]["chunk_id"],
            "distance": float(scores[idx])
        })

    return results


# ----------------------------
# ASK (GROUNDED GENERATION)
# ----------------------------
def ask(question):
    chunks = retrieve(question, k=4)

    context_text = "\n\n".join(
        [f"[SOURCE: {c['source']}]\n{c['text']}" for c in chunks]
    )

    prompt = f"""
You are a grounded QA system.

RULES:
- Use ONLY the provided context.
- If answer is not in context, say: "I don't have enough information."
- Do NOT use outside knowledge.
- Always be precise and factual.

CONTEXT:
{context_text}

QUESTION:
{question}

ANSWER:
"""

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": list({c["source"] for c in chunks}),
        "chunks": chunks
    }