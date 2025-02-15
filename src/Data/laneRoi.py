import numpy
from numpy.ma.extras import average


class LaneRoi:
    """
    Represents two points (average from all detected lines)
    To draw a roi which is just intersection between them
    """

    def __init__(self, left_lines: [], right_lines: []) -> None:
        self.avg_left_line = self.find_average(left_lines).flatten()
        self.avg_right_line = self.find_average(right_lines).flatten()

    def find_average(self, lines_set: []) -> numpy.ndarray:
        """
        Find average for lines set
        :param lines_set: numpy array, with the next structure -> [x1, y1, x2, y2]
        :return:
        """
        lines_set_np = numpy.array(lines_set)
        return average(lines_set_np, axis=0)

    def find_intersection(self) -> tuple[int, int]:
        """
        Find an intersection between two lines. which is already in this object
        :return:
        tuple which stends for (x, y) coord
        """
        try:
            l_x, l_y = self.avg_left_line[2:]
            r_x, r_y = self.avg_right_line[2:]
            x_int = int((r_y - l_y) / (l_x - r_y))
            y_int = int(l_x * x_int + l_y)
            return x_int, y_int
        except ValueError as error:
            print(error.__str__())

        # if l_x == r_x:
        #     ValueError("Lines are parallel")
