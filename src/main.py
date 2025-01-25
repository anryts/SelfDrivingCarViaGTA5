from src.windowManager import WindowManager

if __name__ == '__main__':
    window_manager = WindowManager("Grand Theft Auto V")
    print(window_manager.get_window_coordinates().__str__())
