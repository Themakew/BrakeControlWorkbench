from application import app
from application import celery
from application import bcontrol
import views


if __name__ == '__main__':
    bcontrol.turn_off_all()
    app.run('0.0.0.0', port=5000, debug=True)
