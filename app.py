import streamlit as st
import cv2
import numpy as np

st.title("Text to Mind Map Generator")

text = st.text_area("Enter your content")

if st.button("Generate Mind Map"):

    words = text.split()
    keywords = words[:5]

    img = np.ones((600,800,3), dtype=np.uint8) * 255

    center = (400,300)
    cv2.circle(img, center, 40, (0,0,0), 2)
    cv2.putText(img,"Topic",(370,305),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)

    positions = [(200,150),(600,150),(200,450),(600,450),(400,100)]

    for i, word in enumerate(keywords):
        x,y = positions[i]

        cv2.rectangle(img,(x-50,y-20),(x+50,y+20),(0,0,0),2)
        cv2.putText(img,word,(x-40,y+5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)

        cv2.line(img,center,(x,y),(0,0,0),2)

    st.image(img, channels="BGR")

    cv2.imwrite("mindmap.png", img)

    with open("mindmap.png","rb") as file:
        st.download_button("Download Mind Map",file,"mindmap.png")
