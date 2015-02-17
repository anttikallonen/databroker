import requests, json, arrow
from pytz import timezone
from collections import defaultdict
import numpy as np


def convertUnifiedToTimeSeries(unifiedjson):
    samples = defaultdict(list)
    for item in unifiedjson:
        if len(item) > 0 :
            currentItem = item[0]
            measurementDateRaw = currentItem.pop("date", None)
            measurementTz = timezone(currentItem.pop("timezone", None))
            measurementDate = arrow.get(measurementDateRaw, tzinfo=measurementTz)
            for key, val in currentItem.items():
                samples[key].append({"timestamp" : measurementDate.timestamp,
                                     "value" : val})
    return samples


def getW2EUnifiedData(username,apikey,starttime,endtime,source,datatype):
    baseurl = "https://w2e.fi/api/"
    userurl = "users/" + username +"/"
    dataurl = "data/unify/" + source + "/" + datatype + "/"

    # Do date calculations
    tstart = arrow.get(starttime)
    tend = arrow.get(endtime)
    daysbetween = (tstart-tend).days
    dateurl = str(tstart.year) + "/" + str(tstart.month) + "/" + str(tstart.day) + "/days/" + str(daysbetween)

    requesturl = baseurl + userurl + dataurl + dateurl
    print(requesturl)

    # Make the request
    headers = {'Authorization' : 'Bearer ' + apikey}
    r = requests.get(requesturl, headers=headers)
    jsondata = r.json()

    return convertUnifiedToTimeSeries(jsondata)

def samplesToArray(samples):
    dataarray = []
    for sampleitem in samples:
        dataarray.append(sampleitem["value"])
    return dataarray

def createGuiDataFrame(label,minvalue,maxvalue,units,samples):
    return {"label" : label, "min" : minvalue, "max" : maxvalue, "units" : units, "samples" : samples}

def readConfigFile(filename):
    json_data=open(filename)
    data = json.load(json_data)
    json_data.close()
    return data

def fetchAllW2EDataForUser(username, apikey, starttime, endtime):
    configdata = readConfigFile("w2econfig.json")
    datalist = list()
    for key, datalabels in configdata.items():
        sourcedata = key.split(":")
        source = sourcedata[0]
        datatype = sourcedata[1]
        # Request samples
        samples = getW2EUnifiedData(username, apikey, starttime, endtime, source, datatype)
        for key, samplevalues in samples.items():
            samplearray = samplesToArray(samplevalues)
            guidata = createGuiDataFrame(datalabels[key]["label"], np.min(samplearray).item(), np.max(samplearray).item(), datalabels[key]["units"], samplevalues)
            datalist.append(guidata)
    return datalist






