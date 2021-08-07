import os

dir = os.curdir
file = os.listdir(dir)
for files in file:
	print(files, len(files))