from ftplib import FTP


class FTPInterface(object):
    """
    Interface for an FTP wrapper class.
    """
    def change_dir(self, target):
        raise NotImplemented

    def download(self, target, destination):
        raise NotImplemented

    def upload(self, target, destination):
        raise NotImplemented


class EdgarFtp(FTPInterface):
    """
    FTP wrapper for EDGAR ftp server.
    Note from SEC:
        To preserve equitable server access, we ask that bulk
        FTP transfer requests are performed between 9 PM and 6 AM Eastern time.
    """
    def __init__(self):
        """
        Connects to ftp.sec.gov
        :return: None
        """
        domain_name = 'ftp.sec.gov'  # domain name or server ip:
        # username and password anonymous

        self.ftp = FTP(domain_name)
        self.ftp.login()

    def change_dir(self, target):
        """
        Changes working directory to target
        :param target: str
        :return: None
        """
        self.ftp.cwd(target)

    def download(self, target, destination=''):
        """
        Downloads the file at path target to path destination.
        If destination not specified, destination = target.
        :param target: str
        :param destination: str
        :return: None
        """
        if destination == '':
            destination = target
        local = open(destination, 'wb')
        # TODO Test if this can handle text files too
        self.ftp.retrbinary('RETR ' + target, local.write, 1024)
        local.close()

    def upload(self, target, destination=''):
        """
        Uploads the file at path target to path destination.
        If destination not specified, destination = target.
        :param target: str
        :param destination: str
        :return: None
        """
        if destination == '':
            destination = target
        local = open(destination, 'rb')
        # FUTURE Test if this can handle text files too
        self.ftp.storbinary('STOR ' + target, local)
        local.close()



