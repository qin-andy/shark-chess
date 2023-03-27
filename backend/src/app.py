import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='../../ui/build')

@app.route("/")
def hell_world():
  return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve(path):
  if path != "" and os.path.exists(app.static_folder + '/' + path):
      return send_from_directory(app.static_folder, path)