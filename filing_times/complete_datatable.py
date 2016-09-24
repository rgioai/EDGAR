import pytz
import os
from datetime import datetime


def add_to_table(doc, path, table):
    l = doc.split('_')
    cik = l[0]
    qtr = l[1]
    l2 = l[2].split('(')
    form = l2[0]
    accession = l2[1].replace(').txt', '')
    row = '%s,%s,%s,%s' % (cik, qtr, form, accession)
    row += add_data(doc, path)
    table.write(row + '\n')


def add_data(doc, path):
    return_string = ''
    try:
        return_string += ',' + add_acceptance_dtg(doc, path)
    except IndexError:
        pass
    return return_string


def add_acceptance_dtg(doc, path):
    d = open(path + '/' + doc, 'r')
    line = d.read().splitlines()[2]
    d.close()
    acceptance_datetime = line.split('>')[1]
    year = int(acceptance_datetime[:4])
    month = int(acceptance_datetime[4:6])
    day = int(acceptance_datetime[6:8])
    hour = int(acceptance_datetime[8:10])
    minute = int(acceptance_datetime[10:12])
    second = int(acceptance_datetime[12:14])
    dtg = datetime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second,
        tzinfo=pytz.timezone('US/Eastern'))
    return str(dtg)


if __name__ == '__main__':

    datatable = open('datatables/complete.csv', 'w')

    os.chdir('/storage/cik')

    for t in os.listdir('/storage/cik'):
        for m in os.listdir('/storage/cik/%s' % t):
            for l in os.listdir('/storage/cik/%s/%s' % (t, m)):
                for d in os.listdir('/storage/cik/%s/%s/%s' % (t, m, l)):
                    path = '/storage/cik/%s/%s/%s' % (t, m, l)
                    add_to_table(d, path, datatable)
    datatable.close()


