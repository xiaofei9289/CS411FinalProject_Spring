from dash import Input, Output, State

from services.university_service import get_widget02_university_profile

# w2 callbacks
def register(app):
    @app.callback(
        Output("widget_02_results", "children"),
        Input("widget_02_view_profile_button", "n_clicks"),
        State("widget_02_university_dropdown", "value"),
        prevent_initial_call=True,
    )
    # show W2 university info
    def widget02_update_university_information(_n_clicks, selected_university):
        return get_widget02_university_profile(selected_university)
