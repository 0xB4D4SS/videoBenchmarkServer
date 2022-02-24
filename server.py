import socketserver
import datasource


class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self) -> None:
        self.data = self.request.recv(1024).strip()
        print(self.data)
        if self.data:
            # ds = datasource.DataSource("ffreport.log")
            self.request.sendall("hi")
            # del ds


class Server:
    def __init__(self, ip="127.0.0.1", port=5000):
        self.ip = ip
        print(self.ip)
        self.port = port
        print(self.port)

    def serve(self, mode):
        if mode == "tcp":
            print("enabling tcp mode")
            with socketserver.TCPServer((self.ip, self.port), RequestHandler) as server:
                print("serving tcp")
                server.serve_forever()
        elif mode == "udp":
            print("enabling udp mode")
            with socketserver.UDPServer((self.ip, self.port), RequestHandler) as server:
                print("serving udp")
                server.serve_forever()
        else:
            print("Error!")
            exit(1)
