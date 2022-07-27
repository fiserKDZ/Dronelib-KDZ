from flask import Flask, render_template, jsonify, Response
import random    

from core.regulator import AverageFilter

from camera_pi import Camera


mockData = False



sa = None
if not mockData:
    from core.sensorArray import SensorArray
    sa = SensorArray()

def readSensorArray(mockData = False):
    i = 3 #Posun senzorů vpravo
    if not mockData: sa.read()
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
    telemetry = {"height": 0, "battery": 0, "time": 0, "speed": 0, "state": "Online"}
    toSend = {"telemetry": telemetry, "sensorArray": sensorArray}
    return jsonify(toSend)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    data = []
    for i in range(12):
        data.append(AverageFilter(size = 2))
    app.run(host='0.0.0.0', port=80)