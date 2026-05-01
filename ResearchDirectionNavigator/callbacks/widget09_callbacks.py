from dash import Input, Output, State, html, ALL, callback_context
from dash.exceptions import PreventUpdate

from components.widget09 import build_widget09_favorites_list, build_widget09_search_results
from utils.mysql import (
    w09_add_favorite_with_transaction as add_favorite,
    w09_list_favorites as list_favorites,
    w09_remove_favorite_with_transaction as remove_favorite,
    w09_search_faculty_by_name as search_faculty_by_name,
)

def register(app):
    @app.callback(
        Output("widget_09_search_results", "children"),
        Input("search_widget09_button", "n_clicks"),
        Input("global_search_input", "value"),
        State("search_widget09", "value"),
        prevent_initial_call=True,
    )
    # search professors 
    def widget09_search_candidates(_n_clicks, global_search_text, typed_name):
        # get the source information that triggers the callback
        triggered_input_source=callback_context.triggered[0]["prop_id"] if callback_context.triggered else ""
        # if it's triggered by global search
        if triggered_input_source.startswith("global_search_input"):
            # if no input in the global search
            if not (global_search_text or "").strip():
                return html.P(
                    "Type a name and click Explore to find candidates to favorite.",
                    className="text-muted small mb-0",
                )
            raise PreventUpdate
        # trim spaces among input text
        trimmed_faculty_name=(typed_name or "").strip()
        if not trimmed_faculty_name:
            return html.P(
                "Please type a name first, then click Explore.",
                className="text-muted small mb-0",
            )
        # match the professor's inforamtion based on input faculty name
        matching_faculty_rows=search_faculty_by_name(trimmed_faculty_name, limit=15)
        return build_widget09_search_results(matching_faculty_rows)

    @app.callback(
        Output("widget_09_favorites", "children"),
        Input({"type": "w9-add-fav", "index": ALL}, "n_clicks"),
        Input({"type": "w9-remove-fav", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    # add / remove favorite, then refresh list
    def widget09_mutate_favorites(add_clicks_list, remove_clicks_list):
        # get the specific button that triggered the callback
        triggered_id=getattr(callback_context, "triggered_id", None)
        if not isinstance(triggered_id, dict):
            raise PreventUpdate
        # get the button type and corresponding index from the clicked button
        button_type=triggered_id.get("type")
        faculty_index=triggered_id.get("index")
        # filter invalid index
        if faculty_index is None or int(faculty_index)==-999999:
            raise PreventUpdate
        # get all the clicks for future decision
        all_clicks=(add_clicks_list or [])+(remove_clicks_list or [])
        if not all_clicks or max(all_clicks)<1:
            raise PreventUpdate
        # get the current faculty id
        faculty_id=int(faculty_index)
        # if the clicked button is add button
        if button_type=="w9-add-fav":
            add_favorite(faculty_id)
        # if the clicked button is remove button
        elif button_type=="w9-remove-fav":
            remove_favorite(faculty_id)
        else:
            raise PreventUpdate
        # update the latest favorite list
        favorite_faculty_rows=list_favorites()
        return build_widget09_favorites_list(favorite_faculty_rows)
