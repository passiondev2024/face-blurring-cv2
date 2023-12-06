import os
import tkinter as tk
import threading
import cv2
import imutils
import numpy as np

from pyimagesearch.face_blurring import anonymize_face_pixelate, anonymize_face_simple


class FaceBlurringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Blurring App")

        self.capture = None
        self.running = False
        self.thread = None

        self.method = tk.StringVar(value="simple")
        self.input_blocks = tk.IntVar(value=20)
        self.input_confidence = tk.DoubleVar(value=0.5)

        self.create_widgets()

    def create_widgets(self):
        options_frame = tk.Frame(self.root)
        options_frame.pack(pady=10)

        tk.Label(options_frame, text="Blur Method:").grid(row=0, column=0, padx=10)
        self.radiobutton_simple = tk.Radiobutton(options_frame, text="Simple", variable=self.method, value="simple")
        self.radiobutton_simple.grid(row=0, column=1)

        self.radiobutton_pix = tk.Radiobutton(options_frame, text="Pixelated", variable=self.method, value="pixelated")
        self.radiobutton_pix.grid(row=0, column=2)

        tk.Label(options_frame, text="Number of Blocks:").grid(row=1, column=0, padx=10)
        self.input_blocks_entry = tk.Entry(options_frame, textvariable=self.input_blocks)
        self.input_blocks_entry.grid(row=1, column=1)

        tk.Label(options_frame, text="Confidence Threshold:").grid(row=2, column=0, padx=10)
        self.input_confidence_entry = tk.Entry(options_frame, textvariable=self.input_confidence)
        self.input_confidence_entry.grid(row=2, column=1)

        start_button = tk.Button(self.root, text="Start", command=self.start_blurring).pack()

        stop_button = tk.Button(self.root, text="Stop", command=self.stop_blurring).pack()

        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

    def start_blurring(self):
        if not self.running:
            self.input_blocks_entry.config(state="disabled")
            self.input_confidence_entry.config(state="disabled")
            self.radiobutton_simple.config(state="disabled")
            self.radiobutton_pix.config(state="disabled")
            try:
                input_blocks = int(self.input_blocks.get())
                input_confidence = float(self.input_confidence.get())
                if input_confidence <= 0.1:
                    raise Exception
                if input_blocks <= 0 or input_blocks >= 50:
                    raise Exception
            except Exception:
                print(f"Некорректное значение. Введите int и float соответственно.")
                self.input_blocks_entry.config(state="normal")
                self.input_confidence_entry.config(state="normal")
                self.radiobutton_simple.config(state="normal")
                self.radiobutton_pix.config(state="normal")
                return
            self.capture = cv2.VideoCapture(0)
            self.running = True
            self.thread = threading.Thread(target=self.process_video)
            self.thread.start()


    def stop_blurring(self):
        self.running = False
        if self.capture:
            self.capture.release()
            self.capture = None
        cv2.destroyAllWindows()

        self.input_blocks_entry.config(state="normal")
        self.input_confidence_entry.config(state="normal")
        self.radiobutton_simple.config(state="normal")
        self.radiobutton_pix.config(state="normal")


    def process_video(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                continue

            method = self.method.get()
            input_blocks = self.input_blocks.get()
            input_confidence = self.input_confidence.get()

            prototxt_path = os.path.sep.join(["face_detector", "deploy.prototxt"])
            weights_path = os.path.sep.join(["face_detector", "res10_300x300_ssd_iter_140000.caffemodel"])
            net = cv2.dnn.readNet(prototxt_path, weights_path)
            frame = imutils.resize(frame, width=400)
            h, w = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > input_confidence:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    face = frame[startY:endY, startX:endX]
                    if method == "simple":
                        face = anonymize_face_simple(face, factor=3.0)
                    else:
                        face = anonymize_face_pixelate(face, blocks=input_blocks)
                    frame[startY:endY, startX:endX] = face
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.canvas.winfo_width(), self.canvas.winfo_height()))
            photo = tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceBlurringApp(root)
    root.mainloop()
