import chromadb
from sentence_transformers import SentenceTransformer
import uuid

# ----------------------------
# LOAD MODEL (LOCAL EMBEDDING)
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------
# INIT CHROMA DB (LOCAL PERSISTENCE)
# ----------------------------
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="docker_rag"
)


# ----------------------------
# EMBED + STORE CHUNKS
# ----------------------------
def embed_chunks(chunks):
    """
    Takes chunks from ingestion pipeline and stores them in ChromaDB
    """

    texts = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        texts.append(chunk["text"])

        metadatas.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        })

        # unique id per chunk
        ids.append(str(uuid.uuid4()))

    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ Embedded and stored {len(texts)} chunks")


# ----------------------------
# RETRIEVAL FUNCTION
# ----------------------------
def retrieve(query, k=4):
    """
    Returns top-k relevant chunks + metadata + distance
    """

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    chunks = []

    for i in range(len(results["documents"][0])):

        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_id": results["metadatas"][0][i]["chunk_id"],
            "distance": results["distances"][0][i]
        })

    return chunks


# ----------------------------
# DEBUG / TESTING
# ----------------------------
def test_retrieval(queries):
    for q in queries:
        print("\n" + "=" * 60)
        print("QUERY:", q)

        results = retrieve(q, k=4)

        for r in results:
            print("\n--- RESULT ---")
            print("SOURCE:", r["source"])
            print("CHUNK_ID:", r["chunk_id"])
            print("DISTANCE:", round(r["distance"], 4))
            print(r["text"][:400])


# ----------------------------
# MAIN (TEST RUN)
# ----------------------------
if __name__ == "__main__":

    # TEMP: import your ingestion output
    from ingestion import run

    docs, chunks = run()

    embed_chunks(chunks)

    test_queries = [
        "What is Docker and how do containers work?",
        "How does Kubernetes manage scaling?",
        "What are best practices for Docker security?"
    ]

    test_retrieval(test_queries)