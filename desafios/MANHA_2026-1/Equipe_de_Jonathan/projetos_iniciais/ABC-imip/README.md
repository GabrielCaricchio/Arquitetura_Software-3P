# ABC-Imip

Sistema fullstack para auxiliar a **alfabetização de crianças hospitalizadas** no IMIP (Instituto de Medicina Integral Prof. Fernando Figueira).

O professor cadastra os pacientes/alunos, que realizam quizzes e atividades de alfabetização. Os resultados são analisados por **inteligência artificial**, que gera um feedback pedagógico sobre o aprendizado de cada criança para orientar o trabalho do professor.

#### Turma: 3°P de SI (manhã)
#### Professor: Cloves Rocha
#### Equipe:
- Jonathan Freitas
- Kauã Vinicius

---

## Objetivo

Oferecer uma plataforma digital acessível no ambiente hospitalar, permitindo que crianças internadas continuem seu processo de alfabetização de forma lúdica e acompanhada, mesmo fora da sala de aula tradicional.

---

## Tecnologias

| Camada         | Tecnologia                                      |
|----------------|-------------------------------------------------|
| Front-end      | React *(em desenvolvimento)*                    |
| Back-end       | Python 3.12 + Flask (API REST)                  |
| Banco de dados | SQLite                                          |
| ORM            | SQLAlchemy + Flask-Migrate                      |
| Comunicação    | JSON (troca de dados cliente ↔ servidor)        |
| Autenticação   | JWT (Flask-JWT-Extended)                        |
| IA             | Google Gemini 1.5 Flash                         |

---

## Funcionalidades

- **Cadastro e login** de usuários com perfis distintos (`professor` e `aluno`)
- **Registro de crianças/pacientes** pelo professor (perfil `aluno`)
- **Geração de desafios educativos** com apoio de IA (completar palavras)
- **Quizzes de alfabetização** com questões de letra faltante
- **Envio e correção automática** das respostas
- **Histórico de tentativas** e pontuação por aluno
- **Feedback por IA** com análise do desempenho e sugestões pedagógicas para o professor
- **Fallback local** quando a API do Gemini não estiver disponível

---

## Arquitetura do sistema

O projeto segue o **método em camadas**: Flask expõe uma API REST, SQLAlchemy persiste os dados em SQLite e o serviço de IA integra o modelo `gemini-1.5-flash` para gerar desafios e feedback pedagógico.

### Camadas

| Camada            | Responsabilidade                                              |
|-------------------|---------------------------------------------------------------|
| Apresentação      | Interface React — interação com professor e aluno               |
| Controle (rotas)  | Endpoints Flask — recebem e respondem requisições em JSON       |
| Serviços          | Regras de negócio — quizzes, correção e integração com a IA     |
| Persistência      | SQLAlchemy — modelos e acesso ao banco SQLite                   |
| Serviço externo   | Google Gemini 1.5 Flash — geração de desafios e feedback        |

```mermaid
flowchart TB
    subgraph apresentacao [Camada de Apresentação]
        React[React]
    end

    subgraph controle [Camada de Controle]
        Auth[/auth]
        Quiz[/quizzes]
        Test[/test]
    end

    subgraph servicos [Camada de Serviços]
        AIService[Serviço de IA]
    end

    subgraph persistencia [Camada de Persistência]
        ORM[SQLAlchemy ORM]
        DB[(SQLite)]
    end

    subgraph externo [Serviço Externo]
        Gemini[Gemini 1.5 Flash]
    end

    React -->|JSON| Auth
    React -->|JSON| Quiz
    Auth --> ORM
    Quiz --> ORM
    Quiz --> AIService
    Test --> AIService
    AIService --> Gemini
    ORM --> DB
```

---

## Estrutura do projeto

```
ABC-imip/
├── app/
│   ├── __init__.py          # Factory da aplicação Flask
│   ├── config.py            # Configurações (SQLite, JWT)
│   ├── models.py            # Modelos do banco de dados
│   ├── routes/
│   │   ├── auth.py          # Registro e login
│   │   ├── quizzes.py       # Geração e envio de quizzes
│   │   └── test_ai.py       # Rotas de teste da IA
│   └── services/
│       └── ai_service.py    # Integração com Gemini e fallback
├── migrations/              # Migrações do banco (Alembic)
├── run.py                   # Ponto de entrada do back-end
├── requirements.txt         # Dependências Python
└── README.md
```

---

## Modelo de dados

