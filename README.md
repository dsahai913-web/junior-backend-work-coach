# Work Coach — A Practical Guide for Junior Developers

**Turning confusing development tasks into a clear starting point.**

Starting a development task is not always as simple as opening an editor and writing code.

For an intern or a junior developer, a task from Jira or a senior developer can involve unfamiliar concepts, files they have never seen before, or a codebase they do not fully understand yet. Sometimes, the hardest part is not writing the code — it is figuring out where to begin.

**Work Coach is a project I am building to help solve that problem.**

It allows a developer to enter a work task and receive AI-generated guidance that helps them understand the requirement, identify what they may need to learn, and plan their first steps before jumping into implementation.

The goal is not to have AI do the work for the developer. It is to help them approach the work with more clarity and become more independent over time.

## The problem I'm trying to solve

When you're new to a team, you might receive a task that sounds straightforward to an experienced developer but feels overwhelming when you're seeing the underlying concepts for the first time.

Questions quickly come up:

- What does this task actually require me to do?
- Which concepts or skills do I need to understand first?
- Where should I start looking in the codebase?
- How can I break the task into manageable steps?
- What should I check before considering the work complete?

Work Coach is designed around these questions. Instead of giving developers another generic chatbot, the idea is to provide task-focused guidance that they can use as a starting point for their actual development work.

## How it works

1. **Describe the task** — Enter a development task in your own words, such as a feature request, bug fix, or backend change.
2. **Understand the requirement** — Get an AI-generated explanation in simpler terms.
3. **Identify learning gaps** — See the concepts or skills that may be useful for completing the task.
4. **Plan the approach** — Use a structured breakdown to understand the steps involved and decide where to begin.
5. **Take ownership** — Use the guidance to investigate, implement, test, and understand the solution yourself.

The idea is to reduce the uncertainty at the beginning of a task, not to replace the developer's thinking.

## What I'm building

Work Coach is being developed as a full-stack application with a focus on backend engineering, authentication, database design, and practical AI integration.

The current project includes work on:

- **User authentication:** Registering and authenticating users using JWT-based authentication.
- **Task management:** Creating and managing development tasks associated with individual users.
- **AI-powered analysis:** Using Google's Gemini API to turn task descriptions into learning-oriented guidance.
- **Task ownership:** Ensuring users access their own tasks rather than another user's tasks.
- **Database persistence:** Storing application data in PostgreSQL through SQLAlchemy.
- **Database migrations:** Managing database schema changes with Alembic.
- **Frontend integration:** Connecting a browser-based interface to the FastAPI backend.
- **Reliable task creation:** Implementing idempotency support to help prevent duplicate task creation when a request is retried.

The exact feature set may evolve as I continue testing and improving the application.

## Technology stack

| Area | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database migrations | Alembic |
| Authentication | JWT |
| AI integration | Google Gemini API |
| Frontend | HTML, CSS, JavaScript |
| Configuration | Environment variables with `.env` for local development |
| Development tools | Git and GitHub |

## Why I chose this project

I wanted to build something beyond a basic CRUD application — something connected to a real challenge that developers face when entering the industry.

This project gives me an opportunity to work through problems that go beyond making an API return the correct response: authentication, user-specific data access, database consistency, API integration, error handling, and connecting a frontend to a backend.

It also gives me a practical way to explore how generative AI can support learning and problem-solving without removing the need to understand the code.

I'm building Work Coach as a learning project, so I expect the architecture and features to improve as I encounter new challenges and learn better ways to solve them.

## Running the project locally

### Prerequisites

- Python installed
- PostgreSQL installed and running, or access to a PostgreSQL database
- A Google Gemini API key
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd junior_backend
```

Replace the placeholder with your actual repository URL.

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root. Add the environment variable names expected by your application, using your own local credentials.

For example, your configuration may include:

```dotenv
DATABASE_URL=your_postgresql_connection_string
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_long_random_secret
```

These names are examples; match them to the variables your code actually reads. Never commit real API keys, passwords, or secret values to GitHub.

### 5. Set up the database

Create your PostgreSQL database, then apply the Alembic migrations if your project is configured to manage its schema through Alembic:

```bash
alembic upgrade head
```

### 6. Start the backend

```bash
uvicorn main:app --reload
```

The backend should be available at:

`http://127.0.0.1:8000`

FastAPI's interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

### 7. Open the frontend

Serve the `frontend` folder using your preferred local development server and configure the frontend API URL to point to the running backend.

For local development, this may be:

`http://127.0.0.1:5500`

Make sure the frontend's configured URL and the backend's CORS settings match your local setup.

## Current status

Work Coach is under active development. I'm building and testing its backend, AI analysis flow, authentication, database interactions, and frontend integration.

My focus is on making the application useful in a real development workflow: guidance should be understandable, task data should remain associated with the correct user, and the application should handle failures without losing the user's work.

## What's next

Areas I want to improve as the project develops include:

- More consistent, structured AI analysis.
- Better handling of AI API errors and slow responses.
- A smoother task-analysis experience on the frontend.
- More thorough testing of authentication, task ownership, and error cases.
- Deployment and configuration for a production environment.
- Clearer guidance that helps developers learn rather than simply copy a solution.

## A final note

I'm building Work Coach to explore a simple idea: **a junior developer should not need to know everything before they can make progress — they need a better way to figure out what to learn and what to do next.**

This project is my attempt to build that starting point while learning how to design, develop, and maintain a full-stack application.
