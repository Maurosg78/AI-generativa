import sqlite3
import numpy as np
import openai
import argparse
import glob
from tqdm import tqdm
from dotenv import load_dotenv
import os

# Cargar el archivo .env desde la ruta especificada
load_dotenv("/Users/mauriciosobarzo/Desktop/2025/Marzo/rag-basico/.env")

# Inicializar el cliente de OpenAI usando la clave de API desde las variables de entorno
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chunker(text, chunk_size=1000, overlap=200):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i : i + chunk_size])
    return chunks

def clean_text(text):
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        # Eliminar solo líneas que sean puramente ruido (encabezados, pies de página, etc.)
        if any(noise in line.lower() for noise in ["boletín oficial del estado", "pág.", "núm.", "lunes", "boe-a-", "boe-b-"]):
            continue
        # Eliminar líneas vacías o con solo espacios
        if line.strip() == "":
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def populate_embeddings(chunks):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chunks (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 text TEXT UNIQUE,
                 embedding BLOB)''')
    for chunk in chunks:
        c.execute("SELECT embedding FROM chunks WHERE text = ?", (chunk,))
        result = c.fetchone()
        if result:
            print(f"Chunk ya existe, usando embedding cacheado: {chunk[:50]}...")
            continue
        embedding = get_embedding(chunk)
        embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
        c.execute("INSERT INTO chunks (text, embedding) VALUES (?, ?)", (chunk, embedding_bytes))
    conn.commit()
    return conn

def query_embeddings(query, conn, top_k=10):  # Cambia top_k de 5 a 10
    c = conn.cursor()
    query_embedding = get_embedding(query)
    c.execute("SELECT text, embedding FROM chunks")
    results = c.fetchall()

    similarities = []
    for text, emb_bytes in results:
        embedding = np.frombuffer(emb_bytes, dtype=np.float32)
        similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
        similarities.append((text, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Depuración: mostrar los 5 chunks más relevantes
    print("Top 5 chunks más relevantes:")
    for i, (text, sim) in enumerate(similarities[:5], 1):
        print(f"Chunk {i} (similitud: {sim:.4f}): {text[:100]}...")

    context_chunks = [text for text, _ in similarities[:top_k]]
    context = "\n".join(context_chunks)
    
    prompt = f"Contexto:\n{context}\n\nPregunta: {query}\nInstrucción: Responde con la información del contexto. Si no encuentras la respuesta, di 'No está disponible'."
    return prompt

def main():
    parser = argparse.ArgumentParser(description="RAG básico para procesar documentos.")
    parser.add_argument("--docs", type=str, default="boe.md", help="Patrón de archivos a procesar (ej. boe.md)")
    parser.add_argument("--query", type=str, help="Consulta para buscar en los documentos")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Tamaño de los chunks")
    parser.add_argument("--overlap", type=int, default=200, help="Solapamiento entre chunks")
    args = parser.parse_args()

    documents = glob.glob(args.docs)
    all_chunks = []
    for doc in documents:
        print(f"Procesando documento: {doc}")
        with open(doc, "r", encoding="utf-8") as f:
            text = f.read()
        cleaned_text = clean_text(text)
        chunks = chunker(cleaned_text, chunk_size=args.chunk_size, overlap=args.overlap)
        all_chunks.extend(chunks)

    conn = populate_embeddings(all_chunks)

    if args.query:
        prompt = query_embeddings(args.query, conn)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        print("Respuesta:", response.choices[0].message.content)

    conn.close()

if __name__ == "__main__":
    main()