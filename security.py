import cv2
import time
import sys
import os
import speech_recognition as sr
import wave
import pyaudio
import pyttsx3
import smtplib
from twilio.rest import Client


# set delay to enable "security" lets you move away from camera
#was supposed to be used to prevent accidental detection while setting program
#time.sleep(1)

# use the xml file with different data points for face detection
# obtained from https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# Initialize camera
cam = cv2.VideoCapture(0)

# set resolution
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# Initialize speech recognizer
#r = sr.Recognizer()
# set the device index to use for the microphone, was causing problems
#mic = sr.Microphone(device_index=3)

# used so only one message gets sent from face detection
face_counter = 0

while True:
    # Capture frame-by-frame
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # If a face is detected, print and do next check
    if len(faces) > 0:
        print("Face detected!")
        # so it only sends one
        if face_counter == 0:
            # Twilio account
            account_sid = ''
            auth_token = ''
            twilio_number = ''

            # Phone number to receive
            to_number = ''
            message = 'Face detected! Room unsecure!'

            # Create Twilio client and send message
            client = Client(account_sid, auth_token)
            client.messages.create(
                to=to_number,
                from_=twilio_number,
                body=message
            )
            face_counter+=1
            

        """ with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            if "specific word" in text.lower():
                print("Specific word detected")
            else:
                print("Specific word not detected")

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results due to {e}") """

    # This draws a green square around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Send email
""" smtp_server.sendmail(sender_email, receiver_email, message.as_string())
smtp_server.quit() """

#print('Email sent successfully!')

#print(sr.Microphone.list_microphone_names())


# Releases the camera after q is pressed
cam.release()
cv2.destroyAllWindows()