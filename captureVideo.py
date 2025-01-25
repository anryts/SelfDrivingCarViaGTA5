import cv2

class VideoCapturing:

    def __init__(self, width: int, height: int, framerate: int):
        self.width = width
        self.height = height
        self.framerate = framerate
    def capture_frames(self) -> None:
        # Capture video from the camera
        cap = cv2.VideoCapture(0)
        # Check if the camera is opened correctly
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        # Capture video frame by frame
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release the camera
        cap.release()
        # Close all windows
        cv2.destroyAllWindows()

    def get_info(self) -> str:
        return cv2.__version__
