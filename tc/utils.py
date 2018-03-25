import os

def createAndOpen(filename, mode):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return open(filename, mode)