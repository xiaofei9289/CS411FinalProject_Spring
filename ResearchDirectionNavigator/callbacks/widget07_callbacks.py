from dash import Input, Output, State, html

from components.widget07 import build_widget07_network_results
from utils.neo4j import w07_neo4j_collaboration_network


def register(app):
    @app.callback(
        Output("widget_07_results", "children"),
        Input("search_widget07_button", "n_clicks"),
        State("search_widget07", "value"),
        prevent_initial_call=True,
    )
    def widget07_update_collaboration_network(_n_clicks, faculty_name):
        if not (faculty_name or "").strip():
            return html.P(
                "Please type a faculty name first, then click Show Network.",
                className="text-muted small mb-0",
            )
        network_payload=w07_neo4j_collaboration_network(faculty_name, limit=12)
        return build_widget07_network_results(network_payload)
