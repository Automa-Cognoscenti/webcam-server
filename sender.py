import socket
import sys
from threading import (
    Lock,
    Thread,
)

import cv2


class WebcamVideoStream(object):
    def __init__(self, src=0, width=640, height=480):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()
        self.thread = None

    def start(self):
        if self.started:
            print "already started!!"
            return None

        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()


def chunks(lst, n):
    "Yield successive n-sized chunks from lst"
    for i in xrange(0, len(lst), n):
        yield lst[i:i + n]


def write(server_ip, server_port):
    vs = WebcamVideoStream().start()
    try:
        while True:
            _frame = vs.read()
            if _frame is None:
                continue
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server_ip, server_port))
            _, b = cv2.imencode('.jpg', _frame)
            client.send(b)
            client.close()

    except KeyboardInterrupt:
        vs.stop()


if __name__ == '__main__':
    write(sys.argv[1], int(sys.argv[2]))
