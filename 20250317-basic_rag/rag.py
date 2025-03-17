import openai

# import os

# os.environ["OPENAI_API_KEY"] = "sk-proj-1234567890"


def chunker(text, chunk_size=1000, overlap=200):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i : i + chunk_size])
    return chunks


def get_embedding(text):
    # ....
    pass


def populate_embeddings(chunks):
    pass
    # ....
    # Opciones: PG/Supabase
    # SQLlite
    # Memoria/Python
    # Especializadas en esto: Pinecone


def query_embeddings(query):
    pass
    # ....
    # 1. Hago el embedding de la query
    # 2. Busco en la BBDD por embedding
    # 3. Me devuelven los chunks mas cercanos
    # 4. Armo el prompt


def main():
    # Create client instance
    client = openai.OpenAI()

    prompt = "Hello, how are you?"
    # Use chat completions with the new API format
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    # Access response content with the new format
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
