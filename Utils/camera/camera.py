"""
utils/camera/camera.py
----------------------
Simple camera controller for TARS.
"""
import cv2

class CameraController:
    def __init__(self):
        self.cap = None
        self.active = False

    def open_camera(self):
        if self.active:
            return "Camera already running."
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return "⚠️ Could not access the camera."
        self.active = True
        print("📸 Camera feed started. Press 'q' to close.")
        while self.active:
            ret, frame = self.cap.read()
            if not ret:
                break
            cv2.imshow("TARS Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.close_camera()
        return "Camera closed successfully."

    def close_camera(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
        self.active = False
        print("🛑 Camera closed.")

controller = CameraController()

def open_camera_threaded():
    import threading
    threading.Thread(target=controller.open_camera, daemon=True).start()
    return "Camera opened."

def close_camera():
    controller.close_camera()
    return "Camera closed."
