import os


def createAndOpen(filename, mode):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return open(filename, mode)


def writeFile(filename, content):
    file = createAndOpen(filename, 'w')
    file.write(content)
    file.close()