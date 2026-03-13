import streamlit as st
import cv2
import numpy as np
import math
import re
from collections import Counter

st.title("AI Mind Map Generator")

text = st.text_area("Enter your content")

if st.button("Generate Mind Map"):

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    stopwords = {
        "the","is","a","an","and","of","to","in","for","on","with",
        "that","this","it","as","are","was","be","by","from"
    }

    words = [w for w in words if w not in stopwords and len(w) > 3]

    freq = Counter(words)

    keywords = [w for w,_ in freq.most_common(6)]

    topic = keywords[0].capitalize()

    img = np.ones((800,1000,3),dtype=np.uint8)*255

    center = (500,400)

    # Draw center topic
    cv2.circle(img,center,90,(0,140,255),-1)

    text_size = cv2.getTextSize(topic,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9,2)[0]

    cv2.putText(img,
                topic,
                (center[0]-text_size[0]//2,
                 center[1]+10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,(255,255,255),2)

    radius = 300
    angle_step = 360/len(keywords)

    colors = [
        (255,0,0),
        (0,200,0),
        (0,0,255),
        (255,100,0),
        (200,0,200),
        (0,200,200)
    ]

    for i,word in enumerate(keywords[1:]):

        angle = math.radians(i*angle_step)

        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))

        color = colors[i]

        cv2.line(img,center,(x,y),color,3)

        cv2.ellipse(img,(x,y),(100,45),0,0,360,color,-1)

        txt = word.capitalize()

        size = cv2.getTextSize(txt,
                               cv2.FONT_HERSHEY_SIMPLEX,
                               0.7,2)[0]

        cv2.putText(img,
                    txt,
                    (x-size[0]//2,y+5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,(255,255,255),2)

    st.image(img,channels="BGR")
