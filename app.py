import streamlit as st
import cv2
import numpy as np
import math
from collections import Counter

st.title("AI Mind Map Generator")

text = st.text_area("Enter your content")

if st.button("Generate Mind Map"):

    words = text.lower().split()

    stopwords = ["is","the","a","an","and","of","to","in","for","on","with","that","this"]

    words = [w for w in words if w not in stopwords]

    freq = Counter(words)

    keywords = [w for w,c in freq.most_common(6)]

    img = np.ones((800,1000,3),dtype=np.uint8)*255

    center = (500,400)

    # center node
    cv2.circle(img,center,80,(0,150,255),-1)
    cv2.putText(img,"MAIN TOPIC",(430,405),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

    radius = 280
    angle_step = 360/len(keywords)

    colors = [(255,0,0),(0,200,0),(0,0,255),
              (255,100,0),(200,0,200),(0,200,200)]

    for i,word in enumerate(keywords):

        angle = math.radians(i*angle_step)

        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))

        color = colors[i]

        # branch
        cv2.line(img,center,(x,y),color,3)

        # node
        cv2.ellipse(img,(x,y),(90,40),0,0,360,color,-1)

        cv2.putText(img,word,(x-40,y+5),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

    st.image(img,channels="BGR")

    cv2.imwrite("mindmap.png",img)

    with open("mindmap.png","rb") as f:
        st.download_button("Download Mind Map",f,"mindmap.png")
