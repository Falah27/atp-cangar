from flask import Flask,render_template,Response, request
import cv2
import pyrebase


config = {
  "apiKey": "AIzaSyDRq6JqMAtQiKvOg6mgILsr7ZQ42gMBV5A",
  "authDomain": "cangar-europa-server.firebaseapp.com",
  "databaseURL": "https://cangar-europa-server-default-rtdb.firebaseio.com",
  "projectId": "cangar-europa-server",
  "storageBucket": "cangar-europa-server.appspot.com",
  "messagingSenderId": "671201908053",
  "appId": "1:671201908053:web:99765d65cbb131dda2cbdc"
};

firebase = pyrebase.initialize_app(config)
db = firebase.database()


app=Flask(__name__)


def generate_frames():
    ind_cam = db.child('sensor read').child('camera').get()
    index_cam = ind_cam.val()
    int_cam = int(index_cam)
    camera=cv2.VideoCapture(int_cam)

    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        camera_index = request.form['camera']
        db.child('sensor read').child('camera').set(camera_index)
        return render_template('index.html')
    return render_template('index.html')
    

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)

