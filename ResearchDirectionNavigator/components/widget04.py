from dash import html, dcc
import dash_bootstrap_components as dbc

from utils.common import to_int

# W4 hidden store + offcanvas
def create_layout_for_widget04():
    # create a store to save the currently selected professor
    selected_faculty_store=dcc.Store(id="widget04_selected_professor", data=None)
    # create an offcanvas panel that locates in the right side
    faculty_profile_offcanvas=dbc.Offcanvas(
        id="widget04_offcanvas",
        title="W4 · Faculty Profile",
        # keep it hiddened at first
        is_open=False,
        # slide out from the right when triggered
        placement="end",
        children=html.Div(
            id="widget04_profile_container",
            children=[
                html.Div(
                    id="widget04_profile_content",
                    children=[
                        html.P(
                            "Open a profile from an author name in W1, W6, W7, or W9.",
                            className="text-muted small",
                        ),
                    ],
                ),
            ],
        ),
    )

    return selected_faculty_store, faculty_profile_offcanvas

# build the W4 profile card
def build_widget04_profile_card(profile_data):
    # load the number of papers and citations from the profile data
    publication_count=to_int(profile_data.get("publication_count"), default=0)
    total_citations=to_int(profile_data.get("total_citations"), default=0)

    # get the keyword, collaborator, and representative paper lists
    keyword_rows=profile_data.get("top_keywords") or []
    collaborator_rows=profile_data.get("top_collaborators") or []
    representative_paper_rows=profile_data.get("representative_papers") or []

    # create a list to store the future badge
    keyword_badges=[]
    # iterate each keyword data
    for keyword_row in keyword_rows:
        # get the keyword text and remove the space
        keyword_name=(keyword_row.get("keyword_name") or "").strip()
        if not keyword_name:
            continue
        # create a badge for the keyword
        keyword_badges.append(
            dbc.Badge(
                keyword_name,
                color="primary",
                className="me-1 mb-1",
                pill=True,
            )
        )

    # if there are no keywords, show a placeholder
    if not keyword_badges:
        keyword_badges=[html.Span("—", className="text-muted small")]

    # create a list to store top collaborators
    collaborator_items=[]
    # iterate each data in the collaborator rows
    for collaborator_row in collaborator_rows:
        collaborator_name=(collaborator_row.get("collaborator_name") or "").strip()
        if not collaborator_name:
            continue
        # get the number of shared papers
        shared_paper_count=to_int(collaborator_row.get("shared_papers"), default=0)
        # add them into the list
        collaborator_items.append(
            html.Li(
                f"{collaborator_name} ({shared_paper_count} papers)",
                className="small",
            )
        )

    if collaborator_items:
        collaborator_block=html.Ul(collaborator_items, className="mb-0 ps-3")
    else:
        collaborator_block=html.P("—", className="text-muted small mb-0")

    # create a list to store the representative papers
    representative_paper_items=[]
    for paper_row in representative_paper_rows:
        paper_title=(paper_row.get("title") or "Untitled").strip()
        paper_year=paper_row.get("year")
        paper_citations=paper_row.get("num_citations")

        # convert the number of citations into integers
        paper_citation_count=to_int(paper_citations, default=0)

        # convert the year to display text
        if paper_year is None:
            paper_year_text="-"
        else:
            paper_year_text=str(paper_year)

        # put them into the list
        representative_paper_items.append(
            html.Li(
                f"{paper_title} ({paper_year_text}, cited {paper_citation_count})",
                className="small mb-1",
            )
        )

    # show representative papers as an ordered list 
    if representative_paper_items:
        representative_paper_block=html.Ol(
            representative_paper_items,
            className="mb-0 ps-3 small"
        )
    else:
        representative_paper_block=html.P("—", className="text-muted small mb-0")

    # create the profile card to display
    profile_card=dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(
                        profile_data.get("faculty_name") or "",
                        className="mb-2 text-primary"
                    ),
                    html.P(
                        profile_data.get("university_name") or "",
                        className="text-muted mb-3"
                    ),
                    html.Hr(className="my-2"),
                    html.P(
                        [html.Strong("Number of Publications: "), str(publication_count)],
                        className="mb-2",
                    ),
                    html.P(
                        [html.Strong("Number of Citations: "), str(total_citations)],
                        className="mb-3",
                    ),
                    html.H6("Top Keywords", className="mt-2 mb-2"),
                    html.Div(keyword_badges, className="d-flex flex-wrap"),
                    html.H6("Top Collaborators", className="mt-3 mb-2"),
                    collaborator_block,
                    html.H6("Representative Publications", className="mt-3 mb-2"),
                    representative_paper_block,
                ]
            ),
        ],
        className="shadow-sm border-primary",
        style={
            "backgroundColor": "#e8f4fc",
            "borderWidth": "1px",
        },
    )

    return profile_card
