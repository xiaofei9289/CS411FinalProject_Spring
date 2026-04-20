# Research Direction Navigator

A **Dash** research exploration dashboard that combines **MySQL**, **Neo4j**, **MongoDB**, and **OpenAlex** for course demos and local development.

## Purpose

Research Direction Navigator helps undergraduate and graduate students explore possible PhD research directions. The target users are students who want to discover relevant publications, compare universities, inspect faculty profiles, observe topic trends, and save professors they may want to contact later.

The main scenario is exploratory academic planning: a user starts with a research keyword, reviews related papers and faculty, compares universities, checks broader topic trends, and keeps a short list of favorite professors.

## Demo

TODO: Add the Illinois Media Space video demo link here after recording the 5-10 minute project demo.

## Current features

| Area | Description |
|------|-------------|
| Global search | Top-bar keyword search wired to W1, W5, W9, and W10 |
| W1 | Keyword publication search (MySQL) |
| W2 | University research profile and keyword bar chart (MySQL) |
| W3 | Multi-university comparison table (MySQL) |
| W4 | Faculty profile off-canvas panel (MySQL; linked from W1, W9, etc.) |
| W5 | Research trends: Neo4j interest overlap + MongoDB publications by year (MySQL + Neo4j + MongoDB) |
| W9 | Favorite professors (MySQL; transactions and constraints) |
| W10 | OpenAlex works search with basic request-error handling (optional `OPENALEX_MAILTO`) |

## Placeholder widgets

W6, W7, and W8 are visible in the dashboard layout, but their callbacks and data-access functions are not implemented yet.

| Area | Current status |
|------|----------------|
| W6 | UI shell for smart faculty recommendation |
| W7 | UI shell for collaboration network |
| W8 | UI shell for related keywords explorer |

The page layout is defined in `layout/main_layout.py`. Widget UI lives under `components/`; orchestration is in `services/` and data access in `utils/`.

## Prerequisites

- **Python** 3.10+ (3.11 or 3.13 recommended)
- **MySQL** with the course schema (e.g. `academicworld`), required for initial page load and W1-W4/W9
- **Neo4j** with password set, required for W5 keyword-overlap results
- **MongoDB** with the course `publications` collection, required for W5 yearly trends
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

### 4. Prepare database helpers

Run the setup scripts that match your local databases before launching the dashboard:

```bash
# MySQL: run sql/mysql_setup.sql inside the academicworld database
# MongoDB: run sql/mongo_setup.js in the academicworld database
# Neo4j: run sql/neo4j_setup.cypher in the academicworld database
```

`sql/mysql_setup.sql` uses `DROP INDEX IF EXISTS`, which requires a MySQL version that supports that syntax.

### 5. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:8050/** in your browser.

The app runs with Dash debug mode (`debug=True`) by default. Stop the server with `Ctrl+C` in the terminal.

## Usage

1. Use the top global search box to search a research keyword across W1, W5, W9, and W10.
2. Use W1 to search local Academic World publications by keyword. Click a faculty name in the result table to open the W4 faculty profile side panel.
3. Use W2 to select one university and inspect its faculty count, publication count, major research area, and top keyword chart.
4. Use W3 to select at least two universities and compare publication count, faculty count, recent publication count, and citation total.
5. Use W5 to search a topic and view related keyword overlap from Neo4j together with yearly publication trends from MongoDB.
6. Use W9 to search faculty by name, add professors to My Favorites, remove them, and open their W4 profile from the favorites list.
7. Use W10 to search OpenAlex for external scholarly works related to a topic, title, keyword, or author.

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

## Design

The application follows a layered dashboard architecture:

