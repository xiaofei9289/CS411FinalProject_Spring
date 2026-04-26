from callbacks.widget01_callbacks import register as register_widget01
from callbacks.widget02_callbacks import register as register_widget02
from callbacks.widget03_callbacks import register as register_widget03
from callbacks.widget04_callbacks import register as register_widget04
from callbacks.widget05_callbacks import register as register_widget05
from callbacks.widget06_callbacks import register as register_widget06
from callbacks.widget07_callbacks import register as register_widget07
from callbacks.widget08_callbacks import register as register_widget08
from callbacks.widget09_callbacks import register as register_widget09
from callbacks.widget10_callbacks import register as register_widget10

# this is the widget callback registration entrance
# it aggregates register(app) from all widget modules
# when the application starts, it provides register_all_callbacks(app) 
# to attach all Dash callbacks to the single app instance


CALLBACK_REGISTRARS=(
    register_widget01,
    register_widget02,
    register_widget03,
    register_widget04,
    register_widget05,
    register_widget06,
    register_widget07,
    register_widget08,
    register_widget09,
    register_widget10,
)

# define a function to ietrate every register in  CALLBACK_REGISTRARS
# and then execute register(app) for each registrar
def register_all_callbacks(app):
    for register_callback in CALLBACK_REGISTRARS:
        register_callback(app)
