import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
import string
import random  # <-- Tambahkan baris ini
import signal

# Global variables untuk penanganan interrupt
interrupted = False

def signal_handler(sig, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

# Fungsi untuk membaca coco.names
def load_classes(class_file):
    with open(class_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return classes

def detect_objects(frame, net, layer_names, classes):
    height, width = frame.shape[:2]
    
    # Blob parameter optimasi
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (320, 320), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    class_ids = []
    confidences = []
    boxes = []

    # Ambang batas untuk deteksi
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Optimasi NMS
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
    # Gambar bounding box dan label
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = classes[class_ids[i]]  # Menggunakan nama kelas dari coco.names
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return frame

def select_video():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])

def main():
    # Muat kelas dari coco.names
    classes = load_classes("coco.names")
    
    # Gunakan model yang lebih ringan (YOLOv3-tiny)
    net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    video_path = select_video()
    if not video_path:
        print("Tidak ada file video yang dipilih.")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Gagal membuka video.")
        return

    # Persiapan output
    output_dir = "videos"
    os.makedirs(output_dir, exist_ok=True)
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".avi"
    output_path = os.path.join(output_dir, random_name)

    # VideoWriter settings optimasi
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Frame skipping untuk meningkatkan FPS
    frame_skip = 4  # Ganti angka ini untuk skip lebih banyak frame
    
    try:
        out = cv2.VideoWriter(output_path, fourcc, fps/(frame_skip+1), (width, height))
        frame_count = 0
        
        while cap.isOpened() and not interrupted:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 4
            if frame_count % (frame_skip+4) != 0:
                continue
                
            processed_frame = detect_objects(frame, net, layer_names, classes)
            
            cv2.imshow("Detected Video", processed_frame)
            out.write(processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Pastikan semua resource dilepas dengan benar
        cap.release()
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()
        print(f"Video tersimpan di: {output_path} (mungkin lebih pendek dari aslinya)")

if __name__ == "__main__":
    main()





