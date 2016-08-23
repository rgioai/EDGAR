import csv


class IndexFile(object):
    def __init__(self, year, qtr, file):
        self.directory = 'full-index/' + str(year) + '/QTR' + str(qtr) + '/'
        self.file = file + '.idx'
        # TODO
        with open(self.directory + self.file, newline='') as idxfile:
            idxreader = csv.reader(idxfile, delimiter="|")
