from dash import Input, Output, State

from services.university_service import get_widget02_university_profile

# define a register function to register all widget 02 callbacks to the Dash app
def register(app):
    @app.callback(
        Output("widget_02_results", "children"),
        Input("widget_02_view_profile_button", "n_clicks"),
        State("widget_02_university_dropdown", "value"),
        prevent_initial_call=True,
    )
    # define a function to generate school profile UI based on the selected university
    def widget02_update_university_information(_n_clicks, selected_university):
        return get_widget02_university_profile(selected_university)
