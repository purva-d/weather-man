from flask import Flask, render_template

# importing sys
import sys
  
# adding Folder to the system path
sys.path.insert(0, 'E:\Python_VS\weather-man\db')
from db import MongoOperations as mongoOps
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getWeatherData/')
def getWeatherData():
    data = mongoOps.processData("Thane")
    return data

if __name__=="__main__":
    app.run(debug=True, port = 8000)