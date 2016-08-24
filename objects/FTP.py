from ftplib import FTP


class EdgarFtp(object):
    def __init__(self):
        domain_name = 'ftp.sec.gov'  # domain name or server ip:
        # username and password anonymous

        self.ftp = FTP(domain_name)
        self.ftp.login()

    def change_dir(self, target):
        self.ftp.cwd(target)

    def download(self, filename, target=''):
        if target == '':
            target = filename
        local = open(target, 'wb')
        self.ftp.retrbinary('RETR ' + filename, local.write, 1024)
        local.close()

    def upload(self, filename):
        self.ftp.storbinary('STOR ' + filename, open(filename, 'rb'))


# To preserve equitable server access, we ask that bulk
# FTP transfer requests are performed between 9 PM and 6 AM Eastern time.
