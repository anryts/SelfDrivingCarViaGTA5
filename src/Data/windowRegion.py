class WindowRegion:
    def __init__(self, top_left: tuple[int, int], bottom_right: tuple[int, int], width: int, height: int):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return str(f'Top-left: {self.top_left} \n Bottom-right: {self.bottom_right} \n Width: {self.width} \n Height: {self.height}')
