from dash import ALL, Input, Output, State, callback_context, html
from dash.exceptions import PreventUpdate

from components.widget08 import build_widget08_favorites_list, build_widget08_search_results
from services.publication_favorite_service import (
    add_favorite_publication,
    list_favorite_publications,
    remove_favorite_publication,
    search_publications_for_favorites,
    update_favorite_publication,
)


def register(app):
    @app.callback(
        Output("widget_08_search_results", "children"),
        Input("search_widget08_button", "n_clicks"),
        State("search_widget08", "value"),
        prevent_initial_call=True,
    )
    def widget08_search_publications(_n_clicks, search_text):
        cleaned_text=(search_text or "").strip()
        if not cleaned_text:
            return html.P(
                "Please type a title or keyword first, then click Search.",
                className="text-muted small mb-0",
            )
        publication_rows=search_publications_for_favorites(cleaned_text, limit=10)
        return build_widget08_search_results(publication_rows)

    @app.callback(
        Output("widget_08_favorites", "children"),
        Input({"type": "w8-add-pub", "index": ALL}, "n_clicks"),
        Input({"type": "w8-remove-pub", "index": ALL}, "n_clicks"),
        Input({"type": "w8-update-pub", "index": ALL}, "n_clicks"),
        State({"type": "w8-note", "index": ALL}, "value"),
        State({"type": "w8-note", "index": ALL}, "id"),
        State({"type": "w8-status", "index": ALL}, "value"),
        State({"type": "w8-status", "index": ALL}, "id"),
        prevent_initial_call=True,
    )
    def widget08_mutate_favorites(
        add_clicks_list,
        remove_clicks_list,
        update_clicks_list,
        note_values,
        note_ids,
        status_values,
        status_ids,
    ):
        triggered_id=getattr(callback_context, "triggered_id", None)
        if not isinstance(triggered_id, dict):
            raise PreventUpdate
        button_type=triggered_id.get("type")
        publication_id=triggered_id.get("index")
        if publication_id in (None, "__placeholder__"):
            raise PreventUpdate
        all_clicks=(add_clicks_list or [])+(remove_clicks_list or [])+(update_clicks_list or [])
        numeric_clicks=[clicks or 0 for clicks in all_clicks]
        if not numeric_clicks or max(numeric_clicks) < 1:
            raise PreventUpdate

        if button_type=="w8-add-pub":
            add_favorite_publication(publication_id)
        elif button_type=="w8-remove-pub":
            remove_favorite_publication(publication_id)
        elif button_type=="w8-update-pub":
            note_value=get_value_for_pattern_index(note_values, note_ids, publication_id)
            status_value=get_value_for_pattern_index(status_values, status_ids, publication_id)
            update_favorite_publication(publication_id, status_value, note_value)
        else:
            raise PreventUpdate

        favorite_rows=list_favorite_publications()
        return build_widget08_favorites_list(favorite_rows)


def get_value_for_pattern_index(values, ids, target_index):
    for one_value, one_id in zip(values or [], ids or []):
        if isinstance(one_id, dict) and str(one_id.get("index"))==str(target_index):
            return one_value
    return None
