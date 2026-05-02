# Research Direction Navigator

This project is our CS411 final project. It is a Dash web app. The app supports searches for research papers, professors, universities, research topics.

The project uses MySQL, MongoDB, Neo4j, OpenAlex. The main goal is simple. We hope this app help students explore possible research directions. We also hope to help students find professors of interest under the assistance of this Web App.

## 1. Demo

Video demo (YouTube): [https://www.youtube.com/watch?v=0rfqCjRhDj0](https://www.youtube.com/watch?v=0rfqCjRhDj0)

## Design

We try to keep the structure simple. We did not put everything in one huge file. Split into folders so when bug happen we know where to look.

The front end is **Dash**. Run **`app.py`** then you get the website. **`layout/`** control how widgets placed on page. **`components/`** is each widget UI. **`callbacks/`** is when user click button or type text, Python code run.

Some widgets need **several databases together** (example W5 W6). Those messy logic we put in **`services/`**. Usually MySQL first, then Neo4j or Mongo, one by one.

**`utils/`** is only “how to ask database a question”. MySQL we write SQL with `%s`. Mongo we use pymongo. Neo4j we write Cypher. OpenAlex we just send HTTP request. Secret password we put in `.env`, please copy `.env.example` first.

Very rough picture: user do something → callback run → maybe **`services/`** → **`utils/`** → database answer → show table or chart on screen.

Top bar has **global search**. One keyword can update several panels together. Each widget still has own box so you can use separate.

We use **`dash-bootstrap-components`** make layout not ugly. **`assets/style.css`** change color spacing little bit.

## Implementation

Whole project write in **Python**. Web dashboard use **Plotly Dash**. Grid and button style use **Dash Bootstrap Components**. Figure use **Plotly**. Page skin we DIY in **`assets/style.css`**.

How connect backend:

- **MySQL**: Python package **`mysql-connector-python`**. SQL string use **`%s`** same style like MP homework.
- **MongoDB**: **`pymongo`**. Read trend data from collection. Widget 8 favorite paper also save here (insert update delete).
- **Neo4j**: official Neo4j driver for Python. We send Cypher as plain text string.

Config file use **`python-dotenv`**. Read `.env` at runtime. Real password never push to GitHub.

Widget 10 **OpenAlex**: we no use fancy SDK. **`urllib.request`** call API enough. JSON parse use Python built-in. Code live in **`utils/openalex.py`**.

If you lost where is code: open **`app.py`** first. **`layout/`** **`components/`** is face. **`callbacks/`** is hook. **`services/`** is combine multi DB. **`utils/`** is low level driver stuff.

## 2. What this app can do

The app includes a global search box at the top.

- W1: search papers by keyword

- W2: show university research information
- W3: compare several universities
- W4: show faculty profile
- W5: show research trend by year
- W6: recommend faculty by topic
- W7: show collaboration network
- W8: save favorite publications
- W9: save favorite professors
- W10: search papers from OpenAlex

## 3. How to run

First go into this folder:

```bash
cd ResearchDirectionNavigator
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Copy the env example:

```bash
cp .env.example .env
```

Then edit `.env` and put your own MySQL, MongoDB, and Neo4j settings.

Before running the app, run the setup files if needed:

```bash
# MySQL
database_setup/mysql_setup.sql

# MongoDB
database_setup/mongo_setup.js

# Neo4j
database_setup/neo4j_setup.cypher
```

Run the app:

```bash
python app.py
```

Then open this in the browser:

```text
http://127.0.0.1:8050/
```

## 4. All the files

```text
ResearchDirectionNavigator/
  app.py
  requirements.txt
  .env.example
  assets/
  callbacks/
  components/
  layout/
  services/
  utils/
  database_setup/
```

Some folders:

- `components/`: contains the UI code for each widget.
- `callbacks/`:  contains Dash callback code.
- `layout/`: contains the main page layout.
- `services/`: contains helper code between callbacks and database code.
- `utils/`: contains database code. It also contains API code.
- `assets/style.css`: controls the page style.
- `database_setup/`: contains setup files for MySQL, MongoDB, Neo4j.

## 5. Databases we used

- MySQL is used for normal table queries. These queries include papers, faculty, universities, favorite professors.
- MongoDB is used for publication trend data. It is also used for favorite publications.
- Neo4j is used for keyword-faculty relationships. It is also used for the collaboration graph.
- OpenAlex is used for extra paper search from online data.

## 6. Database features

The project uses several database features for the course requirement, including:

- Indexes are included in MySQL setup files.
- Indexes are included in MongoDB setup files.
- Indexes are included in Neo4j setup files.
- A MySQL view is used for university keyword statistics.
- Constraints are used for favorite records.
- Constraints are used for Neo4j nodes.
- Prepared SQL queries use `%s`.
- A transaction is used in W9 for favorite professor add actions.
- A transaction is used in W9 for favorite professor remove actions.
- MongoDB supports insert actions for favorite publications.
- MongoDB supports delete actions for favorite publications.
- MongoDB supports update actions for favorite publications.

## Extra parts

The project includes two extra parts.

1. OpenAlex search in W10. It can search papers outside the local database.
2. Some widgets use more than one database. For example, W5 uses MySQL, Neo4j, and MongoDB together.

## Contributions

CS411 asks for **tasks** and **approximate time** per member. Adjust hours if you track them differently.

| Team member | NetID | Main tasks | Approx. time | Email |
|-------------|-------|------------|--------------|-------|
| Xiaofei Feng | xfeng18 | Widgets **W1–W5** | ~30 h | xfeng18@illinois.edu |
| Yuxin Zhang | yuxinz17 | Widgets **W6–W10** | ~30 h | yuxinz17@Illinois.edu |

## Notes

- MySQL should be running before opening the app.
- MongoDB setup is required for some widgets.
- Neo4j setup is required for some widgets.
- OpenAlex search problems usually come from internet connection issues.
- The app runs in debug mode. This project is a course project.

## Course

This project was built for 2026 Spring CS411 Database Systems.
