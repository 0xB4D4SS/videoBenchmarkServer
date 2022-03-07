import time


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


class DataSource:

    def __init__(self, source):
        self.source = source

    def readData(self):
        file = open(self.source)
        lines = follow(file)
        for line in lines:
            if "frame=" in line:
                return line
