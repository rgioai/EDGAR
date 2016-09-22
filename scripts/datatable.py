import pytz
import os
from datetime import datetime

def add_to_table(doc, table):
    l = doc.split('_')
    cik = l[0]
    qtr = l[1]
    l2 = l[2].split('(')
    form = l2[0]
    accession = l2[1].replace(').txt', '')
    row = '%s,%s,%s,%s' % (cik, qtr, form, accession)
    row += add_data(doc)
    return row
    #table.write(row)


def add_data(doc):
    return_string = ''
    return_string += ',' + add_acceptance_dtg(doc)
    return return_string


def add_acceptance_dtg(doc):
    d = open(doc, 'r')
    line = d.read().splitlines()[3]
    d.close()
    acceptance_datetime = line.split('>')[1]
    year = acceptance_datetime[:4]
    month = acceptance_datetime[4:6]
    day = acceptance_datetime[6:8]
    hour = acceptance_datetime[8:10]
    minute = acceptance_datetime[10:12]
    second = acceptance_datetime[12:14]
    dtg = datetime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second,
        tzinfo=pytz.pytz.timezone('US/Eastern'))
    return str(dtg)


if __name__ == '__main__':
    os.chdir('/storage')
    datatable = open('dataTable.csv', 'w')

    os.chdir('/storage/cik')

    for t in os.listdir('/storage/cik'):
        for m in os.listdir('/storage/cik/%s' % t):
            for l in os.listdir('/storage/cik/%s/%s' % (t, m)):
                for d in os.listdir('/storage/cik/%s/%s/%s' % (t, m, l)):
                    print(add_to_table(d, datatable))
                    break


