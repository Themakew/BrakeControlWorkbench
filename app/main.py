from application import app
from application import celery
from application import bcontrol
import views
import memcache


if __name__ == '__main__':
    client = memcache.Client([('127.0.0.1', 11211)])
    client.set("isTesting", False)
    client.set("isBreaking", False)
    client.set("cycles", 0)
    client.set("current_cycle", 0)

    bcontrol.turn_off_all()
    app.run('0.0.0.0', port=5000, debug=True)
