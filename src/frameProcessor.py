import cv2
import numpy as np
import ultralytics


class FrameProcessor:
    def __init__(self, window_name):
        self.window_name = window_name
        self.model = ultralytics.models.yolo.YOLO()  # Load YOLO model
        self.model.to("cuda")

    def display_window(self, frame: np.ndarray) -> None:
        processed_frame = self.process_frame(frame)
        cv2.imshow(self.window_name, processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.close()

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        if frame.shape[2] == 4:  # If the frame has an alpha channel (RGBA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Convert to BGR (3 channels)

        results = self.model(frame, device="cuda", stream=True)  # Run YOLO inference
        for result in results:
            for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
                x1, y1, x2, y2 = map(int, box[:4])  # Extract bounding box coordinates
                label = self.model.names[int(cls)]  # Extract label of box
                frame_text = f"{label}: {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
                cv2.putText(frame, frame_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        return frame

    def close(self):
        cv2.destroyAllWindows()
