from dash import Input, Output, State

from services.university_service import get_widget03_comparison

def register(app):
    @app.callback(
        Output("widget_03_results", "children"),
        Input("search_widget03_button", "n_clicks"),
        State("widget_03_university_dropdown", "value"),
        prevent_initial_call=True,
    )
    # show W3 comparison table
    def widget03_update_university_comparision(n_clicks, selected_universities):
        return get_widget03_comparison(selected_universities)
