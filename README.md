
# Face-Recognition-Attendance-System

This project is a POC web application demonstrating the use of facial recognition for marking attendance. 
It is a web application that can be used across various sectors, including corporate offices, educational institutions, 
manufacturing plants, healthcare facilities, retail stores, government buildings, remote work environments, and events, 
to streamline attendance tracking, enhance security, and improve operational efficiency.

Recognizes, detects the faces and takes the attendance automatically.

## Functionality Overview
- Register new employees.
- Add new employee photos.
- View attendance reports of all students log-in and log-out in the browser. We can also download both the log-ins and log-offs attendance sheet from the browser itself for easy access.

## This project is built using the below tools and libraries
 - _[OpenCV](https://en.wikipedia.org/wiki/OpenCV)_ - open-source library used for computer vision and image processing tasks
 - _[Dlib](https://en.wikipedia.org/wiki/Dlib)_ - machine learning library specializing in computer vision and image processing, particularly known for its facial recognition capabilities
 - _[face_recognition](https://pypi.org/project/face-recognition/#:~:text=called%20face_recognition%20that%20you%20can,for%20each%20person%20with%20the)_ - Python library that simplifies the process of detecting and recognizing faces in images and video, built on top of dlib and OpenCV
 - _[Flask](https://en.wikipedia.org/wiki/Flask_(web_framework))_ - lightweight and flexible web framework for Python used to build web applications and APIs.

### SOFTWARE SPECIFICATIONS
BACK END : PYTHON, FLASK, MICROSOFT EXCEL

FRONT END : HTML, CSS, JAVA SCRIPT

APPLICATION TYPE : WEB APPLICATION

IDE : PYCHARM COMMUNITY EDITION

### Face Detection 
- Dlib's HOG facial detector.

### Facial Landmark Detection 
- Dlib's 68 point shape predictor

### Extraction of Facial Embeddings 
- face_recognition by Adam Geitgey

### Classification of Unknown Embedding
- using a Linear SVM (scikit-learn)_
- The application was tested on data from 45 students.

## Scope of the project
It includes automating attendance tracking using facial recognition technology to replace manual methods. It features a web application for real-time management and reporting of attendance, targeting corporate offices, schools, and other organizations. The project also involves web development and database management with a user-friendly interface, aiming to improve accuracy and efficiency in tracking employee or student presence.

## Note on Dataset Privacy:
For privacy reasons, all image datasets in the __IMAGE_FILES__ folder, which contained JPG images of my classmates, have been removed from this project. 