import os
import socket

import server
from multiprocessing import Process


def stream(source):
    os.environ["FFREPORT"] = "file=ffreport.log:level=32"
    os.system(f"ffmpeg.exe -i {source} -f mpegts udp://127.0.0.1:9991 -loglevel quiet -report")


if __name__ == '__main__':
    # streamProcess = Process(target=stream, args=('rtsp://rtsp.stream/pattern',))
    # streamProcess.start()
    # streamProcess.join()
    server = server.Server()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("127.0.0.1", 5000))
        sock.sendall(bytes("getdata\n", "utf-8"))
        result = str(sock.recv(1024), "utf-8")
    print(result)
