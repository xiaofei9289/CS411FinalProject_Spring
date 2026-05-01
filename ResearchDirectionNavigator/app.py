from dash import Dash
import dash_bootstrap_components as dbc

from callbacks import register_all_callbacks
from layout.main_layout import build_full_app_layout

def create_dash_app():
    dash_app=Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    dash_app.layout=build_full_app_layout
    register_all_callbacks(dash_app)
    return dash_app


dash_app=create_dash_app()
flask_server=dash_app.server

if __name__=="__main__":
    dash_app.run(debug=True)
