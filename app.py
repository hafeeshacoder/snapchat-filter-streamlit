import streamlit as st
import cv2
import numpy as np
import nltk
from nltk.corpus import stopwords
import math

nltk.download('stopwords')

st.title("🧠 Text to Mind Map Generator")

text = st.text_area("Enter your content")

if st.button("Generate Mind Map"):

    stop_words = set(stopwords.words('english'))

    words = text.lower().split()

    keywords = [w for w in words if w not in stop_words]

    keywords = list(dict.fromkeys(keywords))[:8]

    # Create blank white image
    img = np.ones((700,900,3), dtype=np.uint8) * 255

    center = (450,350)

    # Draw center topic
    cv2.circle(img, center, 60, (0,100,255), -1)
    cv2.putText(img,"Topic",(415,355),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

    # Colors for nodes
    colors = [
        (255,0,0),
        (0,200,0),
        (0,0,255),
        (255,100,0),
        (200,0,200),
        (0,200,200),
        (100,100,255),
        (0,150,255)
    ]

    radius = 250
    angle_step = 360 / len(keywords)

    for i, word in enumerate(keywords):

        angle = math.radians(i * angle_step)

        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))

        color = colors[i % len(colors)]

        # draw line
        cv2.line(img, center, (x,y), color, 3)

        # draw node
        cv2.circle(img, (x,y), 50, color, -1)

        cv2.putText(img, word[:10],
                    (x-35,y+5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255,255,255),
                    2)

    st.image(img, channels="BGR")

    cv2.imwrite("mindmap.png", img)

    with open("mindmap.png","rb") as file:
        st.download_button("Download Mind Map",file,"mindmap.png")
