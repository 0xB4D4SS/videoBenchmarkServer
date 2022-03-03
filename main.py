import os
import socketserver
import sys
from multiprocessing import Process
import datasource


def run_server():
    class RequestHandler(socketserver.BaseRequestHandler):

        def handle(self) -> None:
            data = datasource.DataSource.currdata
            print(datasource.DataSource.currdata)
            self.request.sendall(bytes(data, "utf-8"))

    class Server(socketserver.TCPServer):
        def __init__(self, server_address, RequestHandlerClass):
            super().__init__(server_address, RequestHandlerClass)

    server = Server(("127.0.0.1", 5000), RequestHandler)
    try:
        print("serving")
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


def getData():
    ds.readData()


def stream(source):
    os.environ["FFREPORT"] = "file=ffreport.log:level=32"
    os.system(f"ffmpeg.exe -i {source} -f mpegts udp://127.0.0.1:9991 -loglevel quiet -report")


if __name__ == '__main__':
    ds = datasource.DataSource('ffreport.log')
    streamProcess = Process(target=stream, args=('rtsp://rtsp.stream/pattern',))
    streamProcess.start()
    # streamProcess.join()
    # dataProcess = Process(target=getData)
    # dataProcess.start()
    serverProcess = Process(target=run_server)
    serverProcess.start()
    serverProcess.join()
    while True:
        try:
            getData()
        except KeyboardInterrupt:
            sys.exit(0)
