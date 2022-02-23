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
    data = ""

    def __init__(self, source):
        self.source = source
        self.readData()

    def readData(self):
        file = open(self.source)
        lines = follow(file)
        for line in lines:
            if "frame=" in line:
                self.data = line
