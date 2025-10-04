# 🧠 Ingestão e Busca Semântica com LangChain + Postgres (pgvector)

## 🚀 Objetivo
Este projeto permite:
- **Ingestão:** Ler um arquivo `document.pdf`, quebrar em *chunks* (1000 tokens / 150 de overlap), gerar embeddings e salvar tudo no Postgres com **pgvector**.  
- **Busca:** Fazer perguntas via CLI e receber respostas **com base no conteúdo do PDF**, sem usar dados externos.
- **Chat:** Interagir em modo conversacional com o conteúdo ingerido, como se fosse um assistente treinado apenas no seu PDF.

---

## 🧩 Tecnologias
- **Python 3.10+**
- **LangChain**
- **PostgreSQL + pgvector**
- **Docker & Docker Compose**
- **OpenAI** ou **Google Gemini** (para embeddings e chat)

---

## ⚙️ Requisitos
- Python 3.10 ou superior (se quiser rodar localmente)
- Docker e Docker Compose instalados
- Conta e chave de API da OpenAI (ou Google, se usar Gemini)

---

## 🧰 Estrutura do Projeto

```
📦 projeto/
├── .env
├── docker-compose.yml
├── requirements.txt
├── src/
│   ├── ingest.py
│   ├── search.py
│   ├── test_search.py
│   └── chat.py
└── document.pdf
```

---

## 🔧 Arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com o conteúdo abaixo:

```bash
# ===== Banco de dados =====
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5440/rag
PGVECTOR_COLLECTION=gpt5_collection

# ===== OpenAI (padrão) =====
OPENAI_API_KEY=coloque_sua_chave_aqui
OPENAI_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-5-nano

# ===== Gemini (opcional) =====
GOOGLE_API_KEY=
GEMINI_EMBEDDING_MODEL=models/embedding-001
GEMINI_CHAT_MODEL=gemini-2.5-flash-lite

# ===== Seletor de provedor =====
PROVIDER=openai
```

---

## 🐳 💻 Como Rodar o Projeto com Docker

### 1️⃣ Subir o banco de dados com pgvector
Na raiz do projeto, execute:
```bash
docker compose up -d
```

Isso irá:
- Criar um container **Postgres 17 com a extensão pgvector**
- Expor a porta **5440**
- Criar o banco **rag**

Verifique se o container está ativo:
```bash
docker compose ps
```

E acesse o banco, se quiser conferir:
```bash
psql "postgresql://postgres:postgres@127.0.0.1:5440/rag"
```

---

### 2️⃣ (Opcional) Rodar o Python dentro de um container
Se quiser rodar tudo dentro de um container Python (sem instalar dependências localmente), adicione no seu `docker-compose.yml` algo como:

```yaml
services:
  app:
    build: .
    volumes:
      - .:/app
    depends_on:
      - postgres
    environment:
      - PGVECTOR_URL=${PGVECTOR_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PROVIDER=${PROVIDER}
    command: tail -f /dev/null
```

Depois suba novamente:
```bash
docker compose up -d --build
```

E entre no container:
```bash
docker exec -it app bash
```

---

## 🧾 Etapas do Projeto

### 🧩 1️⃣ Ingestão de Documentos
Execute:
```bash
python3 src/ingest.py
```
Isso irá:
- Ler o arquivo `document.pdf`
- Gerar *chunks* (partes menores de texto)
- Criar embeddings
- Inserir tudo no Postgres na coleção configurada

---

### 🔍 2️⃣ Busca Semântica (CLI)
Para fazer perguntas sobre o conteúdo do PDF:
```bash
python3 src/test_search.py
```
O script fará a busca vetorial no banco, recuperará os trechos mais relevantes e responderá com base apenas no conteúdo indexado.

---

### 💬 3️⃣ Usando o Chat
Este modo permite uma **conversa interativa** com o conteúdo do seu PDF.

Execute:
```bash
python3 src/chat.py
```

O sistema:
- Carrega as embeddings salvas no Postgres  
- Mantém o contexto entre as perguntas (memória de chat)  
- Usa o modelo definido no `.env` (`OPENAI_CHAT_MODEL` ou `GEMINI_CHAT_MODEL`)  
- Responde de forma conversacional sobre o conteúdo do documento

#### 🧠 Exemplo de uso:
```
Usuário: Qual é o tema principal do documento?
Assistente: O documento discute o processo de avaliação do GPT-5 e o compara ao GPT-4 em termos de raciocínio e consistência.
Usuário: E como o GPT-5 se sai melhor?
Assistente: O GPT-5 apresenta maior consistência em raciocínios complexos e múltiplos passos, além de reduzir a taxa de alucinações em relação ao GPT-4.
```

---

## 🧰 Comandos Úteis do Docker

| Comando | Descrição |
|----------|------------|
| `docker compose up -d` | Sobe os containers em segundo plano |
| `docker compose down` | Derruba todos os containers |
| `docker compose logs -f` | Mostra os logs em tempo real |
| `docker compose ps` | Mostra o status dos containers |
| `docker exec -it app bash` | Abre o shell dentro do container do app |
| `docker exec -it postgres bash` | Abre o shell dentro do Postgres |
| `psql "postgresql://postgres:postgres@127.0.0.1:5440/rag"` | Acessa o banco localmente |

---

## 🧠 Dicas Extras

- Você pode armazenar vários PDFs e ajustar o `ingest.py` para processar todos de uma pasta `docs/`.
- Para usar o **Gemini** ao invés da **OpenAI**, altere no `.env`:
  ```bash
  PROVIDER=gemini
  ```

---

## 🧾 Licença
MIT © 2025 — Desenvolvido por **Lucas Batista**
