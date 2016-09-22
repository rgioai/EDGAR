from robobrowser import RoboBrowser
from zipfile import ZipFile
import os


def download_and_unzip(url):
    url = 'https://' + url
    l = url.split('/')
    zip_name = l[len(l)-1]
    csv_name = zip_name.replace('.zip', '.csv')

    if not os.path.exists(csv_name):
        browser = RoboBrowser(history=False, allow_redirects=True)
        request = browser.session.get(url, stream=True)

        with open(zip_name, "wb") as f:
            f.write(request.content)
            f.close()
        try:
            zipped = ZipFile(zip_name)
            zipped.extractall()
            zipped.close()

            os.remove(zip_name)
            print("Collecting: %s" % csv_name)
        except zipfile.BadZipFile:
            pass
    else:
        print("Collected: %s" % csv_name)


if __name__ == '__main__':
    with open('logfiles', 'r') as f:
        logs = f.read()
        f.close()
    logs = logs.split(' ')

    os.chdir('/storage/sec_logs')

    total = len(logs)
    for l in logs:
        download_and_unzip(l)



