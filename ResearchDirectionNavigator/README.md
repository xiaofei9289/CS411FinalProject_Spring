# Research Direction Navigator

A **Dash** research exploration dashboard that combines **MySQL**, **Neo4j**, **MongoDB**, and **OpenAlex** for course demos and local development.

## Features

| Area | Description |
|------|-------------|
| Global search | Top-bar keyword search wired to multiple widgets |
| W1 | Keyword publication search (MySQL) |
| W2 | University research profile and keyword bar chart (MySQL) |
| W3 | Multi-university comparison table (MySQL) |
| W4 | Faculty profile off-canvas panel (MySQL; linked from W1, W9, etc.) |
| W5 | Research trends: Neo4j interest overlap + MongoDB publications by year (MySQL + Neo4j + MongoDB) |
| W6–W8 | Recommendations, collaboration network, related keywords, etc. |
| W9 | Favorite professors (MySQL; transactions and constraints) |
| W10 | OpenAlex works search (optional `OPENALEX_MAILTO`) |

The page layout is defined in `layout/main_layout.py`. Widget UI lives under `components/`; orchestration is in `services/` and data access in `utils/`.

## Prerequisites

- **Python** 3.10+ (3.11 or 3.13 recommended)
- **MySQL** with the course schema (e.g. `academicworld`)
- **Neo4j** with password set (required for parts of W5 and related flows)
- **MongoDB** (W5 yearly trends, etc.)
- Optional: network access to **OpenAlex** for W10

## Quick start

### 1. Create and activate a virtual environment

```bash
cd ResearchDirectionNavigator
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the template and fill in your local credentials (**do not commit a real `.env`**):

```bash
cp .env.example .env
# Edit .env: set at least MYSQL_PASSWORD, NEO4J_PASSWORD, etc.
```

See `.env.example` for MySQL, MongoDB, Neo4j, and OpenAlex variables.

### 4. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:8050/** in your browser.

The app runs with Dash debug mode (`debug=True`) by default. Stop the server with `Ctrl+C` in the terminal.

## Project layout

```
ResearchDirectionNavigator/
├── app.py                 # Dash entrypoint
├── requirements.txt
├── .env.example           # Environment variable template
├── assets/                # Static files (e.g. style.css)
├── callbacks/             # Dash callback registration
├── components/            # UI widgets (widget01 … widget10)
├── layout/                # App shell and grid
├── services/              # Search, trends, favorites, etc.
└── utils/                 # DB and API helpers (mysql, neo4j, mongodb, openalex)
```

## Notes

- **Fresh layout on each load**: `app.layout` is a callable so the tree is rebuilt on every full page load. That keeps widgets such as W9 “My Favorites” in sync with the database after refresh.
- **Databases down**: Some widgets may error or show empty results if MySQL, Neo4j, or MongoDB is unreachable; verify services are running and `.env` is correct.
- **Neo4j**: If `NEO4J_PASSWORD` is unset, `utils/neo4j.py` raises a clear error when creating the driver.

## License and course use

Built for **CS411 Database Systems** coursework. Do not put production secrets or real deployment credentials in the repo.
