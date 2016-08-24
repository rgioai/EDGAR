from ftplib import FTP


class FTPInterface(object):
    def change_dir(self, target):
        raise NotImplemented

    def download(self, target, destination):
        raise NotImplemented

    def upload(self, target, destination):
        raise NotImplemented


class EdgarFtp(FTPInterface):
    def __init__(self):
        domain_name = 'ftp.sec.gov'  # domain name or server ip:
        # username and password anonymous

        self.ftp = FTP(domain_name)
        self.ftp.login()

    def change_dir(self, target):
        self.ftp.cwd(target)

    def download(self, target, destination=''):
        if destination == '':
            destination = target
        local = open(destination, 'wb')
        # TODO Test if this can handle text files too
        self.ftp.retrbinary('RETR ' + target, local.write, 1024)
        local.close()

    def upload(self, target, destination=''):
        if destination == '':
            destination = target
        local = open(destination, 'rb')
        # FUTURE Test if this can handle text files too
        self.ftp.storbinary('STOR ' + target, local)
        local.close()


# To preserve equitable server access, we ask that bulk
# FTP transfer requests are performed between 9 PM and 6 AM Eastern time.
