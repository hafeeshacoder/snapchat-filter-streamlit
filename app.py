import streamlit as st
import cv2
import numpy as np
import tempfile

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="AI Traffic Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("🚗 Intelligent Visual Traffic Counter")
st.write("Upload a fixed-camera traffic video to analyze and classify vehicles in real-time.")

# 3. SIDEBAR CONTROLS
st.sidebar.title("📊 Control Panel")
st.sidebar.info("Adjust settings if detection is poor.")

# Sensitivity: Lower means the AI is more likely to pick up slight movements
sensitivity = st.sidebar.slider("Detection Sensitivity", 10, 250, 150)
# Min Area: Helps ignore noise like wind in trees or small shadows
min_area = st.sidebar.number_input("Minimum Object Size (Area)", value=200)
debug_mode = st.sidebar.checkbox("Show AI Debug Mask")

st.sidebar.divider()
st.sidebar.subheader("Live Stats")
car_stat = st.sidebar.metric("Cars", "0")
truck_stat = st.sidebar.metric("Trucks/Buses", "0")
ped_stat = st.sidebar.metric("Pedestrians", "0")

# 4. INITIALIZE OPENCV TOOLS
# MOG2 is the Background Subtraction (Filtering) algorithm from your syllabus
backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=sensitivity, detectShadows=True)

def process_frame(frame, min_a):
    # STEP 1: Background Subtraction (Filtering)
    fg_mask = backSub.apply(frame)
    
    # STEP 2: Cleaning the mask (Thresholding & Morphological Filtering)
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    
    # STEP 3: Contour Detection
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    counts = {"Car": 0, "Truck": 0, "Pedestrian": 0}
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_a:
            continue
            
        # STEP 4: Drawing & Logic-based Classification (K-NN Principle)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        
        # Classification based on Area and Shape Features
        if area > 4500:
            label, color = "Truck", (0, 0, 255) # Red
            counts["Truck"] += 1
        elif area > 800 and aspect_ratio > 0.8:
            label, color = "Car", (0, 255, 0) # Green
            counts["Car"] += 1
        else:
            label, color = "Pedestrian", (255, 255, 0) # Cyan
            counts["Pedestrian"] += 1
            
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
    return frame, fg_mask, counts

# 5. FILE UPLOAD & EXECUTION
uploaded_file = st.file_uploader("Upload Traffic Video (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

if uploaded_file:
    # Handle video file buffer
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    
    # UI Layout: Video on left, Mask on right (if debug)
    col1, col2 = st.columns([2, 1])
    video_placeholder = col1.empty()
    mask_placeholder = col2.empty() if debug_mode else None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Processing
        frame = cv2.resize(frame, (800, 480))
        processed_frame, mask, current_counts = process_frame(frame, min_area)
        
        # Display Results
        video_placeholder.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
        if debug_mode:
            mask_placeholder.image(mask, caption="AI View (Movement Detection)")
            
        # Update Sidebar Stats
        car_stat.metric("Cars", current_counts["Car"])
        truck_stat.metric("Trucks/Buses", current_counts["Truck"])
        ped_stat.metric("Pedestrians", current_counts["Pedestrian"])
        
    cap.release()
    st.success("Video processing complete!")
else:
    st.info("💡 Pro Tip: Use a video where the camera is completely still (e.g., CCTV or Dashboard cam).")
