import os
import socket

HOST = '0.0.0.0'
PORT = 5001
ADDR = (HOST, PORT)
chunksize = 4096

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(ADDR)
serv.listen(5)

print 'listening ...'

file_counter = 0
while True:
    conn, _ = serv.accept()
    tmp = "/tmp/images/.tmp"
    with open(tmp, 'w') as f:
        while True:
            data = conn.recv(chunksize)
            if not data: break
            f.write(str(data))
    dst = "/tmp/images/{}.jpg".format(file_counter)
    os.rename(tmp, dst)
    file_counter += 1
    conn.close()
