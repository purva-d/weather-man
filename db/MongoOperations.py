from flask.json import jsonify
import requests
import json
import datetime
def getDataFromApi():
    apikey=""
    city="London"
    url="https://api.openweathermap.org/data/2.5/onecall?lat=33.44&lon=-94.04&exclude=hourly,minutely,alerts&appid="+apikey
    #"api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+apikey

    response = requests.get(url)
    if (response.status_code == 200): 
        print("The request was a success!")
        response_dict = json.loads(response.text)
        daily=response_dict['daily']
        wdata=dict()
        for obj in daily:
            curDate = int(obj['dt'])*1000
            print(obj['dt'],"--------------------",curDate)
            wdata.update({curDate: obj['temp']['day']})
        return wdata
        
        # Code here will only run if the request is successful
    elif (response.status_code == 404):
        print("Result not found!")

from pymongo import MongoClient
username = "ebzAdmin"
password = "ebzAdminUser10110"
ipaddress= "localhost"
port = 27017
database_name = "weather"
books_collection = "books"
'''
def extractData():
    with open('db/weather.json') as f:
        weather_data = json.load(f)
        daily=weather_data['daily']
        data = dict()
        for obj in daily:
            #curDate = unixToDate(obj['dt'])
            curDate = int(obj['dt'])*1000
            data.update({curDate: obj['temp']['day']})
        return data
'''
def unixToDate(posix_time):
    return ((datetime.datetime.fromtimestamp(posix_time)).strftime('%d/%m/%Y'))

def uploadToMongo(data,city):         
    with open('db/dbconfig.json') as f:
        db_settings = json.load(f)
    client = MongoClient("mongodb://"+db_settings['username']+":"+db_settings['password']+"@"+db_settings['host']+":"+str(db_settings['port'])+"/"+db_settings['database']) 
    if (client == None):
        print("No connection")
    else:
        print("Connection success")
        db = client[db_settings['database']]
        for date, temperature in data.items():
            insertData = {
                "City": city,
                "Date": date,
                "Temp":temperature
            }
            prod_id = db.temperatureCollection.insert_one(insertData)
            #print(date, ":", temperature)

def retrieveFromDb(city):
    with open('db/dbconfig.json') as f:
        db_settings = json.load(f)
    client = MongoClient("mongodb://"+db_settings['username']+":"+db_settings['password']+"@"+db_settings['host']+":"+str(db_settings['port'])+"/"+db_settings['database']) 
    if (client == None):
        print("No connection")
    else:
        print("Connection success extract")
        db = client[db_settings['database']]
        results = db.temperatureCollection.find({"City":city})
        #results = json.dumps(result)
        returnRe = dict()
        tempData = dict()
        for obj in results:
            tempData.update({obj['Date']:obj['Temp']})
            #returnRes.update(tempData) 
        for key,val in tempData.items():
            print(key,"  ",val)
        return tempData

def processData(city):
    apidata=getDataFromApi()
    uploadToMongo(apidata,city)
    resdata = retrieveFromDb(city)
    return resdata
#getDataFromApi()