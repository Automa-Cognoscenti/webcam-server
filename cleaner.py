import glob
import os
import time


def clean_old_files():
    while True:
        list_of_files = glob.glob('/tmp/images/*')
        since = time.time()
        for file_name in list_of_files:
            if since - os.path.getctime(file_name) > 5:
                os.remove(file_name)

        time.sleep(1)


if __name__ == '__main__':
    clean_old_files()
