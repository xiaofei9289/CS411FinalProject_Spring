## 1. Project Name

Research Direction Navigator

## 2. Target Users

Undergraduate and graduate students who are interested in pursuing a PhD and want to quickly gain an overview of research directions, relevant professors, and related publications.

## 3. Project Purpose

This project is designed to help users explore research directions, discover relevant faculty members and publications, compare universities, and identify potential academic paths through an interactive dashboard.

## 4. Widgets

#### Widget1：Keyword Publication Search

- Database：MySQL
- User Input：users can enter the keyword in a text box 
- Output：users can get a list of publications, including titles, authors, publication years, and venues
- Interaction with Other Widgets：Clicking an author name opens Widget4 (Faculty Profile) in the side panel; the top global search can also trigger the same W1 search flow


#### Widget2：University Research Profile

- Database：MySQL
- User Input：users can select a university from the drop-down menu, then click the view profile
- Output：after selecting a university, users can see one keyword bar chart and three summary cards: total publications, major research area, and number of faculty
- Interaction with Other Widgets：None

#### Widget3：University Comparison

- Database： MySQL 
- User Input： users can select at least two universities, then click button to compare the selected universities
- Output：users can get a comparison **table** of faculty count, publication count, recent publication count, and citation totals across selected universities (`components/widget03.py` uses an HTML table)
- Interaction with Other Widgets： None

------

#### Widget4：Faculty Profile

- Database： MySQL
- User Input： users can click a professor name from Widget1, Widget6, Widget7, or Widget9 to open the profile (no separate text box in W4)
- Output：users can get the selected faculty’s university, publication and citation totals, top keyword tags from their papers, representative publications, and top co-authors (collaborators on shared papers), loaded from the relational schema (`faculty`, `publication`, `keyword`, etc.).
- Interaction with Other Widgets：this widget can be triggered from W1, W6, W7, W9; it is shown as an off-canvas side panel on the right

------

#### Widget5：Research Trends

- Database： MySQL + Neo4j + MongoDB
- User Input： users enter a research keyword (and can use the top global search, which also drives W5) and run the trend search
- Output： (1) a bar chart of related keywords ranked by overlap with the faculty set that matches the query in Neo4j (after seed faculty ids are resolved in MySQL); (2) a line chart of publication counts over year from the MongoDB `publications` collection—for the Neo4j-derived keyword set when available, otherwise aggregated for the original search keyword alone
- Interaction with Other Widgets： none (can share the same keyword as the global search bar)

------

#### Widget6：Smart Faculty Recommendation

- Database： Neo4j + MySQL  + MongoDB 

- User Input： users first type the research topic keywords, then adjust weight sliders, finally get the recommended and sorted faculty
- Output：users can get a ranked table with faculty name, university, Neo4j relevance, keyword-relevant citations, recent publication count, and final score; the panel also shows MongoDB topic-activity context text
- Interaction with Other Widgets：users can click a faculty name in the W6 result table to open Widget4.

------

#### Widget7：Collaboration Network

- Database： Neo4j
- User Input： users type faculty name
- Output： users can get a co-authorship network graph and a collaborator list with shared-publication counts
- Interaction with Other Widgets： users can click faculty names in the collaborator list to open Widget4 (when the id can be mapped to MySQL).

------

#### Widget8：Favorite Publication Manager

- Database： MongoDB
- User Input： users can search publications by title or keyword, click the **+** button to save a publication, update the reading status/note for a saved publication, or click the **×** button to remove it from favorites.
- Output： users can view a saved publication list with title, year, venue, status, personal note, and edit/delete controls.
- Interaction with Other Widgets： this widget handles insert/delete/update on favorite publications inside W8; there is no direct auto-fill link to other widgets in the current code.

------

#### Widget9：Favorite Professors Manager

- **Database:** MySQL
- **User Input:** users can search for faculty members, click the **+** button to add a professor to their favorites, or click the **×** button to remove a professor from the list.
- **Output:** users can view a **“My Favorites”** list with faculty name, university, and remove controls.
- **Interaction with Other Widgets:** users can click a professor’s name in the list to open Widget4.

------

#### Widget10: Global Scholarly Works (OpenAlex)

- API： External API (OpenAlex Works API)
- User Input: users can enter a topic, title, or author-related query, then click Search OpenAlex.
- Output: users can view OpenAlex works in a table with title (link), year, citations, and authors.
- Interaction with Other Widgets: None for exclusive W10-only controls; the **top global search** can also populate the same query context used for OpenAlex (see `services/search_service.py`).

## 5. Extra-Credit

Per **CS411** project guidelines, we document up to **two** optional extra-credit capabilities (each may contribute up to **7.5%** of the final course grade, subject to staff review).

### Capability 1 — External data sourcing (OpenAlex / Widget 10)

- **What it is:** HTTP integration with the **OpenAlex Works API** so users can search beyond the local Academic World snapshot.
- **Why it is useful / cool:** Surfaces **live, worldwide** metadata and citation counts alongside on-prem MySQL / Neo4j / MongoDB widgets.
- **Why it is non-straightforward:** Client design for an external API (query shaping, parsing, optional polite `mailto`, failure paths) in `utils/openalex.py` and W10 callbacks, distinct from relational or Cypher query code.

### Capability 2 — Multi-database querying and orchestration (W5, W6, global search)

- **What it is:** **Chained pipelines** that use the **output of one database** as the basis for the next—e.g. W5 (MySQL faculty seed → Neo4j keyword overlap → MongoDB yearly trends with fallback), W6 (combined MySQL + Neo4j + MongoDB ranking), plus a **single global search** driving W1, W5, and W10.
- **Why it is useful / cool:** Delivers **end-to-end analytics** that no single datastore supports alone; aligns with how production systems federate relational, graph, and document stores.
- **Why it is non-straightforward:** ID alignment across engines, aggregation strategy when Neo4j and MongoDB keyword sets disagree, slider-weighted scoring in W6, and centralized keyword routing in `services/search_service.py` / related services.

## 6. Contributions

Fill in before submission (CS411 asks for **tasks** + **time** per member). Delete the second row if this was a **solo** project.

| Team member | Main tasks | Approx. time |
|-------------|------------|--------------|
| *[Name 1, NetID]* | *[e.g. W1–W5, MySQL/Neo4j scripts, layout, part of README]* | *[hours]* |
| *[Name 2, NetID]* | *[e.g. W6–W10, Mongo/OpenAlex, W9 transactions, demo video]* | *[hours]* |