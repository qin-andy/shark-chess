import json
import os
from flask import Flask, send_from_directory
from bson import json_util
from bots.bot_manager import BotManager
from flask_cors import CORS

from db.dao import RecordsDao

app = Flask(__name__, static_folder='../../ui/build')
CORS(app) # TODO : only for testing


# Singletons declared here (?)
bm = BotManager()
dao = RecordsDao(bm)

@app.route("/")
def hello_world():
  return send_from_directory(app.static_folder, 'index.html')

# Route to access tourney from db
@app.route("/tourney/<tourney_name>")
def get_tourney(tourney_name):
  tourney_json = dao.get_tourney_as_dict(tourney_name)

  # Error handle this
  if tourney_json == None:
    return 'Tourney not found: <' + str(tourney_name) + '>', 400
  
  return json.loads(json_util.dumps(tourney_json)), 200


@app.route('/<path:path>')
def serve(path):
  if path != "" and os.path.exists(app.static_folder + '/' + path):
      return send_from_directory(app.static_folder, path)