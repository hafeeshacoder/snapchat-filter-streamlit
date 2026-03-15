import streamlit as st
import cv2
import numpy as np
import tempfile

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Traffic Status Monitor", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .status-box { 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center; 
        font-weight: bold; 
        font-size: 24px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("🚦 Intelligent Traffic Status Monitor")
st.write("Detecting vehicles and calculating real-time traffic flow status.")

# 3. SIDEBAR CONTROLS
st.sidebar.title("🛠 Settings")
sensitivity = st.sidebar.slider("Detection Sensitivity", 10, 200, 100)
min_area = st.sidebar.number_input("Minimum Vehicle Size", value=400)
debug_mode = st.sidebar.checkbox("Show AI Mask (Internal View)")

# Placeholder for Traffic Status in Sidebar
status_placeholder = st.sidebar.empty()

# 4. INITIALIZE OPENCV TOOLS
backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=sensitivity, detectShadows=True)

def process_roi(roi_frame, min_a):
    fg_mask = backSub.apply(roi_frame)
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    vehicle_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_a:
            continue
            
        x, y, w, h = cv2.boundingRect(cnt)
        vehicle_count += 1
        
        # Identify as generic Vehicle
        cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(roi_frame, "Vehicle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    return roi_frame, fg_mask, vehicle_count

# 5. FILE UPLOAD & EXECUTION
uploaded_file = st.file_uploader("Upload Traffic Video", type=["mp4", "avi", "mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    col1, col2 = st.columns([2, 1])
    video_placeholder = col1.empty()
    mask_placeholder = col2.empty() if debug_mode else None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
            
        frame = cv2.resize(frame, (800, 500))
        
        # DEFINE ROI (Detection Zone)
        roi_y1, roi_y2, roi_x1, roi_x2 = 220, 480, 50, 750
        roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
        
        processed_roi, mask, count = process_roi(roi, min_area)
        frame[roi_y1:roi_y2, roi_x1:roi_x2] = processed_roi
        
        # TRAFFIC STATUS LOGIC
        if count == 0:
            status, color = "NO TRAFFIC", "#d1d1d1" # Gray
        elif count <= 3:
            status, color = "LOW TRAFFIC", "#28a745" # Green
        elif count <= 7:
            status, color = "MEDIUM TRAFFIC", "#ffc107" # Yellow
        else:
            status, color = "HEAVY TRAFFIC", "#dc3545" # Red
            
        status_placeholder.markdown(f"""
            <div class='status-box' style='background-color: {color}; color: white;'>
                {status}<br><span style='font-size: 14px;'>Vehicles: {count}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Visual Boundary
        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (255, 255, 255), 1)
        
        video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if debug_mode:
            mask_placeholder.image(mask, caption="Movement Mask")
            
    cap.release()
    st.success("Analysis Complete")
else:
    st.info("Upload a video to begin traffic analysis.")
