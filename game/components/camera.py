# Import libraries
import cv2
import logging


class Camera:
    def __init__(self, x_axis_crop=None, y_axis_crop=None):
        # Initialize parameters
        self.x_axis_crop = x_axis_crop
        self.y_axis_crop = y_axis_crop

        # Create Video capture object
        self.video_capture = cv2.VideoCapture(0)

    def freeze_frame(self):
        # Take screenshot
        ret, frame = self.video_capture.read()
        # frame = np.rot90(frame)

        if self.x_axis_crop is None or self.y_axis_crop is None:
            # Return the original frame
            return frame
        else:
            # Cropping the taken frame
            new_region = frame[self.x_axis_crop[0]:self.x_axis_crop[1], self.y_axis_crop[0]:self.y_axis_crop[1]]
            cropped_frame = cv2.cvtColor(new_region, cv2.COLOR_BGR2RGB)
            return cropped_frame

    def release(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
