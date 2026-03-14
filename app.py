import streamlit as st
import numpy as np
import cv2

st.title("🎨 Smart Color Image Generator")

st.write("Enter a color name to generate a color and related image")

color_input = st.text_input("Enter Color Name")

colors = {
    "red": (0,0,255),
    "green": (0,255,0),
    "blue": (255,0,0),
    "yellow": (0,255,255),
    "purple": (255,0,255),
    "cyan": (255,255,0),
    "orange": (0,165,255),
    "pink": (203,192,255),
    "black": (0,0,0),
    "white": (255,255,255),
}

if st.button("Generate"):

    color = color_input.lower()

    if color in colors:

        img = np.ones((400,400,3),dtype=np.uint8)*255

        # color background
        img[:] = colors[color]

        # Draw related objects
        if color == "blue":
            # ocean waves
            cv2.circle(img,(200,200),80,(255,255,255),3)

        elif color == "green":
            # tree
            cv2.rectangle(img,(180,250),(220,350),(42,42,165),-1)
            cv2.circle(img,(200,200),80,(0,200,0),-1)

        elif color == "yellow":
            # sun
            cv2.circle(img,(200,200),80,(0,255,255),-1)

        elif color == "red":
            # heart
            cv2.circle(img,(170,200),40,(0,0,255),-1)
            cv2.circle(img,(230,200),40,(0,0,255),-1)
            pts = np.array([[140,210],[260,210],[200,300]])
            cv2.fillPoly(img,[pts],(0,0,255))

        elif color == "black":
            # moon
            cv2.circle(img,(200,200),70,(200,200,200),-1)

        elif color == "white":
            # cloud
            cv2.circle(img,(180,200),40,(255,255,255),-1)
            cv2.circle(img,(220,200),40,(255,255,255),-1)
            cv2.circle(img,(200,170),40,(255,255,255),-1)

        cv2.putText(img,
                    color.upper(),
                    (120,380),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,0),
                    2)

        st.image(img,channels="BGR")

        file_name = f"{color}_image.png"
        cv2.imwrite(file_name,img)

        with open(file_name,"rb") as file:
            st.download_button(
                "Download Image",
                data=file,
                file_name=file_name,
                mime="image/png"
            )

    else:
        st.error("Color not available")
