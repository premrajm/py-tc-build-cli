import os


def create_and_open(filename, mode):
    if "/" in filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    return open(filename, mode)


def writeFile(filename, content):
    file = create_and_open(filename, 'w')
    file.write(content)
    file.close()