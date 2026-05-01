from dash import html, dcc
import dash_bootstrap_components as dbc

# first hint shown in W1
def get_widget01_initial_results_children():
    widge01_discription=html.P(
            "This area will display search results in a table: title, year, citations, venue, and authors."
        )
    return widge01_discription

# W1 column layout
def build_column_widget01():
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "PUBLICATION EXPLORATION",
                        className="section-label section-label-blue",
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


# build row of author buttons
def authors_cell_for_one_paper(faculty_ids_joined, faculty_names_joined):
    # handle None inputs first.
    if faculty_ids_joined is None:
        faculty_ids_joined=""
    if faculty_names_joined is None:
        faculty_names_joined=""

    # split raw strings into two lists.
    raw_id_list=faculty_ids_joined.split("||")
    raw_name_list=faculty_names_joined.split("||")

    # build a clean author list.
    valid_author_list=[]
    for i in range(len(raw_id_list)):
        one_id_text=raw_id_list[i].strip()

        # skip empty or invalid ids.
        if one_id_text=="":
            continue
        if not one_id_text.isdigit():
            continue

        one_faculty_id=int(one_id_text)

        # read name from the same position.
        if i<len(raw_name_list):
            one_author_name=raw_name_list[i].strip()
        else:
            one_author_name=""

        # use fallback name when the name is empty.
        if one_author_name=="":
            one_author_name=f"Faculty {one_faculty_id}"

        valid_author_list.append(
            {
                "faculty_id": one_faculty_id,
                "author_name": one_author_name,
            }
        )

    # show placeholder when no valid author exists.
    if len(valid_author_list)==0:
        return html.Span("(no linked faculty)", className="text-muted small")

    # build author buttons.
    button_list=[]
    for one_author in valid_author_list:
        one_button=dbc.Button(
            one_author["author_name"],
            id={"type": "w4-open-faculty", "index": one_author["faculty_id"]},
            color="link",
            className="p-0 me-2",
            n_clicks=0,
        )
        button_list.append(one_button)

    return html.Div(button_list, className="d-flex flex-wrap align-items-center")

# build the W1 publication table
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
