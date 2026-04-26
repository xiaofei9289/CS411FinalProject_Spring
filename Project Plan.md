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
- Interaction with Other Widgets：Clicking an author name opens Widget4 (Faculty Profile) in the side panel; a keyword chosen in Widget8 can auto-fill this search via the shared store


#### Widget2：University Research Profile

- Database：MySQL
- User Input：users can select a university from the drop-down menu, then click the view profile
- Output：after selecting a university, users can check the top keywords from a bar chart and get the information about the total publications, top conference areas, faculty, and trend insights on the four summary cards
- Interaction with Other Widgets：None

#### Widget3：University Comparison

- Database： MySQL 
- User Input： users can select at least two universities, then click button to compare the selected universities
- Output：users can get a grouped bar chart comparing faculty count, publication count, and citation totals across selected universities
- Interaction with Other Widgets： None

------

#### Widget4：Faculty Profile

- Database： Neo4j
- User Input： users can click a professor name from Widget1, Widget6, Widget7, or Widget9 to open
- Output：users can get the basic information about the selected professors, skill/keyword tags, representative publications, collaborators.
- Interaction with Other Widgets：this widget can be triggered from W1, W6, W7, W9; it can be displayed as an off-canvas side panel

------

#### Widget5：Research Trends

- Database： MongoDB
- User Input： users enter one or more comma-separated keywords and click Show Trend button
- Output： users can get line charts of publication counts over time per keyword 
- Interaction with Other Widgets： none

------

#### Widget6：Smart Faculty Recommendation

- Database： Neo4j + MySQL  + MongoDB 

- User Input： users first type the research topic keywords, then adjust weight sliders, finally get the recommended and sorted faculty
- Output：users can get the ranked table with professor, university, graph-relevance bar, total papers, and recent-activity sparkline
- Interaction with Other Widgets： users can click a professor name to open Widget4, and a keyword selected in Widget8 can also auto-fill the input field of this widget.

------

#### Widget7：Collaboration Network

- Database： Neo4j
- User Input： users type faculty name
- Output： users can get a network graph of co-authorship (nodes and edges) with a short legend
- Interaction with Other Widgets： users can click a node and then select that faculty for Widget4

------

#### Widget8：Favorite Publication Manager

- Database： MongoDB
- User Input： users can search publications by title or keyword, click the **+** button to save a publication, update the reading status/note for a saved publication, or click the **×** button to remove it from favorites.
- Output： users can view a saved publication list with title, year, venue, status, personal note, and edit/delete controls.
- Interaction with Other Widgets： this widget supports insert, delete, and modify operations on favorite publications; saved publication titles can guide users back to Widget1 keyword publication search.

------

#### Widget9：Favorite Professors Manager

- **Database:** MySQL
- **User Input:** users can search for faculty members, click the **+** button to add a professor to their favorites, or click the **×** button to remove a professor from the list.
- **Output:** users can view a **“My Favorites”** list with heart markers and delete controls.
- **Interaction with Other Widgets:** users can click a professor’s name in the list to open Widget4.

------

#### Widget10: Global Scholarly Works (OpenAlex)

- API： External API (OpenAlex Works API)
- User Input: users can enter a topic, title, or author-related query, then click Search OpenAlex.
- Output: users can view the top highly cited works, including title, authors, year, venue, citation count, and an optional DOI link.
- Interaction with Other Widgets: None.