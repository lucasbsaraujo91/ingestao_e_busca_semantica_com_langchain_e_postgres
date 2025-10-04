import os
from pathlib import Path
from dotenv import load_dotenv

from search import search_with_scores
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    provider = os.getenv("PROVIDER", "openai").lower()
    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model=os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash-lite"),
            temperature=0,
        )
    return ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-5-nano"),
        temperature=0,
    )

PROMPT_TEMPLATE = """CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def main():
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path, override=True)

    print("Faça sua pergunta (digite 'sair' para encerrar).")
    llm = get_llm()

    while True:
        question = input("\nPERGUNTA: ").strip()
        if not question:
            continue
        if question.lower() in {"sair", "exit", "quit"}:
            break

        results = search_with_scores(question, k=10)

        if not results:
            print('RESPOSTA: Não tenho informações necessárias para responder sua pergunta.')
            continue

        # junta os conteúdos dos top-k
        context_parts = []
        for tup in results:
            doc, score = tup
            context_parts.append(doc.page_content.strip())
        context = "\n\n---\n\n".join(context_parts).strip()

        if not context:
            print('RESPOSTA: Não tenho informações necessárias para responder sua pergunta.')
            continue

        prompt = PROMPT_TEMPLATE.format(context=context, question=question)
        response = llm.invoke(prompt)
        answer = getattr(response, "content", str(response))
        print(f"RESPOSTA: {answer}")

if __name__ == "__main__":
    main()
