import os


if __name__ == '__main__':
    years = []
    forms = []

    os.chdir('/storage/cik')

    for t in os.listdir('/storage/cik'):
        if t == 'metadata':
            continue
        for m in os.listdir('/storage/cik/%s' % t):
            for l in os.listdir('/storage/cik/%s/%s' % (t, m)):
                for doc in os.listdir('/storage/cik/%s/%s/%s' % (t, m, l)):
                    path = '/storage/cik/%s/%s/%s' % (t, m, l)
                    l = doc.split('_')
                    cik = l[0]
                    qtr = l[1]
                    year = qtr.split('Q')[0]
                    l2 = l[2].split('(')
                    form = l2[0]
                    accession = l2[1].replace(').txt', '')
                    if year not in years:
                        years.append(year)
                    if form not in forms:
                        forms.append(form)
    f = open('/storage/cik/metadata/forms', 'w')
    for i in forms:
        f.write(i + '\n')
    f.close()
    f = open('/storage/cik/metadata/years', 'w')
    for i in years:
        f.write(i + '\n')
    f.close()
