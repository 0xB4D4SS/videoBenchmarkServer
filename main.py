import os
import socketserver
import sys
from multiprocessing import Process

import datasource


class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self) -> None:
        data = self.request.recv(1024).strip()
        print(str(data))
        if data:
            # self.request.sendall(bytes(Base.sdata))
            print(Base.sdata)


class Server(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)


class Base:

    # TODO: get data from file and send it through tcp server
    sdata = ""

    def runall(self):
        # streamProcess = Process(target=self.stream, args=('rtsp://rtsp.stream/pattern',))
        # streamProcess.start()
        # streamProcess.join()
        dataProcess = Process(target=self.getData)
        dataProcess.start()
        serverProcess = Process(target=self.run_server)
        serverProcess.start()
        serverProcess.join()

    def getData(self):
        ds = datasource.DataSource('ffreport.log')
        Base.sdata = ds.readData()

    def run_server(self):

        server = Server(("127.0.0.1", 5000), RequestHandler)
        try:
            print("serving")
            server.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)

    @staticmethod
    def stream(source):
        os.environ["FFREPORT"] = "file=ffreport.log:level=32"
        os.system(f"ffmpeg.exe -i {source} -f mpegts udp://127.0.0.1:9991 -loglevel quiet -report")


if __name__ == '__main__':
    base = Base()
    base.runall()
    # streamProcess = Process(target=stream, args=('rtsp://rtsp.stream/pattern',))
    # streamProcess.start()
    # streamProcess.join()
    # dataProcess = Process(target=getData)
    # dataProcess.start()
    # serverProcess = Process(target=run_server)
    # serverProcess.start()
    # serverProcess.join()
