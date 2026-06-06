import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

DB_DIR = "data/chroma_db"
COLLECTION_NAME = "unofficial_guide_chunks"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 4

embedding_model = SentenceTransformer(MODEL_NAME)
chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve(query, top_k=TOP_K):
    query_embedding = embedding_model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_number": results["metadatas"][0][i]["chunk_number"],
            "distance": results["distances"][0][i],
        })

    return retrieved


def build_context(chunks):
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']}, chunk {chunk['chunk_number']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def ask(question):
    retrieved_chunks = retrieve(question)

    # Reject weak retrievals
    relevant_chunks = [
        chunk for chunk in retrieved_chunks
        if chunk["distance"] < 0.9
    ]

    if len(relevant_chunks) == 0:
        return {
            "answer": "I don't have enough information in the provided documents to answer that.",
            "sources": [],
            "retrieved_chunks": []
        }

    # Use only relevant chunks
    retrieved_chunks = relevant_chunks

    context = build_context(retrieved_chunks)

    prompt = f"""
You are answering questions for a RAG system called The Unofficial Guide.

Answer the user's question using ONLY the provided context.
Do not use outside knowledge.
If the context does not contain enough information to answer, say:
"I don't have enough information in the provided documents to answer that."

Be concise, factual, and grounded in the documents.

Context:
{context}

Question:
{question}

Answer:
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You must answer only from the retrieved context. Do not make up facts."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    sources = []
    seen = set()

    for chunk in retrieved_chunks:
        label = f"{chunk['source']} - chunk {chunk['chunk_number']} - distance {chunk['distance']:.4f}"
        if label not in seen:
            sources.append(label)
            seen.add(label)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }
