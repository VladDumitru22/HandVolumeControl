# Hand Volume Control via Real-Time Hand Tracking ✋🔊

## Overview 📝

This Python application implements a real-time **hand gesture recognition system** to dynamically adjust the system audio volume on Windows. Using MediaPipe’s hand landmark detection framework and OpenCV video capture, the system computes the Euclidean distance between the thumb tip (landmark 4) and the index fingertip (landmark 8). This distance is then linearly interpolated to map to the Windows master volume range, allowing intuitive volume control through natural hand gestures.

---

## System Architecture and Workflow ⚙️

1. **Video Capture and Preprocessing** 

   - Video frames are captured from the default webcam using OpenCV's `VideoCapture`.
   - Frames are flipped horizontally for a mirror-like user experience. 
   - Frames are converted to RGB color space to feed into MediaPipe’s hand detection pipeline. 

2. **Hand Detection and Landmark Extraction** 

   - MediaPipe Hands solution is initialized with configurable parameters for detection and tracking confidence.
   - Each frame is processed to detect hand landmarks.
   - Landmark positions (normalized coordinates) are converted to pixel coordinates relative to the frame size.
   - The module extracts the coordinates of landmarks 4 (thumb tip) and 8 (index fingertip). 

3. **Distance Calculation and Volume Mapping** 

   - The Euclidean distance between landmarks 4 and 8 is computed using the Pythagorean theorem.
   - This distance is clamped within empirically determined minimum and maximum ranges to filter noise and outliers.
   - The clamped distance value is mapped linearly to the system volume range (retrieved from Windows via `pycaw`).
   - Volume is adjusted by setting the master volume level through the `IAudioEndpointVolume` COM interface.

4. **Visual Feedback** 

   - A volume bar is drawn on the frame indicating the current volume percentage. 
   - Visual cues (lines and circles) highlight the active fingertips involved in volume control. 
   - The application displays frames per second (FPS) for performance monitoring. 

---

## Dependencies 📦

- **OpenCV (`opencv-python`)**: Real-time video capture and image processing.
- **MediaPipe**: ML solution for hand landmark detection.
- **NumPy**: Efficient numeric operations including interpolation.
- **pycaw**: Python Core Audio Windows library for programmatic volume control.
- **comtypes**: Python COM interface required by pycaw.
- **math**: Core Python library for Euclidean distance calculation.

---

## Installation ⚡

```bash
# Create a virtual environment (optional but recommended) 
python -m venv venv

# Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (Git Bash):
source venv/Scripts/activate

# On Linux/macOS:
source venv/bin/activate

# Install the required packages 
pip install -r requirements.txt

# Run the main script to start the application
python main.py
```
