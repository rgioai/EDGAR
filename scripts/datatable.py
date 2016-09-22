import os


def add_to_table(doc, table):
    l = doc.split('_')
    cik = l[0]
    qtr = l[1]
    l2 = l[2].split('(')
    form = l2[0]
    accession = l2[1].replace(').txt', '')
    row = '%s,%s,%s,%s' % (cik, qtr, form, accession)
    return row


if __name__ == '__main__':
    os.chdir('/storage')
    datatable = open('dataTable.csv', 'w')

    os.chdir('/storage/cik')

    for t in os.listdir('/storage/cik'):
        for m in os.listdir('/storage/cik/%s' % t):
            for l in os.listdir('/storage/cik/%s/%s' % (t, m)):
                for d in os.listdir('/storage/cik/%s/%s/%s' % (t, m, l)):
                    print(add_to_table(d, datatable))


