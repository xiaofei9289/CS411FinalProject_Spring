from dash import Input, Output, callback_context
from dash.exceptions import PreventUpdate

from components.widget01 import get_widget01_initial_results_children
from services.search_service import (
    build_global_search_feedback_children,
    run_widget01_search,
)

# define a register function to register all widget 01 callbacks to the Dash app
def register(app):
    @app.callback(
        Output("widget_01_results", "children"),
        Input("global_search_button", "n_clicks"),
        Input("search_widget01_button", "n_clicks"),
        Input("search_widget01", "value"),
        Input("global_search_input", "value"),
        prevent_initial_call=True,
    )
    
    # define a function to update the publication results based on global or widget search input
    def widget01_update_publication_search(_n_global, _n_w1, w1_value, global_val):
        # get trigger source from callback_context.triggered
        triggered_list=callback_context.triggered
        if triggered_list:
            first_trigger=triggered_list[0]
            trigger_source=first_trigger["prop_id"]
        else:
            trigger_source=""
        # if triggered by global search: search with global keyword+Widget01 input
        if trigger_source.startswith("global_search_input"):
            return run_widget01_search(global_val, w1_value)
        # if only triggered by empty Widget01 input: reset results to initial state
        if trigger_source=="search_widget01.value":
            if not (w1_value or "").strip():
                return get_widget01_initial_results_children()
            raise PreventUpdate

        return run_widget01_search(global_val, w1_value)

    @app.callback(
        Output("global_search_feedback", "children"),
        Input("global_search_button", "n_clicks"),
        Input("global_search_input", "value"),
        prevent_initial_call=True,
    )

    # define a function to update global search feedback based on whether a keyword is entered
    def global_search_empty_hint(_n_explore, global_val):
        keyword=(global_val or "").strip()
        if not keyword:
            return ""
        return build_global_search_feedback_children(keyword)
