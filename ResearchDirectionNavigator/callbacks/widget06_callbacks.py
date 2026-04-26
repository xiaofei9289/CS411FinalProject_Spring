from dash import Input, Output, State, html

from components.widget06 import build_widget06_recommendation_results
from services.recommendation_service import run_widget06_recommendation


def register(app):
    @app.callback(
        Output("widget_06_results", "children"),
        Input("search_widget06_button", "n_clicks"),
        State("search_widget06", "value"),
        State("widget06_graph_weight", "value"),
        State("widget06_citation_weight", "value"),
        State("widget06_recent_weight", "value"),
        prevent_initial_call=True,
    )
    def widget06_update_recommendations(
        _n_clicks,
        topic_text,
        graph_weight,
        citation_weight,
        recent_weight,
    ):
        if not (topic_text or "").strip():
            return html.P(
                "Please type a research topic first, then click Recommend.",
                className="text-muted small mb-0",
            )
        recommendation_payload=run_widget06_recommendation(
            topic_text,
            graph_weight,
            recent_weight,
            citation_weight,
        )
        return build_widget06_recommendation_results(recommendation_payload)
