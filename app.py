import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
crown = cv2.imread("crown.png", -1)

class FaceFilter(VideoTransformerBase):

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            crown_width = w
            crown_height = int(h/2)

            resized_crown = cv2.resize(crown,(crown_width,crown_height))

            for i in range(crown_height):
                for j in range(crown_width):
                    if resized_crown[i,j][3] != 0:
                        img[y-i-10, x+j] = resized_crown[i,j][:3]

        return img


st.title("Snapchat Style Face Filter")
st.write("Real time face filter using Streamlit")

webrtc_streamer(
    key="snapchat",
    video_transformer_factory=FaceFilter
)
