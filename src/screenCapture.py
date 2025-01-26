from typing import Callable
from src.Data.windowRegion import WindowRegion

import mss
import numpy as np
import time


class ScreenCapture:
    def __init__(self, window_region: WindowRegion, target_fps: int = 30):
        self.window_region = window_region
        self.target_fps = target_fps

    def capture_video_frame(self) -> np.ndarray:
        with mss.mss() as sct:
            monitor = {
                "top": self.window_region.top_left[1],
                "left": self.window_region.top_left[0],
                "width": self.window_region.width,
                "height": self.window_region.height,
            }
            frame = np.array(sct.grab(monitor))
            return frame

    def capture_stream(self, callback: Callable[[np.ndarray], None]) -> None:

        frame_interval = 1 / self.target_fps
        last_time = time.time()

        while True:
            frame = self.capture_video_frame()
            callback(frame)

            #Handling an FPS count
            elapsed_time = time.time() - last_time
            time_wait = frame_interval - elapsed_time
            print(f'fps: {1 / elapsed_time}')
            if time_wait > 0:
                time.sleep(time_wait)
            last_time = time.time()
