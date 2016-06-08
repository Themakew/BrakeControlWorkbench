from application import app
from application import celery
import views


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
