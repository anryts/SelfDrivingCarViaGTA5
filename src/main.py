from src.frameProcessor import FrameProcessor
from src.screenCapture import ScreenCapture
from src.windowManager import WindowManager

if __name__ == '__main__':
    window_manager = WindowManager("Grand Theft Auto V")
    screen_capture = ScreenCapture(window_manager.get_window_coordinates(), 60)
    frame_processor = FrameProcessor("GTA V - Processor")
    screen_capture.capture_stream(frame_processor.display_window)
