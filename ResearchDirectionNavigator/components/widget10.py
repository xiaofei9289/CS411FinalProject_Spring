from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.common import to_int

# build the W10 result table
def build_widget10_openalex_results(works, query, error=None):
    search_query_for_display=(query or "").strip() or "—"
    # if there is an error message,
    if error:
        return dbc.Alert(
            f"OpenAlex request failed: {error}",
            color="danger",
            className="mb-0 small",
        )
    # if the works list is empty
    if not works:
        return html.P(
            f'No OpenAlex works matched "{search_query_for_display}". Try a different keyword.',
            className="text-muted small mb-0",
        )
    # build the table header row
    table_header_row=html.Thead(
        html.Tr(
            [
                html.Th("Title"),
                html.Th("Year", style={"width": "72px"}),
                html.Th("Citations", style={"width": "88px"}),
                html.Th("Authors"),
            ]
        )
    )
    # create an empty list to store all table body rows
    table_body_rows=[]
    # iterate each work returned by OpenAlex
    for work in works:
        # get the title of the current work
        title=work.get("title")
        if not title:
            title="—"
        # get the URL of the current work
        url=work.get("url")
        if not url:
            url=""
        else:
            # remove extra spaces around the URL
            url=url.strip()

        if len(title)>200:
            shown_title=title[:200] + "…"
        else:
            shown_title=title

        # if the work has a valid URL, make the title clickable
        if url!="":
            title_cell=html.A(
                shown_title,
                href=url,
                target="_blank",
                rel="noopener noreferrer",
                className="text-decoration-none",
                style={"color": "#2C516E"},
            )
        else:
            title_cell=html.Span(shown_title)

        # get the publication year
        year=work.get("year")
        if year is None:
            year_text="—"
        else:
            year_text=str(year)

        # get the citation count
        citations=to_int(work.get("cited_by_count"), default=0)
        citation_text=str(citations)

        # get the short author text
        authors=work.get("authors_short")
        if not authors:
            authors="—"

        # build one table row for the current work
        one_row=html.Tr(
            [
                html.Td(title_cell, className="small"),
                html.Td(year_text, className="small text-nowrap"),
                html.Td(citation_text, className="small text-nowrap"),
                html.Td(authors, className="small text-muted"),
            ]
        )

        # add the current row into the body row list
        table_body_rows.append(one_row)

    # build the final Bootstrap table using the header and all body rows
    result_table=dbc.Table(
        [table_header_row, html.Tbody(table_body_rows)],
        bordered=True,
        hover=True,
        size="sm",
        responsive=True,
        className="mb-0",
    )

    # count how many works are in the current result list
    work_count=len(works)
    # return the whole result area
    return html.Div(
        [
            html.P(
                [
                    html.Strong("OpenAlex", className="text-secondary"),
                    f" — {work_count} works · query: ",
                    html.Span(
                        search_query_for_display,
                        className="fw-semibold",
                        style={"color": "#2C516E"},
                    ),
                ],
                className="small mb-2",
            ),
            result_table,
            html.P(
                "Data: OpenAlex (CC0). Links open the work page in a new tab.",
                className="text-muted small mt-2 mb-0",
            ),
        ]
    )

# W10 layout
def build_column_widget10(initial_children):
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "EXTERNAL DATA",
                        className="section-label section-label-pink",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-pink",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W10", className="widget-tag"),
                            html.Span(
                                "Global Scholarly Works",
                                className="widget-title",
                            ),
                            html.Span("OpenAlex", className="tech-badge neo4j"),
                            html.Span("External API", className="tech-badge mysql"),
                        ],
                    ),
                    html.P(
                        "Search the global scholarly graph beyond the local dataset.",
                        className="widget-subtitle",
                    ),
                    html.P(
                        "Examples: computer science, databases, attention mechanism...",
                        className="text-muted small mb-2",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus",
                        children=[
                            dcc.Input(
                                id="search_widget10",
                                type="text",
                                placeholder="e.g. topic, title, keywords, or author name",
                                className="form-control",
                                debounce=True,
                            ),
                            dbc.Button(
                                "OpenAlex Search",
                                id="search_widget10_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-pink",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_10_results",
                        children=initial_children,
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=4,
        className="py-2",
    )