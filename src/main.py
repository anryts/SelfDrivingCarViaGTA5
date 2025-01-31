import numpy as np

from src.dataTransfer import DataTransfer
from src.frameProcessor import FrameProcessor
from src.screenCapture import ScreenCapture
from src.windowManager import WindowManager
from threading import Thread


# Define the pipeline function
def process_pipeline(frame: np.ndarray, data_manager: DataTransfer, frame_processor: FrameProcessor):
    """
    Pipeline function to process a single frame.
    1. Sends the frame to the DataTransfer for inference.
    2. Displays the processed frame using FrameProcessor.
    """
    # Send the frame to ZeroMQ and receive processed data, and then display it
    data_manager.process_frame(frame, frame_processor.display_window)


def main():
    # Initialize the WindowManager to fetch coordinates
    window_manager = WindowManager("Grand Theft Auto V")
    window_coordinates = window_manager.get_window_coordinates()

    # Initialize the core components
    screen_capture = ScreenCapture(window_coordinates, 60)
    frame_processor = FrameProcessor("GTA V - Processor")
    data_manager = DataTransfer()

    screen_capture.capture_stream(frame_processor.display_window)

    # Start the pipeline
    #screen_capture.capture_stream(lambda frame: process_pipeline(frame, data_manager, frame_processor))


if __name__ == '__main__':
    main()
