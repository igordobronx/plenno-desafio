# 🕊️ Plenno — Agente de Membros

> Sistema de monitoramento pastoral que identifica membros inativos e gera alertas personalizados com IA.

---

## 📋 Sobre o Projeto

Igrejas precisam acompanhar membros que estão se afastando — sem aparecer nos cultos, sem dízimo há semanas. Este agente monitora esses dados e dispara mensagens automáticas com tom pastoral, personalizadas por tipo de inatividade, usando IA generativa.

---

## 🏗️ Arquitetura

```
plenno-agente/
├── api/
│   ├── main.py                  # FastAPI + lifespan + scheduler
│   ├── routers/
│   │   └── membros.py           # Endpoints REST
│   ├── models/
│   │   └── membro.py            # Schemas Pydantic
│   ├── database/
│   │   ├── db.py                # Engine, session, init_db
│   │   └── models.py            # ORM SQLAlchemy
│   ├── data/
│   │   ├── alertas.json         # arquivos gerados automaticamente
│   │   └── plenno.db            # onde fica armazenado o bd, gerado automaticamente  
│   ├── services/
│   │   └── membro_service.py    # Regras de negócio
│   └── utils/
│       └── json_handler.py      # Leitura/escrita alertas.json
├── automation/
│   ├── agente.py                # Script de automação com IA
│   └── scheduler.py             # Agendamento standalone
├── data/
│   └── alertas.json             # Gerado automaticamente
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/plenno-agente.git
cd plenno-agente
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com sua chave:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🚀 Como Rodar

### API

```bash
uvicorn api.main:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

### Script de automação (manual)

Com a API rodando, em outro terminal:

```bash
python -m automation.agente
```

O script vai:
1. Buscar todos os membros inativos via `/membros/inativos`
2. Gerar uma mensagem pastoral personalizada para cada um via IA
3. Salvar tudo em `data/alertas.json` com timestamp

### Agendamento automático (standalone)

```bash
python -m automation.scheduler
```

Roda todos os dias às **08:00** (America/Sao_Paulo) automaticamente.

> ℹ️ Se a API estiver rodando, o scheduler já sobe junto no `lifespan` do FastAPI — não precisa rodar os dois separados.

---

## 📡 Endpoints

### `POST /membros`

Cadastra um novo membro.

**Body:**
```json
{
  "nome": "Maria Silva",
  "telefone": "62999990000",
  "ultima_presenca": "2024-12-01",
  "ultimo_dizimo": "2024-11-15"
}
```

**Resposta `201`:**
```json
{
  "id": 1,
  "nome": "Maria Silva",
  "telefone": "62999990000",
  "ultima_presenca": "2024-12-01",
  "ultimo_dizimo": "2024-11-15"
}
```

---

### `GET /membros/inativos`

Retorna membros sem presença **ou** dízimo há mais de 30 dias.

**Resposta `200`:**
```json
[
  {
    "id": 1,
    "nome": "Maria Silva",
    "telefone": "62999990000",
    "ultima_presenca": "2024-12-01",
    "ultimo_dizimo": "2024-11-15",
    "dias_sem_presenca": 45,
    "dias_sem_dizimo": 61,
    "tipo_inatividade": "ambos"
  }
]
```

> O campo `tipo_inatividade` pode ser `"presenca"`, `"dizimo"` ou `"ambos"`.

---

### `POST /alerta`

Registra e simula o envio de alerta para um membro.

**Body:**
```json
{
  "membro_id": 1
}
```

**Resposta `201`:**
```json
{
  "membro_id": 1,
  "nome": "Maria Silva",
  "tipo_inatividade": "ambos",
  "timestamp": "2025-01-15"
}
```

> O alerta é registrado no banco **e** salvo em `data/alertas.json`.

---

## 🤖 Automação com IA

O agente gera mensagens diferentes de acordo com o tipo de inatividade do membro:

| Tipo | Comportamento da IA |
|------|---------------------|
| `presenca` | Tom de saudade e cuidado — pergunta se está tudo bem |
| `dizimo` | Foco em comunidade e participação — nunca menciona dinheiro diretamente |
| `ambos` | Prioriza o cuidado humano antes de qualquer outra coisa |

**Exemplo de saída em `alertas.json`:**

```json
[
  {
    "membro_id": 1,
    "nome": "Maria Silva",
    "telefone": "62999990000",
    "tipo_inatividade": "presenca",
    "mensagem": "Oi Maria, tudo bem com você? Faz um tempinho que não te vejo por aqui e quis mandar uma mensagem pra saber como está sendo essa fase. A nossa comunidade sente sua falta 🙏 Qualquer coisa que precisar, pode contar.",
    "timestamp": "2025-01-15T08:00:00.123456"
  }
]
```

---

## 🗂️ Dependências

```txt
fastapi
uvicorn
sqlalchemy
pydantic
httpx
apscheduler
python-dotenv
```

Instale tudo com:

```bash
pip install -r requirements.txt
```

---

## 🧪 Testando rapidamente

Crie um membro inativo de exemplo:

```bash
curl -X POST http://localhost:8000/membros \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Oliveira",
    "telefone": "62988880000",
    "ultima_presenca": "2024-10-01",
    "ultimo_dizimo": "2024-10-01"
  }'
```

Verifique os inativos:

```bash
curl http://localhost:8000/membros/inativos
```

Rode o agente:

```bash
python -m automation.agente
```

---

## 📄 Licença

MIT