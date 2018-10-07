from subprocess import Popen
import sys

filename = sys.argv[1]
while True:
    p = Popen("python3 " + filename, shell=True)
    p.wait()
