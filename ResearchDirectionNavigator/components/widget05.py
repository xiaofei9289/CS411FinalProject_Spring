from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.common import make_gradient_colors, parse_int, to_int

def get_valid_year(raw_year, min_year, max_year):
    year=parse_int(raw_year)
    if year is None:
        return None
    if year<min_year:
        return None
    if year>max_year:
        return None
    return year

def get_publication_count(pub_count):
    if pub_count is None:
        return 0
    result=parse_int(pub_count)
    if result is None:
        return None
    return result

def get_overlap_count(value):
    return to_int(value, default=0)

# remove bad year/count rows before drawing chart
def get_clean_year_count_list(yearly_data):
    min_year=1950
    max_year=2020
    clean_year_count_list=[]

    for row in yearly_data:
        raw_year=row.get("year")
        raw_pub_count=row.get("pub_count")

        year=get_valid_year(raw_year, min_year, max_year)
        if year is None:
            continue
        pub_count=get_publication_count(raw_pub_count)
        if pub_count is None:
            continue
        clean_year_count_list.append((year, pub_count))

    clean_year_count_list.sort()
    return clean_year_count_list

def split_year_and_count_lists(clean_year_count_list):
    year_list=[]
    publication_count_list=[]

    for year, pub_count in clean_year_count_list:
        year_list.append(year)
        publication_count_list.append(pub_count)
    return year_list, publication_count_list

def get_safe_text_for_display(text):
    cleaned_text=(text or "").strip()
    if cleaned_text=="":
        return "your search"
    return cleaned_text

# line chart for yearly publications
def build_publication_line_figure(year_list, publication_count_list, chart_title):
    line_chart_figure=px.line(
        x=year_list,
        y=publication_count_list,
        markers=True,
        labels={
            "x": "year",
            "y": "number of publications",
        },
    )
    line_chart_figure.update_traces(
        line=dict(color="#2C516E", width=3, shape="linear"),
        marker=dict(
            size=9,
            color="#2C516E",
            line=dict(width=1, color="#ffffff"),
        ),
    )
    max_publication_count=max(publication_count_list) if publication_count_list else 1
    if max_publication_count==0:
        max_publication_count=1
    line_chart_figure.update_layout(
        title=dict(
            text=chart_title,
            font=dict(color="#2C516E", size=16),
        ),
        xaxis_title="year",
        yaxis_title="number of publications",
        paper_bgcolor="#f5f6f8",
        plot_bgcolor="#f5f6f8",
        font=dict(color="#2C516E"),
        xaxis=dict(
            gridcolor="rgba(44, 81, 110, 0.12)",
            showgrid=True,
        ),
        yaxis=dict(
            range=[0, max_publication_count*1.12],
            gridcolor="rgba(44, 81, 110, 0.15)",
            zeroline=False,
        ),
        margin=dict(l=56, r=24, t=56, b=48),
        height=420,
        showlegend=False,
    )

    return line_chart_figure

# this part returns the chart shown in W5
def create_line_chart_for_w05_research_trend(yearly_data, keyword_label="", use_neo4j_keywords=True):
    if not yearly_data:
        return html.P(
            "No annual data found. Try broader keywords.",
            className="text-muted small",
        )
    display_keyword=get_safe_text_for_display(keyword_label)
    chart_title=f'Annual publications (MongoDB) — "{display_keyword}"'

    if not use_neo4j_keywords:
        chart_title+=" (no neo4j keywords)"
    clean_year_count_list=get_clean_year_count_list(yearly_data)

    if not clean_year_count_list:
        return html.P(
            "No annual data found. Try broader keywords.",
            className="text-muted small",
        )
    year_list, publication_count_list=split_year_and_count_lists(clean_year_count_list)

    line_chart_figure=build_publication_line_figure(
        year_list,
        publication_count_list,
        chart_title,
    )

    return dcc.Graph(
        figure=line_chart_figure,
        config={"displayModeBar": False},
        className="mb-1",
    )

# take only top rows for the bar chart
def get_overlap_chart_data(rows, max_rows=25):
    rows_to_show=rows[:max_rows]

    keyword_name_list=[]
    overlap_count_list=[]

    for row in rows_to_show:
        keyword_name=str(row.get("name") or "")

        if len(keyword_name)>32:
            keyword_name=keyword_name[:31] + "…"

        overlap_count=get_overlap_count(row.get("overlap"))

        keyword_name_list.append(keyword_name)
        overlap_count_list.append(overlap_count)

    return keyword_name_list, overlap_count_list

