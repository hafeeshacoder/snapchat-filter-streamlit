import streamlit as st
import numpy as np
import cv2

# Page settings
st.set_page_config(page_title="Smart Color Generator", page_icon="🎨")

# Custom CSS for styling
st.markdown("""
<style>
.main-title{
text-align:center;
font-size:42px;
font-weight:bold;
color:#ff4b4b;
}
.sub-text{
text-align:center;
font-size:18px;
color:gray;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎨 Smart Color Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Enter a color name and generate a beautiful color preview</p>', unsafe_allow_html=True)

# User input
color_input = st.text_input("Enter Color Name")

# Color dictionary (BGR for OpenCV)
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

# Button
if st.button("Generate Color"):

    color = color_input.lower()

    if color in colors:

        # Create image
        img = np.zeros((400,400,3), dtype=np.uint8)
        img[:] = colors[color]

        # Display image
        st.image(img, channels="BGR", caption=f"{color.capitalize()} Color")

        # Get RGB values
        b,g,r = colors[color]

        # Convert to HEX
        hex_color = '#%02x%02x%02x' % (r,g,b)

        # Display color info
        st.success(f"RGB Value: ({r}, {g}, {b})")
        st.info(f"HEX Code: {hex_color}")

        # Save image
        file_name = f"{color}_color.png"
        cv2.imwrite(file_name, img)

        # Download button
        with open(file_name, "rb") as file:
            st.download_button(
                label="Download Image",
                data=file,
                file_name=file_name,
                mime="image/png"
            )

    else:
        st.error("Color not found. Try red, blue, green, yellow etc.")
