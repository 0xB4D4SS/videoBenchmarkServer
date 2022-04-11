import os
import socketserver
import sys
from multiprocessing import Process
import datasource


def run_server(datasrc):

    class RequestHandler(socketserver.BaseRequestHandler):

        def handle(self) -> None:
            data = datasrc.readData()
            self.request.sendall(bytes(data, "utf-8"))

    class Server(socketserver.TCPServer):
        def __init__(self, server_address, RequestHandlerClass):
            super().__init__(server_address, RequestHandlerClass)

    server = Server(("127.0.0.1", 5000), RequestHandler)
    print("serving")
    server.serve_forever()


def stream(source, output):
    os.environ["FFREPORT"] = "file=ffreport.log:level=32"
    os.system(f"ffmpeg.exe -i {source} -f mpegts udp://{output} -loglevel quiet -report")


if __name__ == '__main__':
    ds = datasource.DataSource('ffreport.log')
    streamProcess = Process(target=stream, args=('rtsp://rtsp.stream/pattern', '127.0.0.1:9991'))
    serverProcess = Process(target=run_server, args=(ds,))
    try:
        streamProcess.start()
        serverProcess.start()
        serverProcess.join()
    except KeyboardInterrupt:
        streamProcess.close()
        serverProcess.close()
        del ds
        sys.exit(0)
