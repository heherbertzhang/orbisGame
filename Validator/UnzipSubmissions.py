import zipfile
import os

def unzipSubmissions():
    os.chdir("./Test/")
    files = os.listdir("./")
    for i in files:
		if zipfile.is_zipfile(i):
            with zipfile.ZipFile(i) as zf:
                zf.extractall(i.split('.')[0])


if __name__ == '__main__':
    unzipSubmissions()
