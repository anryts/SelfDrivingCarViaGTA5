from typing import Callable

import numpy as np
import time
import zmq


class DataTransfer:
    def __init__(self):
        self.context_send = zmq.Context()
        self.sender = self.context_send.socket(zmq.REQ)

        # Bind or connect as appropriate
        self.sender.bind("tcp://localhost:5558")  # For sending frames

    def process_frame(self, frame: np.ndarray, callback: Callable[[np.ndarray], None]) -> None:
        self.sender.send(frame.tobytes())
        print("Frame sent to ZeroMQ")
        try:
            processed_data = self.sender.recv()  # Wait for processed data
            processed_frame = np.frombuffer(processed_data, dtype=np.uint8).reshape(frame.shape)
            callback(processed_frame)
        except Exception as e:
            print(f"Error in processing frame: {e}")
