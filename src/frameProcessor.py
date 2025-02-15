import cv2
import numpy as np
import ultralytics
from numpy.ma.extras import average

from src.Data.laneRoi import LaneRoi


class FrameProcessor:
    def __init__(self, window_name):
        self.window_name = window_name
        self.model = ultralytics.models.yolo.YOLO()  # Load YOLO model
        self.model.to("cuda")

    def display_window(self, frame: np.ndarray) -> None:
        processed_frame = self.process_frame(frame)
        cv2.imshow(self.window_name, processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.close()

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        if frame.shape[2] == 4:  # If the frame has an alpha channel (RGBA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Convert to BGR (3 channels)

        detected_lines = self.lane_detection(frame)
        boundaries = self.compute_lane_lines(detected_lines)

        roi = self.draw_roi(frame, boundaries)
        # try:
        #     cv2.line(frame, (
        #         int(boundaries.avg_left_line[0]), int(boundaries.avg_left_line[1])),
        #              (int(boundaries.avg_left_line[2]), int(boundaries.avg_left_line[3])),
        #              (0, 255, 0), 2)
        #     cv2.line(frame, (
        #         int(boundaries.avg_right_line[0]), int(boundaries.avg_right_line[1])),
        #              (int(boundaries.avg_right_line[2]), int(boundaries.avg_right_line[3])),
        #              (0, 255, 0), 2)
        # except ValueError as error:
        #     print(error.__str__())

        return roi
        # return self.draw_roi(result)

        # results = self.model(frame, device="cuda", stream=True)  # Run YOLO inference
        # for result in results:
        #     for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
        #         x1, y1, x2, y2 = map(int, box[:4])  # Extract bounding box coordinates
        #         label = self.model.names[int(cls)]  # Extract label of box
        #         distance = self.distance_estimators(x2 - x1, y2 - y1)
        #         frame_text = f"{label}: {conf:.2f}\n distance: {distance:.1f}"
        #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
        #         cv2.putText(frame, frame_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        # return frame

    def lane_detection(self, frame: np.ndarray) -> np.ndarray:
        """
        :param frame:
        :return:
        numpy array with detected lines, which will be processed by next steps
        """

        processed_image = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
        processed_image = cv2.GaussianBlur(processed_image, (9, 9), 0)
        processed_image = cv2.Canny(processed_image, 50, 180)
        LINE_LENGTH = 1_000  # as long as you want
        dist_resol = 1
        angel_resol = np.pi / 180
        threshold = 125
        # HoughLines - returns a numpy array, of shape (n, 1, 2)
        lines = cv2.HoughLinesP(processed_image, rho=dist_resol, theta=angel_resol, threshold=threshold,
                                minLineLength=25, maxLineGap=50)
        return lines
        # for line in lines:
        #     x1, y1, x2, y2 = line[0]
        #     cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # # rho -> the distance from the origin (top left of the image) to the line
        # # theta -> the angle between the x-axis and the line normal
        # rho, theta = line[0]
        #
        # # Next step convert result from polar coordinated to Cartesian
        # x0 = rho * np.cos(theta)
        # y0 = rho * np.sin(theta)
        #
        # x1 = x0 + LINE_LENGTH * np.sin(-theta)
        # y1 = y0 + LINE_LENGTH * np.cos(theta)
        #
        # x2 = x0 - LINE_LENGTH * np.sin(-theta)
        # y2 = y0 - LINE_LENGTH * np.cos(theta)
        #
        # cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        # return frame

    def draw_roi(self, frame: np.ndarray, boundaries: LaneRoi) -> np.ndarray:
        """
        :param frame: image from game
        :param boundaries: detected average line
        :return:
        """
        height, width = frame.shape[:2]

        intersection_point = boundaries.find_intersection()

        # Just for TEST
        try:
            roi_corners = np.array([
                [intersection_point],  # Top point
                [boundaries.avg_left_line[2:]],  # Bottom-right point
                [boundaries.avg_right_line[2:]]  # Bottom-left point
            ], np.int32)

            # Reshape for fillPoly, which expects an array of shape (num_points, 1, 2)
            roi_corners = roi_corners.reshape((-1, 1, 2))

            # Create an overlay image (copy of the original frame)
            overlay = frame.copy()
            # Fill the polygon on the overlay with a color (e.g., green)
            cv2.fillPoly(overlay, [roi_corners], (0, 255, 0))

            # Blend the overlay with the original frame for a semi-transparent effect
            alpha = 0.3  # Transparency factor
            output = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
            return output
        except ValueError as error:
            print(error.__str__())

        return frame

    def compute_lane_lines(self, detected_lines) -> LaneRoi:
        left_lines = []
        right_lines = []
        for line in detected_lines:
            x1, y1, x2, y2 = line[0]
            # Compute the slope (to know direction)
            slope = (y2 - y1) / (x2 - x1 + 1e-6)  # avoid dividing by zero
            if slope > 0:  # right direction
                right_lines.append(line)
            else:
                left_lines.append(line)

        # Average each line
        lane_roi = LaneRoi(left_lines, right_lines)

        return lane_roi

    @staticmethod
    def distance_estimators(bbox_width: int, bbox_height: int) -> float:
        """
            Just for local test !!!
        :param bbox_width:
        :param bbox_height:
        :return:
        """
        focal_length = 1000  # Example focal length
        known_width = 2.0  # Approximate width of the car (in meters)
        distance: float = (known_width * focal_length) / bbox_width
        return distance

    def close(self) -> None:
        cv2.destroyAllWindows()
