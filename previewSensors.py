from flask import Flask, render_template, jsonify
import random    

from core.regulator import AverageFilter



mockData = True


sa = None
if not mockData:
    from core.sensorArray import SensorArray
    sa = SensorArray()

def readSensorArray(mockData = False):
    i = 3 #Posun senzorů vpravo
    for x in range(12):
        if mockData:
            val = random.randint(0, 1250)
        else:
            val = sa.sensors[x].value
        if val < 0:
            val = 8000
        data[i].filter(val)
        i += 1
        if i >= 12:
            i = 0
    sensorData = []
    for a in data:
        sensorData.append(int(a.getAverage()))

    return sensorData



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/sensors')
def sensors ():
    return render_template('sensors.html')

@app.route('/updateSensors')
def update():
    sensorArray = readSensorArray(mockData=mockData)
    telemetry = {"height": 0, "battery": 0, "time": 0, "speed": 0, "state": "Offline"}
    toSend = {"telemetry": telemetry, "sensorArray": sensorArray}
    return jsonify(toSend)



if __name__ == '__main__':
    data = []
    for i in range(12):
        data.append(AverageFilter(size = 5))
    app.run(host='0.0.0.0', port=80)