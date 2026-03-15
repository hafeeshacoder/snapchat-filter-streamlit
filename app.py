import streamlit as st
import cv2
import numpy as np
import tempfile

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Traffic Detection System", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    section[data-testid="stSidebar"] { width: 300px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("🚗 Intelligent Traffic Detection System")
st.write("Visual recognition and classification within a defined Detection Zone.")

# 3. SIDEBAR CONTROLS
st.sidebar.title("🛠 Settings")
sensitivity = st.sidebar.slider("Detection Sensitivity", 10, 200, 100)
min_area = st.sidebar.number_input("Minimum Object Size (Area)", value=150)
debug_mode = st.sidebar.checkbox("Show AI Mask (Internal View)")

st.sidebar.divider()
st.sidebar.warning("Note: Trees and sky are ignored to improve accuracy.")

# 4. INITIALIZE OPENCV TOOLS
backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=sensitivity, detectShadows=True)

def process_roi(roi_frame, min_a):
    # STEP 1: Background Subtraction (Filtering)
    fg_mask = backSub.apply(roi_frame)
    
    # STEP 2: Cleaning the mask (Thresholding & Morphological Filtering)
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    
    # STEP 3: Contour Detection
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_a:
            continue
            
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        
        # Classification Logic
        if area > 4000:
            label, color = "TRUCK", (0, 0, 255) # Red
        elif area > 600 and aspect_ratio > 0.7:
            label, color = "CAR", (0, 255, 0) # Green
        else:
            label, color = "PEDESTRIAN", (255, 255, 0) # Cyan
            
        cv2.rectangle(roi_frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(roi_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
    return roi_frame, fg_mask

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
        if not ret:
            break
            
        frame = cv2.resize(frame, (800, 500))
        
        # --- DEFINE REGION OF INTEREST (ROI) ---
        # We focus on the bottom half of the screen where the road is
        # [y_start:y_end, x_start:x_end]
        roi_y1, roi_y2, roi_x1, roi_x2 = 220, 480, 50, 750
        roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
        
        processed_roi, mask = process_roi(roi, min_area)
        
        # Overlay processed ROI back to original frame
        frame[roi_y1:roi_y2, roi_x1:roi_x2] = processed_roi
        
        # Visual Boundary for the Report
        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 255), 1)
        cv2.putText(frame, "DETECTION ZONE", (roi_x1, roi_y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        
        # Display Results
        video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if debug_mode:
            mask_placeholder.image(mask, caption="AI Mask (ROI Only)")
            
    cap.release()
    st.success("Video processing complete!")
else:
    st.info("Upload a video to begin analysis.")