| Tabela      | Descrição                                              |
|-------------|--------------------------------------------------------|
| `users`     | Professores e alunos (nome, e-mail, senha, perfil)     |
| `quizzes`   | Quizzes de alfabetização (título, nível)               |
| `questions` | Questões de cada quiz (palavra incompleta, resposta)   |
| `attempts`  | Tentativas dos alunos (nota, vínculo com quiz)         |
| `answers`   | Respostas individuais de cada tentativa                |

---

## Pré-requisitos

- [Python](https://www.python.org/) 3.12+
- [Node.js](https://nodejs.org/) 18+ *(para o front-end React, quando disponível)*
- Chave de API do [Google AI Studio](https://aistudio.google.com/) (Gemini)

---

## Instalação

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd ABC-imip
```

### 2. Back-end (Flask)

**Criar e ativar o ambiente virtual:**

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

**Instalar dependências:**

```bash
pip install -r requirements.txt
```

**Configurar variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:

```env
JWT_SECRET_KEY=sua_chave_secreta_aqui
GEMINI_API_KEY=sua_chave_gemini_aqui
# Opcional — padrão: sqlite:///app.db
# DATABASE_URL=sqlite:///app.db
```

**Aplicar migrações do banco:**

```bash
# Windows (PowerShell)
$env:FLASK_APP = "run.py"
flask db upgrade

# Linux / macOS
export FLASK_APP=run.py
flask db upgrade
```

**Executar o servidor:**

```bash
python run.py
```

A API estará disponível em `http://localhost:5000`.

### 3. Testar a integração com a IA

Com o servidor em execução:

```bash
# Testa geração de feedback
curl http://localhost:5000/test/ai

# Testa geração de desafio
curl http://localhost:5000/test/challenge
```

---

## API REST

### Autenticação (`/auth`)

| Método | Rota              | Descrição                    |
|--------|-------------------|------------------------------|
| POST   | `/auth/register`  | Cadastro de usuário          |
| POST   | `/auth/login`     | Login (retorna token JWT)    |

**Exemplo de cadastro:**

```json
POST /auth/register
{
  "name": "Maria Silva",
  "email": "maria@email.com",
  "password": "senha123",
  "role": "aluno"
}
```

**Exemplo de login (resposta):**

```json
{
  "token": "<jwt>",
  "role": "aluno"
}
```

### Quizzes (`/quizzes`)

| Método | Rota                | Descrição                                      |
|--------|---------------------|------------------------------------------------|
| POST   | `/quizzes/generate` | Gerar quiz com desafios via Gemini             |
| POST   | `/quizzes/submit`   | Enviar respostas e receber feedback da IA      |

**Exemplo de geração de quiz:**

```json
POST /quizzes/generate
{
  "level": "iniciante",
  "quantity": 5
}
```

**Exemplo de resposta:**

```json
{
  "message": "Quiz gerado com sucesso",
  "quiz_id": 1,
  "title": "Quiz de alfabetização",
  "level": "iniciante",
  "questions": [
    {
      "word_with_missing": "c_sa",
      "correct_answer": "a"
    }
  ]
}
```

**Exemplo de envio de respostas:**

```json
POST /quizzes/submit
{
  "student_id": 1,
  "quiz_id": 1,
  "answers": [
    {
      "question_id": 1,
      "student_answer": "a"
    }
  ]
}
```

> A resposta do aluno deve ser a **letra faltante** da palavra (ex.: `"a"` para `"c_sa"`), não a palavra completa.

### Testes da IA (`/test`)

| Método | Rota              | Descrição                              |
|--------|-------------------|----------------------------------------|
| GET    | `/test/ai`        | Testa geração de feedback pedagógico   |
| GET    | `/test/challenge` | Testa geração de desafio educativo     |

---

## Fluxo de uso

1. O **professor** faz login e cadastra a criança/paciente como aluno (`role: "aluno"`).
2. Um **quiz** é gerado via `/quizzes/generate` (manualmente ou pelo front-end).
3. O **aluno** responde as questões e o sistema envia as respostas em `/quizzes/submit`.
4. O sistema **corrige automaticamente**, registra a pontuação e solicita **feedback da IA**.
5. O **professor** visualiza o feedback e acompanha a evolução do aprendizado.

---

## Dependências principais (back-end)

```
flask
flask-sqlalchemy
flask-migrate
flask-jwt-extended
flask-cors
google-generativeai
python-dotenv
```

---

## Licença

Projeto acadêmico desenvolvido no contexto da disciplina de Arquitetura de Software.