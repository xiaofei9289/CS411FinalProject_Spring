from dash import Input, Output, State

from services.trend_service import run_widget05_search

# w5 callbacks
def register(app):
    @app.callback(
        Output("widget_05_results", "children"),
        Input("global_search_button", "n_clicks"),
        Input("search_widget05_button", "n_clicks"),
        Input("global_search_input", "value"),
        State("search_widget05", "value"),
        prevent_initial_call=True,
    )
    # update W5 trend results
    def widget05_update_research_trend(_n_global, _n_w5, global_val, local_input_text):
        return run_widget05_search(global_val, local_input_text)