| Layer | Files | Responsibility |
|------|-------|----------------|
| App entry | `app.py` | Creates the Dash app, sets the layout factory, and registers callbacks |
| Layout | `layout/main_layout.py` | Arranges widgets into dashboard rows and includes hidden stores/placeholders for pattern-matching callbacks |
| Components | `components/` | Builds the UI for each widget, including tables, cards, charts, forms, and the W4 off-canvas profile panel |
| Callbacks | `callbacks/` | Connects user actions to service functions and updates widget output areas |
| Services | `services/` | Coordinates widget-level business logic and converts database/API results into component data |
| Data access | `utils/` | Runs MySQL, MongoDB, Neo4j, and OpenAlex queries |
| Setup scripts | `sql/` | Creates indexes, views, constraints, and helper tables used by the dashboard |

The dashboard uses independent widgets arranged in a rectangular Bootstrap grid. Some widgets are connected through shared interactions: W1 and W9 can open W4 faculty profiles, and the global search input can drive multiple search widgets.

## Implementation

The frontend is implemented with Dash and Dash Bootstrap Components. Plotly is used for charts, including the W2 keyword bar chart and W5 trend/overlap visualizations. Static styling lives in `assets/style.css`.

The backend uses the provided Academic World data across three database systems:

- **MySQL** is used for publication search, university profiles, university comparison, faculty profiles, and favorite-professor updates.
- **Neo4j** is used in W5 to rank overlapping keywords connected to faculty nodes through graph relationships.
- **MongoDB** is used in W5 to aggregate publication counts by year from the `publications` collection.
- **OpenAlex** is used as an external data source for W10 to search global scholarly works beyond the local dataset.

The code is organized by widget where possible. `utils/mysql/w01.py`, `w02.py`, `w03.py`, `w04.py`, `w05.py`, and `w09.py` contain MySQL queries for the corresponding widgets. `utils/neo4j.py`, `utils/mongodb.py`, and `utils/openalex.py` contain graph, document, and external API access helpers.

## Database Techniques

The project uses several database techniques required by the course specification:

| Technique | Where | How it is used |
|-----------|-------|----------------|
| Indexing | `sql/mysql_setup.sql`, `sql/mongo_setup.js`, `sql/neo4j_setup.cypher` | Adds indexes for keyword names, publication years, join tables, MongoDB keyword/year fields, and Neo4j node lookups |
| View | `sql/mysql_setup.sql` | Creates `university_keyword_stats`, which supports W2 university keyword summaries |
| Constraint | `sql/mysql_setup.sql`, `sql/neo4j_setup.cypher` | Adds a unique constraint on favorite faculty, a foreign key from favorites to faculty, and Neo4j uniqueness constraints |
| Prepared statements | `utils/mysql/*.py` | Uses parameterized `%s` queries for user-provided input instead of string-concatenating values into SQL |
| Transaction | `utils/mysql/w09.py` | Adds/removes favorite professors and writes audit log rows in one MySQL transaction with commit, rollback, and cleanup |

The W9 transaction keeps `favorite_professors` and `favorite_log` consistent. When a user adds or removes a favorite professor, the dashboard mutates the current favorite list and writes a matching log row. If either SQL statement fails, the transaction rolls back so the database does not keep a partial favorite change.

## Notes

- **Fresh layout on each load**: `app.layout` is a callable so the tree is rebuilt on every full page load. That keeps widgets such as W9 “My Favorites” in sync with the database after refresh.
- **Initial MySQL dependency**: The layout loads university dropdown options and W9 favorites from MySQL. If MySQL is unreachable or `.env` is wrong, the page may fail during initial load.
- **Databases down**: W5 depends on MySQL, Neo4j, and MongoDB. If Neo4j or MongoDB is unreachable during W5 search, that callback may error or show no trend results.
- **Neo4j**: If `NEO4J_PASSWORD` is unset, `utils/neo4j.py` raises a clear error when creating the driver.
- **W6-W8**: These widgets are currently placeholders. Their buttons and result areas are present, but no callbacks are registered.
- **Local development**: `python app.py` runs Dash with `debug=True`.

## License and course use

Built for **CS411 Database Systems** coursework. Do not put production secrets or real deployment credentials in the repo.
