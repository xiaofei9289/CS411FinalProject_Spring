# Research Direction Navigator

This project is our CS411 final project. It is a Dash web app. The app supports searches for research papers, professors, universities, research topics.

The project uses MySQL, MongoDB, Neo4j, OpenAlex. The main goal is simple. We hope this app help students explore possible research directions. We also hope to help students find professors of interest under the assistance of this Web App.

## 1. Demo

Demo Link:

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

## Team work

Fill this before submission:

| Team member | NetID | Work done | Email |
|-------------|-----------|------|------|
| Xiaofei Feng | xfeng18 | We shared the work evenly | xfeng18@illinois.edu |
| Yuxin Zhang | yuxinz17 | We shared the work evenly | yuxinz17@Illinois.edu |

## Notes

- MySQL should be running before opening the app.
- MongoDB setup is required for some widgets.
- Neo4j setup is required for some widgets.
- OpenAlex search problems usually come from internet connection issues.
- The app runs in debug mode. This project is a course project.

## Course

This project was built for 2026 Spring CS411 Database Systems.
