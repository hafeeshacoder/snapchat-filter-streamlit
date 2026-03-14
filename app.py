import streamlit as st
import numpy as np
import cv2

st.set_page_config(page_title="Smart Color Generator", page_icon="🎨", layout="centered")

# ---------- CSS STYLING ----------
st.markdown("""
<style>

body {
background: linear-gradient(120deg,#f6d365,#fda085);
}

.main-title{
text-align:center;
font-size:48px;
font-weight:bold;
color:#ff4b4b;
margin-bottom:5px;
}

.sub-text{
text-align:center;
font-size:20px;
color:#444;
margin-bottom:30px;
}

.stTextInput input{
border-radius:10px;
border:2px solid #ff4b4b;
padding:10px;
font-size:18px;
}

.stButton>button{
background: linear-gradient(90deg,#ff4b4b,#ff9a9e);
color:white;
font-size:18px;
border-radius:10px;
padding:10px 25px;
border:none;
}

.stButton>button:hover{
background: linear-gradient(90deg,#ff6a6a,#ffb199);
}

.color-card{
padding:15px;
border-radius:15px;
box-shadow:0px 5px 15px rgba(0,0,0,0.2);
text-align:center;
font-size:18px;
font-weight:bold;
margin-top:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<p class="main-title">🎨 Smart Color Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Generate beautiful colors and download them instantly</p>', unsafe_allow_html=True)

# ---------- INPUT ----------
color_input = st.text_input("Enter Color Name")

# ---------- COLOR DICTIONARY ----------
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

# ---------- BUTTON ----------
if st.button("✨ Generate Color"):

    color = color_input.lower()

    if color in colors:

        img = np.zeros((400,400,3), dtype=np.uint8)
        img[:] = colors[color]

        st.image(img, channels="BGR", caption=f"{color.capitalize()} Color Preview")

        b,g,r = colors[color]
        hex_color = '#%02x%02x%02x' % (r,g,b)

        st.markdown(f"""
        <div class="color-card">
        RGB Value : ({r}, {g}, {b}) <br>
        HEX Code : {hex_color}
        </div>
        """, unsafe_allow_html=True)

        file_name = f"{color}_color.png"
        cv2.imwrite(file_name, img)

        with open(file_name, "rb") as file:
            st.download_button(
                label="⬇ Download Image",
                data=file,
                file_name=file_name,
                mime="image/png"
            )

    else:
        st.error("Color not found. Try red, blue, green, yellow etc.")
