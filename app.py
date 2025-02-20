import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from flask import Flask, flash, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename
import csv


UPLOAD_FOLDER = r'E:\GitHub Projects\Face Recognition Attendance System\IMAGE_FILES'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def hello_world():
    return render_template("login.html")


database={'admin':'123', 'ADMIN':'123'}


@app.route('/form_login', methods=['POST', 'GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
        return render_template('login.html', info='Invalid User')

    else:
        if database[name1] != pwd:
            return render_template('login.html', info='Invalid Password')
        else:
            return render_template('navig.html', name=name1)


@app.route('/navig')
def navig_file():
    return render_template('navig.html')


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/success', methods=['GET', 'POST'])
def success():
    if 'file' not in request.files:
        # flash('No file part')
        return render_template('upload.html')
    file = request.files['file']
    if file.filename == '':
        # flash('No image selected for uploading')
        return render_template('upload.html')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        # flash('Image successfully uploaded and displayed below')
        return render_template('upload.html')
    else:
        # flash('Allowed image types are -> png, jpg, jpeg, gif')
        return render_template('upload.html')


@app.route('/index')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    IMAGE_FILES = []
    filename = []
    dir_path = r'E:\GitHub Projects\Face Recognition Attendance System\IMAGE_FILES'

    for imagess in os.listdir(dir_path):
        img_path = os.path.join(dir_path, imagess)
        img_path = face_recognition.load_image_file(img_path)  # reading image and append to list
        IMAGE_FILES.append(img_path)
        filename.append(imagess.split(".", 1)[0])

    def encoding_img(IMAGE_FILES):
        encodeList = []
        for img in IMAGE_FILES:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def takeAttendence(name):
        #fields = ['Name', 'Time In']
        #with open('attendance.csv', 'w') as f1:
            #csvwriter = csv.writer(f1)
            #csvwriter.writerow(fields)

        with open('attendanceIn.csv', 'r+') as f:
            mypeople_list = f.readlines()
            nameList = []
            for line in mypeople_list:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                time = now.strftime('%I:%M:%S')
                date = now.strftime("%d-%B-%Y")
                f.writelines(f'\n{name}, {time}, {date}')

    encodeListknown = encoding_img(IMAGE_FILES)
    # print(len('sucesses'))

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgc = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        # converting image to RGB from BGR
        imgc = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        fasescurrent = face_recognition.face_locations(imgc)
        encode_fasescurrent = face_recognition.face_encodings(imgc, fasescurrent)

        # faceloc- one by one it grab one face location from fasescurrent
        # than encodeFace grab encoding from encode_fasescurrent
        # we want them all in same loop so we are using zip
        for encodeFace, faceloc in zip(encode_fasescurrent, fasescurrent):
            matches_face = face_recognition.compare_faces(encodeListknown, encodeFace)
            face_distence = face_recognition.face_distance(encodeListknown, encodeFace)
            # print(face_distence)
            # finding minimum distence index that will return best match
            matchindex = np.argmin(face_distence)

            if matches_face[matchindex]:
                name = filename[matchindex].upper()
                # print(name)
                y1, x2, y2, x1 = faceloc
                # multiply locations by 4 because we above we reduced our webcam input image by 0.25
                #y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), 3, cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                takeAttendence(name)  # taking name for attendence function above

        # cv2.imshow("campare", img)
        # cv2.waitKey(0)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27:
            break


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/S3_csv_table")
def s3():
  with open(r'E:\GitHub Projects\Face Recognition Attendance System\attendanceIn.csv') as file:
    reader = csv.reader(file)
    return render_template("S3_csv_table.html", csv=reader)

###################################################################


@app.route('/indexOut')
def index1():
    """Video streaming home page."""
    return render_template('indexOut.html')


def gen1():
    IMAGE_FILES = []
    filename = []
    dir_path = r'E:\GitHub Projects\Face Recognition Attendance System\IMAGE_FILES'

    for imagess in os.listdir(dir_path):
        img_path = os.path.join(dir_path, imagess)
        img_path = face_recognition.load_image_file(img_path)  # reading image and append to list
        IMAGE_FILES.append(img_path)
        filename.append(imagess.split(".", 1)[0])

    def encoding_img(IMAGE_FILES):
        encodeList = []
        for img in IMAGE_FILES:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def takeAttendence1(name):
        #fields = ['Name', 'Time In']
        #with open('attendance.csv', 'w') as f1:
            #csvwriter = csv.writer(f1)
            #csvwriter.writerow(fields)

        with open('attendanceOut.csv', 'r+') as f:
            mypeople_list = f.readlines()
            nameList = []
            for line in mypeople_list:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                time = now.strftime('%I:%M:%S')
                date = now.strftime("%d-%B-%Y")
                f.writelines(f'\n{name}, {time}, {date}')

    encodeListknown = encoding_img(IMAGE_FILES)
    # print(len('sucesses'))

    cap1 = cv2.VideoCapture(0)

    while True:
        success, img = cap1.read()
        imgc = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        # converting image to RGB from BGR
        imgc = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        fasescurrent = face_recognition.face_locations(imgc)
        encode_fasescurrent = face_recognition.face_encodings(imgc, fasescurrent)

        # faceloc- one by one it grab one face location from fasescurrent
        # than encodeFace grab encoding from encode_fasescurrent
        # we want them all in same loop so we are using zip
        for encodeFace, faceloc in zip(encode_fasescurrent, fasescurrent):
            matches_face = face_recognition.compare_faces(encodeListknown, encodeFace)
            face_distence = face_recognition.face_distance(encodeListknown, encodeFace)
            # print(face_distence)
            # finding minimum distence index that will return best match
            matchindex = np.argmin(face_distence)

            if matches_face[matchindex]:
                name = filename[matchindex].upper()
                # print(name)
                y1, x2, y2, x1 = faceloc
                # multiply locations by 4 because we above we reduced our webcam input image by 0.25
                #y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), 3, cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                takeAttendence1(name)  # taking name for attendence function above

        # cv2.imshow("campare", img)
        # cv2.waitKey(0)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27:
            break


@app.route('/video_feed1')
def video_feed1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen1(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/out")
def s4():
  with open(r'E:\GitHub Projects\Face Recognition Attendance System\attendanceOut.csv') as file:
    reader = csv.reader(file)
    return render_template("out.html", csv=reader)


if __name__ == "__main__":
    app.run(debug=True)
