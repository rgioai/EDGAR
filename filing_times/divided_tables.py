import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


if __name__ == '__main__':
    complete_datatable = open('datatables/complete.csv', 'w')
    years = {}
    forms = {}
    all = []
    for line in complete_datatable:
        cik, qtr, form, accession, dtg = line.split(',')
        year = qtr.split('Q')
        # 2016-08-03 16:32:32-04:56
        time_string = dtg.split(' ')[1]
        hour = int(time_string.split(':')[0])
        if year not in years.keys():
            years[year] = [hour]
        else:
            years[year].append(hour)
        if form not in forms.keys():
            forms[form] = [hour]
        else:
            forms[form].append(hour)
        all.append(hour)
    complete_datatable.close()

    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    for y in years.keys():
        title = y
        arr = np.array(years[y])
        pp = PdfPages('datatables/by-year/%s.pdf' % title)
        n, b, p = plt.hist(arr, bins)
        plt.xlabel('Hour')
        plt.ylabel('Num_Filings')
        plt.title(title)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    for f in forms.keys():
        title = f
        arr = np.array(forms[f])
        pp = PdfPages('datatables/by-form/%s.pdf' % title)
        n, b, p = plt.hist(arr, bins)
        plt.xlabel('Hour')
        plt.ylabel('Num_Filings')
        plt.title(title)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    title = 'All'
    arr = np.array(all)
    pp = PdfPages('datatables/%s.pdf' % title)
    n, b, p = plt.hist(arr, bins)
    plt.xlabel('Hour')
    plt.ylabel('Num_Filings')
    plt.title(title)
    plt.savefig(pp, format='pdf')
    pp.close()
    plt.close()

