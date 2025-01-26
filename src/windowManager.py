import pygetwindow as gw

from src.Data.windowRegion import WindowRegion


class WindowManager:
    def __init__(self, window_name: str):
        self.window_name = window_name

    def get_window_coordinates(self) -> WindowRegion:
        try:
            window = gw.getWindowsWithTitle(self.window_name)[0]
            size: tuple[int, int] = window.size
            top_left: tuple[int, int] = window.topleft
            bottom_right: tuple[int, int] = window.bottomright
            return WindowRegion(top_left, bottom_right, size[0], size[1])
        except Exception as ex:
            print(f'Seems like An window with name {self.window_name} was not found \n'
                  f'Error description: {ex.__str__()}')

