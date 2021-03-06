from flask import Flask, request
import w2ecaller
import jsonpickle
import json
import logging


app = Flask(__name__)
JSON_HEADERS = {'content-type':'application/json'}

@app.route('/')
def mainpage():
    return "Health Data Broker is running..."



@app.route('/getalldata', methods=['GET'])
def getalldata():
    try:
        # Get credentials from request
        credentials = json.loads(str(request.headers["Authorization"]))
        logging.debug("Authorization credentials:" + str(credentials))
        # Get W2E credentials
        w2ecreds = credentials["W2E"]
        starttime = 0
        endtime = 0
        if 'starttime' in request.args:
            starttime = request.args['starttime']
        if 'endtime' in request.args:
            endtime = request.args['endtime']
        # Fetch W2E data
        datalist = w2ecaller.fetchAllW2EDataForUser(w2ecreds["username"],w2ecreds["apikey"], starttime, endtime)
        return json.dumps(datalist, sort_keys=True, indent=4, separators=(',', ': '))

    except Exception as e:
        if logging.getLogger().getEffectiveLevel() is not logging.DEBUG:
            return jsonpickle.encode(str(e)), 500
        else:
            raise e





