from dash import html, dcc
import dash_bootstrap_components as dbc

# create a function to display widget 01 description
def get_widget01_initial_results_children():
    widge01_discription=html.P(
            "This area will display search results in a table: title, year, citations, venue, and authors."
        ),
    return widge01_discription

# define a function to builds the layout of Widget 01 in the dashboard
# the column for widget 1 is about the keywords and it accounts for half of the width of the page
def build_column_widget01():
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "PUBLICATION EXPLORATION",
                        className="section-label section-label-keyword",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-blue",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W1", className="widget-tag"),
                            html.Span(
                                "Keyword Publication Search",
                                className="widget-title",
                            ),
                            html.Span("MySQL", className="tech-badge mysql"),
                            html.Span("Index", className="tech-badge index"),
                        ],
                    ),
                    html.P(
                        "Search publications based on a research keyword.",
                        className="widget-subtitle",
                    ),
                    html.P(
                        "Examples: machine learning, data mining, robotics...",
                        className="text-muted small mb-2",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus w1-search-row",
                        children=[
                            dcc.Input(
                                id="search_widget01",
                                type="text",
                                placeholder="Enter keywords to search",
                                size="72",
                                className="form-control",
                                debounce=False,
                                style={
                                    "minWidth": "0",
                                    "boxSizing": "border-box",
                                },
                            ),
                            dbc.Button(
                                "Search",
                                id="search_widget01_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-blue",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_01_results",
                        children=get_widget01_initial_results_children(),
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=6,
        className="py-2",
    )


# create a function to convert the faculty ID and name strings into a row of clickable author buttons.
def authors_cell_for_one_paper(faculty_ids_joined, faculty_names_joined):
    # faculty_ids_joined / faculty_names_joined: one string per paper from MySQL (group_concat), pieces joined by "||".
    # split on "||" and strip; two parallel lists — same index means the same author.
    # check if is none
    if faculty_ids_joined is None:
        faculty_ids_joined=""
    if faculty_names_joined is None:
        faculty_names_joined=""
    # split  concatenated string by using "||"
    faculty_id_str_list=faculty_ids_joined.split("||")
    faculty_name_list=faculty_names_joined.split("||")

    # remove the empty value
    clean_id_list=[]
    for i in faculty_id_str_list:
        i=i.strip()
        if i != "":
            clean_id_list.append(i)
    clean_name_list=[]
    for i in faculty_name_list:
        clean_name_list.append(i.strip())

    # if no author
    if not faculty_id_str_list:
        return html.Span("(no linked faculty)", className="text-muted small")
    # create a button list
    button_list=[]

    # iterate each element in the clean_id_list
    for i in range(len(clean_id_list)):
        faculty_id_str=clean_id_list[i]

        # check if it is digit
        if not faculty_id_str.isdigit():
            continue
        faculty_id=int(faculty_id_str)

        # get the author name
        if i < len(clean_name_list):
            author_name=clean_name_list[i]
        else:
            author_name=f"Faculty {faculty_id}"

        # create the button
        button=dbc.Button(
            author_name,
            id={"type": "w4-open-faculty", "index": faculty_id},
            color="link",
            className="p-0 me-2",
            n_clicks=0
        )
        button_list.append(button)


    return html.Div(button_list, className="d-flex flex-wrap align-items-center")

# create a function to convert the query information into a table
def build_publication_list_for_widget01(publications):
    # if no publication found, return a message to explain
    if not publications:
        return html.Div("No publications found for this research direction.")
    # create a list for table rows
    table_rows=[]
    for single_publication in publications:
        paper_title=single_publication.get("title", "No Title")
        paper_year=single_publication.get("year", "—")
        paper_citation_count=single_publication.get("num_citations", "")
        paper_venue=single_publication.get("venue") or "—"
        faculty_ids_joined=single_publication.get("faculty_ids") or ""
        faculty_names_joined=single_publication.get("faculty_names") or ""

        # build the table row
        row=html.Tr([
            html.Td(paper_title),
            html.Td(str(paper_year)),
            html.Td(str(paper_citation_count)),
            html.Td(paper_venue),

            # clickable authors
            html.Td(
                authors_cell_for_one_paper(faculty_ids_joined, faculty_names_joined)
            )
        ])
        table_rows.append(row)
    # table header
    table_header=html.Thead(
        html.Tr(
            [
                html.Th("Title"),
                html.Th("Year"),
                html.Th("Citations"),
                html.Th("Venue"),
                html.Th("Authors"),
            ]
        )
    )
    # table body
    table_body=html.Tbody(table_rows)
    return html.Div(
        [
            html.H5("Search Results", className="mb-2"),
            dbc.Table(
                [table_header, table_body],
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
                className="mb-0 align-middle",
            ),
        ]
    )
