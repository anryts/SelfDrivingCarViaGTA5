import captureVideo
from captureVideo import VideoCapturing

if __name__ == '__main__':
    captureVideo = VideoCapturing(480, 640, 30)
    print(captureVideo.get_info())
    captureVideo.capture_frames()
