from threading import Thread
from time import sleep, monotonic
from routes import endpoint
from routes.endpoint import serverList as sL
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import (
    Flask
)

app = Flask(__name__)
app.register_blueprint(endpoint.bp)
app = ProxyFix(app, x_for=1, x_proto=1, x_host=1)

# TODO: Make more readable.
def routine():
    while True:
        sleep(6)
        for key, value in sL.copy().items():
            if monotonic() - value["keepAlive"] >= 15:
                sL.pop(key, None)

task = Thread(target=routine, daemon=True)
task.start()

if __name__ == "__main__":
    app.run(port=8000) # debug=true makes the thread run twice... not issue for production