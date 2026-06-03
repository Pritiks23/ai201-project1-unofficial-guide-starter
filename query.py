import chromadb
from sentence_transformers import SentenceTransformer
from llm import generate_answer

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="docs")


def retrieve(query, k=4):
    query_emb = embed_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_emb,
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_id": results["metadatas"][0][i].get("chunk_id", i),
            "distance": results["distances"][0][i],
        })

    return chunks


def ask(question):
    chunks = retrieve(question, k=4)

    contexts = [
        {"text": c["text"], "source": c["source"]}
        for c in chunks
    ]

    answer = generate_answer(question, contexts)

    return {
        "answer": answer,
        "sources": list({c["source"] for c in chunks}),
        "chunks": chunks
    }