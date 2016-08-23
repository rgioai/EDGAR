from objects.FTP import EdgarFtp
import os
from zipfile import ZipFile

ftp = EdgarFtp()
ftp.change_dir('edgar')
os.chdir('/storage/')

directory = 'full-index/2015/QTR1/'
try:
    os.makedirs(directory)
except FileExistsError:
    pass

ftp.download(directory + 'master.zip')
zip = ZipFile(directory + 'master.zip')
zip.extractall(path=directory)
zip.close()

os.remove(directory + 'master.zip')

