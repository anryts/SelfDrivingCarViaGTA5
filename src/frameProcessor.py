import cv2
import numpy as np


class FrameProcessor:
    def __init__(self, window_name):
        self.window_name = window_name

    def display_window(self, frame: np.ndarray) -> None:
        cv2.imshow(self.window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.close()

    def close(self):
        cv2.destroyAllWindows()
