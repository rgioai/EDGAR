import numpy as np
import datetime as dt

if __name__ == '__main__':
    max_days = (dt.date.today() - dt.date(year=2014, month=1, day=1)).days
    max_hours = 24
    blank = np.zeros((max_days, max_hours))
    # FUTURE Break this out by form

    complete_datatable = open('datatables/complete.csv', 'r')

    for line in complete_datatable:
        try:
            cik, qtr, form, accession, dtg = line.split(',')
        except ValueError:
            continue
        filing_dt = dt.datetime.strptime(dtg[:-7], '%Y-%m-%d %H:%M:%S')
        filing_date = dt.date(year=filing_dt.year, month=filing_dt.month, day=filing_dt.day)
        y_index = filing_dt.hour
        x_index = (dt.date.today() - filing_date).days

        blank[x_index][y_index] += 1

    complete_datatable.close()

    blank_row = np.zeros(24)
    empty_rows = []
    for i in range(len(blank)):
        row = blank[i]
        if np.sum(row) == 0:
            empty_rows.append(i)
    print(empty_rows)
    for i in reversed(empty_rows):
        blank = np.delete(blank, i, 0)

    by_hour = np.transpose(blank)

    out = open('by-hour.csv', 'w')
    out.write('hour,mean,std,95_high,max\n')

    for h in range(24):
        values = by_hour[h]
        mean = np.mean(values)
        std = np.std(values)
        high = mean + (1.96 * std)
        low = mean - (1.96 * std)
        maximum = np.amax(values)
        minimum = np.amin(values)
        out.write('%d,%d,%d,%d,%d\n' % (h, mean, std, high, maximum))

    out.close()
