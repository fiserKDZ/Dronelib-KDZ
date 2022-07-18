from flask import Flask, render_template, jsonify
    
from core.sensorArray import SensorArray
from core.regulator import AverageFilter



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#Accept get request from the user

@app.route('/update')
def update():
    
    sa.read()
    i = 3
    for x in range(12):
        val = sa.sensors[x].value
        if val < 0:
            val = 8000
        data[i].filter(val)
        i += 1
        if i >= 12:
            i = 0
    toSend = []
    for a in data:
        toSend.append(a.getAverage())
    #print("Sensor values: ", toSend)
    return jsonify(toSend)



if __name__ == '__main__':
    data = []
    for i in range(12):
        data.append(AverageFilter(size = 5))
    sa = SensorArray()
    app.run(host='0.0.0.0', port=80)