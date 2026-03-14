import streamlit as st
import numpy as np
import cv2

st.title("🎨 Text to Color Generator")

st.write("Type a color name and generate a color image.")

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
    "gray": (128,128,128),
    "brown": (19,69,139)
}

if st.button("Generate Color"):

    color = color_input.lower()

    if color in colors:

        img = np.zeros((400,400,3), dtype=np.uint8)

        img[:] = colors[color]

        cv2.putText(img,
                    color.upper(),
                    (80,210),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    2)

        st.image(img, channels="BGR")

        file_name = f"{color}_color.png"

        cv2.imwrite(file_name, img)

        with open(file_name, "rb") as file:
            st.download_button(
                label="Download Image",
                data=file,
                file_name=file_name,
                mime="image/png"
            )

    else:
        st.error("Color not found. Try red, blue, green etc.")
