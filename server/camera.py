import glob
import os

import cv2


def _get_created_time_if_exists(file_name):
    try:
        if os.path.getsize(file_name) > 0:
            return os.path.getctime(file_name)
    except OSError:
        return 0


class Camera(object):
    limited = NotImplemented

    def get_next_frame(self):
        raise NotImplementedError


class FileCamera(Camera):
    limited = False

    def __init__(self):
        self.latest_file = None
        self.last_frame = None

    @staticmethod
    def _get_next_file_name():
        file_names = glob.glob('/tmp/images/*.jpg')
        return max(file_names, key=_get_created_time_if_exists)

    def get_next_frame(self):
        latest_file_name = self._get_next_file_name()
        if latest_file_name == self.latest_file:
            return None
        else:
            self.latest_file = latest_file_name
            frame = cv2.imread(latest_file_name)
            _, _buffer = cv2.imencode('.jpg', frame)
            return _buffer.tostring()
