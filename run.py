# run.py
from app import app
from config.config import HOST, PORT
from threading import Thread
from app import routes


app.run(host=HOST, port=PORT, debug=True)
