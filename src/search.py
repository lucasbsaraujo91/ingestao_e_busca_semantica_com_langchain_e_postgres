import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_embeddings():
    provider = os.getenv("PROVIDER", "openai").lower()
    if provider == "gemini":
        return GoogleGenerativeAIEmbeddings(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model=os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001"),
        )
    return OpenAIEmbeddings(
        model=os.getenv("OPENAI_MODEL", "text-embedding-3-small")
    )


def get_store():
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path, override=True)

    emb = get_embeddings()
    return PGVector(
        connection=os.getenv("PGVECTOR_URL"),
        collection_name=os.getenv("PGVECTOR_COLLECTION", "docs"),
        embeddings=emb,
        use_jsonb=True,
    )


def search_with_scores(query: str, k: int = 10):
    store = get_store()
    # 1) tentar plural
    try:
        return store.similarity_search_with_scores(query, k=k)
    except AttributeError:
        pass
    # 2) tentar singular (sua versão)
    try:
        return store.similarity_search_with_score(query, k=k)
    except AttributeError:
        pass
    # 3) fallback sem score
    docs = store.similarity_search(query, k=k)
    return [(d, None) for d in docs]
