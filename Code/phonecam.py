import cv2
import numpy as np
import time
from datetime import datetime
from ultralytics import YOLO
import sys
import os
import logging
import multiprocessing as mp
import requests
import imutils
import subprocess
import universal

def install_requirements():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing requirements: {e}")

roi_x1 = None
roi_x2 = None
drawing = False
roi_crossed = False
last_screenshot_time = None
screenshot_interval = 1.5  # 1.5 seconds interval between screenshots

# List to store IDs of boxes that have already been captured
captured_boxes = []

# Function to simulate processing
def process_screenshot(path,name):
    # print(f"start {q}")
    # cpu_intensive_operation(25)
    current_dir=os.getcwd()
    # print(f"end {q}")
    output_dir = os.path.join(current_dir, "pipeline.py")
    image_path = path
    name_image = name
    # Construct the command
    command = [
        "python", output_dir, 
        "--image", image_path,
        "--name_image", name_image
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    # Print the output and error (if any)
    # print("Return code:", result.returncode)
    print("Output:")
    print(result.stdout)
    print("Error:")
    print(result.stderr)



def cpu_intensive_operation(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        for _ in range(1000):
            for _ in range(1000):
                _ = 1 + 1 

# Mouse callback function to set the ROI
def set_roi(event, x, y, flags, param):
    global roi_x1, roi_x2, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        roi_x1 = x
        roi_x2 = x
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            roi_x2 = x
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi_x2 = x

def check_roi_crossing(box, roi_x1, roi_x2, frame_height):
    # Check if the box crosses 50% or more of the ROI
    x1, y1, x2, y2 = box
    box_width = x2 - x1
    box_crossed = (x2 > roi_x1 and x1 < roi_x2) and ((x2 - roi_x1) / box_width >= 0.8)
    return box_crossed

def check_body_coverage(keypoints):
    if keypoints is not None:
        keypoint_names = [
                "Nose", "Left Eye", "Right Eye", "Left Ear", "Right Ear",
                "Left Shoulder", "Right Shoulder", "Left Elbow", "Right Elbow",
                "Left Wrist", "Right Wrist", "Left Hip", "Right Hip",
                "Left Knee", "Right Knee", "Left Ankle", "Right Ankle"
        ]

        indices_to_check = [5, 6, 13, 14]
        
        visible_keypoints_mask = keypoints.conf > 0.5
        visible_keypoints_mask = visible_keypoints_mask[0].cpu().numpy()

        check = all(visible_keypoints_mask[idx] for idx in indices_to_check)
        # if check:
        #     print("true")
        # else: 
        #     print("false")
        return check

    else:
        return False

def take_screenshot(frame, box):
    x1, y1, x2, y2 = map(int, box)
    cropped_frame = frame[y1:y2, x1:x2]
    timestamp = str(datetime.now()).replace(' ', '')
    # print(date)
    universal.date = timestamp[:10]
    universal.time = timestamp[10:18]
    filename = f"screenshot_1.png"
    cwd=os.getcwd()
    image_path=os.path.join(cwd,'tmp',filename)
    cv2.imwrite(image_path, cropped_frame)
    print(f"Screenshot taken: {filename}")
    return image_path,filename


class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

if __name__ == '__main__':
    mp.set_start_method('spawn')
    
    processes = []
    max_processes = 6



    url = sys.argv[1]

    cv2.namedWindow('YOLOv8')
    cv2.setMouseCallback('YOLOv8', set_roi)

    # Load YOLOv8 model after setting multiprocessing context
    model = YOLO(r'model/yolov8n-pose.pt')
    logging.getLogger('ultralytics').setLevel(logging.CRITICAL)



    #For Phone Camera
    while True:
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        frame = imutils.resize(frame, width=1000, height=1800)


        # Perform detection and tracking with suppressed output
        with SuppressOutput():
            results = model.track(frame, persist=True)

        # Get the detected bounding boxes and labels
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            keypoints = results[0].keypoints
            ids = results[0].boxes.id
            ids = ids.cpu().numpy() if ids is not None else np.array([])

            classes = results[0].boxes.cls.cpu().numpy()

            frame_height, frame_width = frame.shape[:2]

            current_time = time.time()

            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = box[:4]
                track_id = ids[i] if len(ids) > 0 else None
                class_id = int(classes[i])

                # Process only human class (class_id == 0)
                if class_id == 0:
                    if roi_x1 is not None and roi_x2 is not None and check_roi_crossing((x1, y1, x2, y2), roi_x1, roi_x2, frame_height) and check_body_coverage(keypoints=keypoints):
                        if track_id not in captured_boxes:

                            if len(processes) < max_processes:
                                image,name_image=take_screenshot(frame, (x1, y1, x2, y2))
                                p = mp.Process(target=process_screenshot, args=(image,name_image,))
                                p.start()
                                processes.append(p)
                                captured_boxes.append(track_id)
                                last_screenshot_time = current_time
                                roi_crossed = True
                                print("Yeah")
                            else:
                                print("Queue full!")
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                # Draw track ID if available
                    if track_id is not None:
                        cv2.putText(frame, f'ID: {track_id}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Check for finished processes
            for p in processes[:]:
                if not p.is_alive():
                    processes.remove(p)

        # Reset the ROI color after 0.1 seconds
        if last_screenshot_time and current_time - last_screenshot_time > 0.1:
            roi_crossed = False

        # Draw ROI
        if roi_x1 is not None and roi_x2 is not None:
            color = (255, 255, 0) if not roi_crossed else (0, 0, 255)
            cv2.rectangle(frame, (roi_x1, 0), (roi_x1 + 4, frame_height), color, 2)

        # Display the resulting frame
        cv2.imshow('YOLOv8', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        

    # Release the capture
    cv2.destroyAllWindows()
