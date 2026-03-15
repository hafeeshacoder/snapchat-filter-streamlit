import streamlit as st
import cv2
import numpy as np
from PIL import Image

# SETTING PAGE CONFIG FOR ATTRACTIVE UI
st.set_page_config(page_title="AI Traffic Intelligence", layout="wide")

# CUSTOM CSS FOR STYLING
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Intelligent Visual Traffic Counter")
st.markdown("### Powered by OpenCV, K-NN Classification & Streamlit")

# SIDEBAR FOR CONTROLS & STATS
st.sidebar.title("📊 Traffic Dashboard")
conf_threshold = st.sidebar.slider("Detection Sensitivity", 0, 255, 200)
st.sidebar.divider()

# PLACEHOLDERS FOR REAL-TIME STATS
car_stat = st.sidebar.metric("Cars Detected", "0")
truck_stat = st.sidebar.metric("Trucks Detected", "0")
ped_stat = st.sidebar.metric("Pedestrians", "0")

# --- CORE LOGIC ---

# 1. Background Subtraction (Filtering)
backSub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=conf_threshold)

def process_frame(frame):
    # Apply Filtering to isolate moving objects
    fg_mask = backSub.apply(frame)
    
    # Cleaning the mask (Morphological Filtering)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    
    # 2. Contour Detection
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    counts = {"Car": 0, "Truck": 0, "Pedestrian": 0}
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500: continue  # Filter noise
        
        # 3. K-NN Inspired Logic (Classification based on Area/Aspect Ratio)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        
        # Classification Logic
        if area > 4000:
            label = "Truck"
            color = (0, 0, 255) # Red
            counts["Truck"] += 1
        elif 1000 < area <= 4000 and aspect_ratio > 1.0:
            label = "Car"
            color = (0, 255, 0) # Green
            counts["Car"] += 1
        else:
            label = "Pedestrian"
            color = (255, 255, 0) # Cyan
            counts["Pedestrian"] += 1
            
        # 4. Drawing
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
    return frame, counts

# --- UI INTERACTION ---
uploaded_file = st.file_uploader("Upload a traffic video file...", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded file to temp path
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    cap = cv2.VideoCapture("temp_video.mp4")
    frame_window = st.image([]) # Placeholder for video
    
    total_counts = {"Car": 0, "Truck": 0, "Pedestrian": 0}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.resize(frame, (800, 500))
        processed_img, current_counts = process_frame(frame)
        
        # Convert BGR to RGB for Streamlit
        processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        
        # Update metrics in sidebar
        car_stat.metric("Cars Detected", current_counts["Car"])
        truck_stat.metric("Trucks Detected", current_counts["Truck"])
        ped_stat.metric("Pedestrians", current_counts["Pedestrian"])
        
        # Display frame
        frame_window.image(processed_img)
    
    cap.release()
else:
    st.info("Please upload a video to start the traffic analysis.")
