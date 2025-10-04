# 🧠 Ingestão e Busca Semântica com LangChain + Postgres (pgvector)

## 🚀 Objetivo
Este projeto permite:
- **Ingestão:** Ler um arquivo `document.pdf`, quebrar em *chunks* (1000 tokens / 150 de overlap), gerar embeddings e salvar tudo no Postgres com **pgvector**.  
- **Busca:** Fazer perguntas via CLI e receber respostas **com base no conteúdo do PDF**, sem usar dados externos.

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
│   └── test_search.py
└── document.pdf
```

---

## 🔧 Arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com o conteúdo abaixo:

```bash
# ===== Banco de dados =====
# URL de conexão com o Postgres + pgvector
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5440/rag
# Nome da coleção onde os embeddings serão armazenados
PGVECTOR_COLLECTION=gpt5_collection

# ===== OpenAI (padrão) =====
# Sua chave de API da OpenAI (obrigatória se usar o provedor OpenAI)
OPENAI_API_KEY=coloque_sua_chave_aqui
# Modelo de embeddings
OPENAI_MODEL=text-embedding-3-small
# Modelo de chat
OPENAI_CHAT_MODEL=gpt-5-nano

# ===== Gemini (opcional) =====
# Sua chave de API do Google (se for usar Gemini)
GOOGLE_API_KEY=
# Modelo de embeddings do Gemini
GEMINI_EMBEDDING_MODEL=models/embedding-001
# Modelo de chat do Gemini
GEMINI_CHAT_MODEL=gemini-2.5-flash-lite

# ===== Seletor de provedor =====
# Define qual provedor será usado: "openai" ou "gemini"
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
Se você quiser rodar a aplicação dentro de um container Python (sem precisar instalar dependências localmente), adicione no seu `docker-compose.yml` algo como:

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

E entre no container para rodar os scripts:
```bash
docker exec -it app bash
```

---

### 3️⃣ Rodar os scripts (no host ou no container)

**Ingestão de documentos:**
```bash
python3 src/ingest.py
```
Isso vai:
- Ler o arquivo `document.pdf`
- Gerar os *chunks*
- Criar embeddings
- Inserir os vetores no Postgres (coleção definida no `.env`)

**Busca semântica (CLI):**
```bash
python3 src/test_search.py
```
O script fará uma pergunta e mostrará a resposta com base nos dados vetorizados.

---

## 🧰 Comandos Úteis do Docker

| Comando | Descrição |
|----------|------------|
| `docker compose up -d` | Sobe os containers em background |
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
