import os
import socket
import socketserver
import sys
from multiprocessing import Process


def run_tcp():
    class RequestHandler(socketserver.BaseRequestHandler):

        def handle(self) -> None:
            self.data = self.request.recv(1024).strip()
            print(self.data)
            if self.data:
                # ds = datasource.DataSource("ffreport.log")
                self.request.sendall("hi")
                # del ds

    class Server(socketserver.TCPServer):
        def __init__(self, server_address, RequestHandlerClass):
            super().__init__(server_address, RequestHandlerClass)

    server = Server(("127.0.0.1", 5000), RequestHandler)
    try:
        print("serving")
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

        # def serve(self, mode):
        #     if mode == "tcp":
        #         print("enabling tcp mode")
        #         with socketserver.TCPServer(self.server_address, RequestHandler) as server:
        #             print("serving tcp")
        #             server.handle_request()
        #     elif mode == "udp":
        #         print("enabling udp mode")
        #         with socketserver.UDPServer(self.server_address, RequestHandler) as server:
        #             print("serving udp")
        #             server.handle_request()
        #     else:
        #         print("Error!")
        #         exit(1)


def stream(source):
    os.environ["FFREPORT"] = "file=ffreport.log:level=32"
    os.system(f"ffmpeg.exe -i {source} -f mpegts udp://127.0.0.1:9991 -loglevel quiet -report")


if __name__ == '__main__':
    # streamProcess = Process(target=stream, args=('rtsp://rtsp.stream/pattern',))
    # streamProcess.start()
    # streamProcess.join()
    # serv = Server(("127.0.0.1", 5000), RequestHandler)
    # serv.serve("tcp")
    run_tcp()
    # serverProcess = Process(target=server.serve, args=('tcp',))
    # serverProcess.start()
    # serverProcess.join()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("127.0.0.1", 5000))
        sock.sendall(bytes("getdata\n", "utf-8"))
        result = str(sock.recv(1024), "utf-8")
        print(result)
    except IOError:
        sys.exit(0)
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #     print("lol")
    #     sock.connect(("127.0.0.1", 5000))
    #     print(sock.__str__())
    #     sock.sendall(bytes("getdata\n", "utf-8"))
    #     result = str(sock.recv(1024), "utf-8")
    # print(result)
