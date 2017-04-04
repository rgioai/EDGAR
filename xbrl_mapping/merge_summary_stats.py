import os


if __name__ == '__main__':

    DATA_DIR = '/storage/xbrl_reporting'

    target_file = open('all_summ_stats.csv', 'w')
    target_file.write('vec_len,category,dist_fn,top_n,n,min,max,mean,std,med\n')

    for fname in os.listdir(DATA_DIR):
        if 'summary_stats' in fname:
            vlen = fname.split('_')[1]
            cat = fname[18:].replace('_summary_stats.csv', '')

            with open('%s/%s' % (DATA_DIR, fname), 'r') as f:
                lines = f.readlines()[1:]
                for l in lines:
                    target_file.write('%s,%s,%s' % (vlen, cat, l))
    target_file.close()

