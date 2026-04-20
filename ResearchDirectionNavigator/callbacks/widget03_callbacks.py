from dash import Input, Output, State

from services.university_service import get_widget03_comparison

# define a register function to register all widget 03 callbacks to the Dash app
def register(app):
    @app.callback(
        Output("widget_03_results", "children"),
        Input("search_widget03_button", "n_clicks"),
        State("widget_03_university_dropdown", "value"),
        prevent_initial_call=True,
    )
    # define a function to build side-by-side university comparison UI from the dropdown selection
    def widget03_update_university_comparision(n_clicks, selected_universities):
        return get_widget03_comparison(selected_universities)
