import time

from dash import Input, Output, ALL, callback_context
from dash.exceptions import PreventUpdate

from components.widget04 import build_widget04_profile_card
from services.faculty_service import build_widget04_profile_response

# define a register function to register all widget 04 callbacks to the Dash app
def register(app):
    @app.callback(
        Output("widget04_selected_professor", "data"),
        Input({"type": "w4-open-faculty", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    # define a function to store which faculty card was clicked so the profile panel knows whom to load
    def w1_put_faculty_id_in_store_for_widget04(_n_clicks_list):
        # if no callback triggerred, no update
        if not callback_context.triggered:
            raise PreventUpdate
        # get the clicked component ID from callback_context
        triggered_component_id=getattr(callback_context, "triggered_id", None)
        # if not a "w4-open-faculty" type component, no update
        if not isinstance(triggered_component_id, dict) or triggered_component_id.get("type") != "w4-open-faculty":
            raise PreventUpdate
        # get index (faculty ID) from the dict
        faculty_id=triggered_component_id.get("index")
        # filter those values that are not valid
        if faculty_id is None or int(faculty_id)==-999999:
            raise PreventUpdate
        # if no click happens
        if not _n_clicks_list:
            raise PreventUpdate
        if max(_n_clicks_list) < 1:
            raise PreventUpdate
        return {"faculty_id": int(faculty_id), "tick": time.time()}

    @app.callback(
        Output("widget04_profile_content", "children"),
        Output("widget04_offcanvas", "is_open"),
        Input("widget04_selected_professor", "data"),
        prevent_initial_call=True,
    )
    # define a function to open the off-canvas profile and fill it using the stored faculty id
    def widget04_open_from_store(store_data):
        response=build_widget04_profile_response(store_data, build_widget04_profile_card)
        if response is None:
            raise PreventUpdate
        return response
