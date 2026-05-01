from dash import Input, Output, State

from services.search_service import run_widget10_search

# w10 callbacks
def register(app):
    @app.callback(
        Output("widget_10_results", "children"),
        Input("global_search_button", "n_clicks"),
        Input("search_widget10_button", "n_clicks"),
        Input("global_search_input", "value"),
        State("search_widget10", "value"),
        prevent_initial_call=True,
    )
    # update W10 result area
    def widget10_update_global_scholar_works(_n_global, _n_w10, global_val, local_input_text):
        return run_widget10_search(global_val, local_input_text)
