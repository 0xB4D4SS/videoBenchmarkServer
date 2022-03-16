import os
import socketserver
import socket
import sys
from multiprocessing import Process
import datasource


def run_server(datasrc):
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 5000  # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                req = conn.recv(1024)
                if not req:
                    break
                print(f"Received: {str(req)}")
                data = datasrc.readData()
                conn.sendall(bytes(data, "utf-8"))

    # class RequestHandler(socketserver.BaseRequestHandler):
    #
    #     def handle(self) -> None:
    #         data = datasrc.readData()
    #         self.request.sendall(bytes(data, "utf-8"))
    #
    # class Server(socketserver.TCPServer):
    #     def __init__(self, server_address, RequestHandlerClass):
    #         super().__init__(server_address, RequestHandlerClass)
    #
    # server = Server(("127.0.0.1", 5000), RequestHandler)
    # server.
    # print("serving")
    # server.serve_forever()


def stream(source):
    os.environ["FFREPORT"] = "file=ffreport.log:level=32"
    os.system(f"ffmpeg.exe -i {source} -f mpegts udp://127.0.0.1:9991 -loglevel quiet -report")


if __name__ == '__main__':
    try:
        ds = datasource.DataSource('ffreport.log')

        streamProcess = Process(target=stream, args=('rtsp://rtsp.stream/pattern',))
        streamProcess.start()

        serverProcess = Process(target=run_server, args=(ds,))
        serverProcess.start()
        serverProcess.join()
    except KeyboardInterrupt:
        streamProcess.close()
        serverProcess.close()
        del ds
        sys.exit(0)
