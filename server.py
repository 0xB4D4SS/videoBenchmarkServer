import socketserver
import datasource


class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self) -> None:
        self.data = self.request.recv(1024).strip()
        if self.data:
            ds = datasource.DataSource("ffreport.log")
            self.request.sendall(ds.data)
            del ds


class Server:
    def __init__(self, mode="tcp", ip="127.0.0.1", port=5000):
        self.ip = ip
        self.port = port
        if mode == "tcp":
            with socketserver.TCPServer((self.ip, self.port), RequestHandler) as server:
                server.serve_forever()
        elif mode == "udp":
            with socketserver.UDPServer((self.ip, self.port), RequestHandler) as server:
                server.serve_forever()
        else:
            print("Error!")
            exit(1)
