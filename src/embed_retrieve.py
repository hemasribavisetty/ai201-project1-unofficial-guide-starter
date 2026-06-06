import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path("data/chunks/chunks.json")
DB_DIR = "data/chroma_db"
COLLECTION_NAME = "unofficial_guide_chunks"

MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 4


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_vector_store(chunks):
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=DB_DIR)

    # Delete old collection if it exists, so reruns are clean
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_number": chunk["chunk_number"],
        }
        for chunk in chunks
    ]

    print(f"Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts).tolist()

    print("Saving chunks to ChromaDB...")
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Saved {collection.count()} chunks to ChromaDB.")
    return collection, model


def retrieve(query, collection, model, top_k=TOP_K):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []

    for i in range(len(results["documents"][0])):
        retrieved.append(
            {
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )

    return retrieved


def print_results(query, results):
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Source: {result['metadata']['source']}")
        print(f"Chunk number: {result['metadata']['chunk_number']}")
        print(f"Distance: {result['distance']:.4f}")
        print("Text:")
        print(result["text"])
        print("-" * 80)


def main():
    chunks = load_chunks()
    collection, model = build_vector_store(chunks)

    test_queries = [
        "What do students say about Robert Bierman and CSC 415?",
        "Are CS students required to complete 12 units of electives?",
        "What do students say about the SFSU CS program overall?",
        "What easy classes do students recommend at SFSU?",
        "Which professor is praised as helpful by students?",
    ]

    for query in test_queries:
        results = retrieve(query, collection, model)
        print_results(query, results)


if __name__ == "__main__":
    main()