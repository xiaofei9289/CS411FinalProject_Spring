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

# register all widget callbacks here
def register_all_callbacks(app):
    register_widget01(app)
    register_widget02(app)
    register_widget03(app)
    register_widget04(app)
    register_widget05(app)
    register_widget06(app)
    register_widget07(app)
    register_widget08(app)
    register_widget09(app)
    register_widget10(app)
