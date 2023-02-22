from flask import Flask
from flask import request
import json
import sqlite3

app = Flask(__name__)

@app.route("/", methods=['GET'])
def indx():
    if request.method == 'GET':
        with sqlite3.connect("data.db") as con:
            #get uuid of the  max timestamp from lists
            classID = con.execute("SELECT classID FROM LISTS WHERE timestamp = (SELECT MAX(timestamp) FROM LISTS)").fetchone()[0]
            # get all the names and codes from the list WHERE classID = classID
            res = con.execute(f"SELECT name, code, timestamp FROM LISTS WHERE classID = '{classID}'").fetchall()
            return json.dumps(res)
if __name__ == "__main__":
    app.run(host='localhost', port='8080')