# bar chart for keyword overlap
def build_overlap_bar_figure(keyword_name_list, overlap_count_list):
    bar_color_list=make_gradient_colors(len(keyword_name_list))

    max_overlap_count=max(overlap_count_list) if overlap_count_list else 1
    if max_overlap_count==0:
        max_overlap_count=1

    bar_chart_figure=px.bar(
        x=keyword_name_list,
        y=overlap_count_list,
        labels={
            "x": "keywords",
            "y": "Number of Overlapping Teachers",
        },
    )

    bar_chart_figure.update_traces(
        marker_color=bar_color_list,
        marker_line_width=0,
    )

    bar_chart_figure.update_layout(
        title=dict(
            text="Top Interest Overlap Keywords (Neo4j)",
            font=dict(color="#2C516E", size=16),
        ),
        xaxis_title="keywords",
        yaxis_title="Number of Overlapping Teachers",
        paper_bgcolor="#f5f6f8",
        plot_bgcolor="#f5f6f8",
        font=dict(color="#2C516E"),
        xaxis=dict(
            tickangle=-45,
            automargin=True,
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            range=[0, max_overlap_count * 1.12],
            gridcolor="rgba(44, 81, 110, 0.15)",
            zeroline=False,
        ),
        margin=dict(l=52, r=20, t=52, b=160),
        height=380,
        showlegend=False,
    )

    return bar_chart_figure

def build_overlap_keywords_bar_chart(rows, max_rows=25):
    if not rows:
        return html.P(
            "No Neo4j interest keywords available for the listed teachers",
            className="text-muted small mb-0",
        )

    keyword_name_list, overlap_count_list=get_overlap_chart_data(rows, max_rows)

    bar_chart_figure=build_overlap_bar_figure(
        keyword_name_list,
        overlap_count_list,
    )

    overlap_bar_graph=dcc.Graph(
        figure=bar_chart_figure,
        config={"displayModeBar": False},
        className="mb-1",
    )

    has_hidden_rows=len(rows)>max_rows

    if not has_hidden_rows:
        return overlap_bar_graph

    return html.Div(
        [
            overlap_bar_graph,
            html.P(
                f"(Showing top {max_rows} keywords, sorted by overlapping teacher count, descending.)",
                className="text-muted small mt-1 mb-0",
            ),
        ]
    )

# put the two W5 charts together
def build_w05_panel(matched_faculty_count,neo4j_keyword_rows,mongo_line_chart,mongo_uses_neo4j_keywords):
    extra_note=None

    # Mongo has no exact data for Neo4j keywords, so use original search word
    if neo4j_keyword_rows and not mongo_uses_neo4j_keywords:
        extra_note=html.P(
            "Note: MongoDB did not match the Neo4j keyword set above; the line chart below falls back to your search term in MongoDB.",
            className="text-warning small mb-2",
        )

    elif not neo4j_keyword_rows:
        extra_note=html.P(
            "Note: With no Neo4j interest keywords, the line chart queries MongoDB using only the search term.",
            className="text-muted small mb-2",
        )

    return html.Div(
        [
            html.H6(
                "(1) Top keywords by overlapping faculty interest",
                className="mb-2 fw-semibold",
            ),
            html.P(
                f"MySQL: LIKE match on publication–keyword links for your input; {matched_faculty_count} faculty matched.",
                className="small mb-1",
            ),
            html.P(
                "Among these faculty, keywords are ranked by how many share that interest (highest first).",
                className="small mb-2",
            ),
            extra_note,
            build_overlap_keywords_bar_chart(neo4j_keyword_rows),
            html.H6(
                "(2) Annual publication counts (MongoDB)",
                className="mb-2 mt-4 fw-semibold",
            ),
            mongo_line_chart,
        ]
    )

# W5 card layout
def build_column_widget05(initial_children):
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "ANALYTICS",
                        className="section-label section-label-purple",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-purple",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W5", className="widget-tag"),
                            html.Span(
                                "Research Trends",
                                className="widget-title",
                            ),
                            html.Span("MySQL", className="tech-badge mysql"),
                            html.Span("Neo4j", className="tech-badge neo4j"),
                            html.Span("MongoDB", className="tech-badge mongo"),
                        ],
                    ),
                    html.P(
                        "Visualize publication trends over time.",
                        className="widget-subtitle",
                    ),
                    html.P(
                        "Examples: machine learning, data mining, human-computer interaction...",
                        className="text-muted small mb-2",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus",
                        children=[
                            dcc.Input(
                                id="search_widget05",
                                type="text",
                                placeholder="Enter keywords to search",
                                className="form-control",
                                debounce=True,
                            ),
                            dbc.Button(
                                "Show Trend",
                                id="search_widget05_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-purple",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_05_results",
                        children=initial_children,
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=5,
        className="py-2",
    )