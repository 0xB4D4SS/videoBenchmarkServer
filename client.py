import socket


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 5000))
    sock.sendall(bytes("getdata\n", "utf-8"))
    result = str(sock.recv(1024), "utf-8")
    print(result)


if __name__ == '__main__':
    client()
