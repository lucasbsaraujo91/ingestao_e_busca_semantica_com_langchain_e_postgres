import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector

# Embeddings (OpenAI ou Gemini)
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_embeddings():
    provider = os.getenv("PROVIDER", "openai").lower()
    if provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY não definido e PROVIDER=gemini.")
        model = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
        return GoogleGenerativeAIEmbeddings(api_key=api_key, model=model)
    # default: openai
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não definido e PROVIDER=openai.")
    model = os.getenv("OPENAI_MODEL", "text-embedding-3-small")
    return OpenAIEmbeddings(model=model)


def main() -> None:
    env_path = Path(__file__).with_name(".env")  # .env na pasta src (ajuste se preferir)
    if not env_path.exists():
        # fallback: .env na raiz do repo
        env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path, override=True)

    for k in ("PGVECTOR_URL", "PGVECTOR_COLLECTION"):
        if not os.getenv(k):
            raise RuntimeError(f"Faltou {k} no .env")

    # Carrega PDF
    pdf_path = Path(__file__).resolve().parents[1] / "document.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

    docs = PyPDFLoader(str(pdf_path)).load()

    # Split (1000/150)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, add_start_index=False
    )
    splits = splitter.split_documents(docs)
    if not splits:
        print("Nenhum chunk gerado.")
        return

    # Limpa metadados em branco
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in (d.metadata or {}).items() if v not in ("", None)},
        )
        for d in splits
    ]
    ids = [f"doc-{i}" for i in range(len(enriched))]

    # Embeddings
    emb = get_embeddings()

    # Vetor store (usa 'embeddings=' para compatibilidade com sua versão)
    store = PGVector(
        connection=os.getenv("PGVECTOR_URL"),
        collection_name=os.getenv("PGVECTOR_COLLECTION", "docs"),
        embeddings=emb,
        use_jsonb=True,
        # create_extension=True,  # opcional (compose já cria)
    )

    store.add_documents(documents=enriched, ids=ids)
    print(f"Ingestão concluída: {len(enriched)} chunks → coleção '{os.getenv('PGVECTOR_COLLECTION')}'.")
    

if __name__ == "__main__":
    main()
