#!/usr/bin/env python3

import numpy as np
from seq2vec import HashSeq2Vec
from joblib import Parallel, delayed
import sys
import h5py
import os


def raw_file_list(tld_path):
    tld_path += '/financial_statement_data'
    raw_files = []
    for quarter_dir in os.listdir(tld_path):
        if quarter_dir == '.DS_Store':
            continue
        if 'tag.txt' in os.listdir('%s/%s' % (tld_path, quarter_dir)):
            raw_files.append('%s/tag.txt' % quarter_dir)
    return raw_files


def make_master_file(tld_path):
    master_file = open('%s/master_tags.txt' % tld_path, 'w')
    for sub_file in raw_file_list(tld_path):
        with open('%s/financial_statement_data/%s' % (tld_path, sub_file), 'r', encoding='utf-8', errors='ignore') as f:
            try:
                for line in f:
                    if line[:3] != 'tag':
                        master_file.write(line)
            except UnicodeDecodeError as e:
                print(e)
                print('%s/financial_statement_data/%s' % (tld_path, sub_file))
            f.close()
    master_file.close()


def test_master_file(tld_path):
    master_file = open('%s/master_tags.txt' % tld_path, 'r')
    line = master_file.readline()
    print(line)
    print(line == line.replace('\n', ''))
    print(line.split('\t'))
    master_file.close()


def make_category_files(tld_path):
    master_file = open('%s/master_tags.txt' % tld_path, 'r')
    if not os.path.exists('%s/non_sc_files' % tld_path):
        os.mkdir('%s/non_sc_files' % tld_path)
    category_files = {'abstract':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'abstract'), 'w'),
                      'monetary_credit_point':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'monetary_credit_point'), 'w'),
                      'monetary_credit_duration':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'monetary_credit_duration'), 'w'),
                      'monetary_debit_point':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'monetary_debit_point'), 'w'),
                      'monetary_debit_duration':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'monetary_debit_duration'), 'w'),
                      'monetary_unk_point':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'monetary_unk_point'), 'w'),
                      'monetary_unk_duration':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'monetary_unk_duration'), 'w'),
                      'nonmonetary_point':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'nonmonetary_point'), 'w'),
                      'nonmonetary_duration':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'nonmonetary_duration'), 'w'),
                      'inconsistent':
                          open('%s/non_sc_files/%s.txt' % (tld_path, 'inconsistent'), 'w')}
    for line in master_file:
        category, value, standard = process_line(line)
        if type(category) == str:
            category_files[category].write(value + '\n')
    master_file.close()
    for k in category_files.keys():
        category_files[k].close()


def make_sc_category_files(tld_path):
    master_file = open('%s/master_tags.txt' % tld_path, 'r')
    if not os.path.exists('%s/sc_files' % tld_path):
        os.mkdir('%s/sc_files' % tld_path)
    s_category_files = {'abstract':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_abstract'), 'w'),
                        'monetary_credit_point':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_monetary_credit_point'), 'w'),
                        'monetary_credit_duration':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_monetary_credit_duration'), 'w'),
                        'monetary_debit_point':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_monetary_debit_point'), 'w'),
                        'monetary_debit_duration':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_monetary_debit_duration'), 'w'),
                        'monetary_unk_point':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_monetary_unk_point'), 'w'),
                        'monetary_unk_duration':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_monetary_unk_duration'), 'w'),
                        'nonmonetary_point':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_nonmonetary_point'), 'w'),
                        'nonmonetary_duration':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_nonmonetary_duration'), 'w'),
                        'inconsistent':
                            open('%s/sc_files/%s.txt' % (tld_path, 's_inconsistent'), 'w')}
    c_category_files = {'abstract':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_abstract'), 'w'),
                        'monetary_credit_point':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_monetary_credit_point'), 'w'),
                        'monetary_credit_duration':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_monetary_credit_duration'), 'w'),
                        'monetary_debit_point':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_monetary_debit_point'), 'w'),
                        'monetary_debit_duration':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_monetary_debit_duration'), 'w'),
                        'monetary_unk_point':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_monetary_unk_point'), 'w'),
                        'monetary_unk_duration':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_monetary_unk_duration'), 'w'),
                        'nonmonetary_point':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_nonmonetary_point'), 'w'),
                        'nonmonetary_duration':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_nonmonetary_duration'), 'w'),
                        'inconsistent':
                            open('%s/sc_files/%s.txt' % (tld_path, 'c_inconsistent'), 'w')}
    for line in master_file:
        category, value, standard = process_line(line)
        if type(category) == str:
            if standard:
                s_category_files[category].write(value + '\n')
            else:
                c_category_files[category].write(value + '\n')
    master_file.close()
    for k in c_category_files.keys():
        c_category_files[k].close()
    for k in s_category_files.keys():
        s_category_files[k].close()


def process_line(line):
    line_list = line.replace('\n', '').split('\t')
    tag = line_list[0]
    custom = line_list[2]
    standard = (custom == '0')
    abstract = line_list[3]
    datatype = line_list[4]
    iord = line_list[5]
    crdr = line_list[6]
    tlabel = line_list[7]
    doc = line_list[8]
    try:
        return assign_category(abstract, datatype, iord, crdr), '%s; %s; %s' % (tag, tlabel, doc), standard
    except ValueError as e:
        print(e)
        return 'inconsistent', '%s; %s; %s' % (tag, tlabel, doc), standard


def assign_category(abstract, datatype, iord, crdr):
    if abstract == '1':
        return 'abstract'
    elif datatype == 'monetary':
        if crdr == 'C':
            if iord == 'I':
                return 'monetary_credit_point'
            elif iord == 'D':
                return 'monetary_credit_duration'
            else:
                raise ValueError('Invalid iord value: (%s, %s, %s, %s)' % (abstract, datatype, iord, crdr))
        elif crdr == 'D':
            if iord == 'I':
                return 'monetary_debit_point'
            elif iord == 'D':
                return 'monetary_debit_duration'
            else:
                raise ValueError('Invalid iord value: (%s, %s, %s, %s)' % (abstract, datatype, iord, crdr))
        else:
            if iord == 'I':
                return 'monetary_unk_point'
            elif iord == 'D':
                return 'monetary_unk_duration'
            else:
                raise ValueError('Invalid iord value: (%s, %s, %s, %s)' % (abstract, datatype, iord, crdr))
    elif datatype != 'monetary':
        if iord == 'I':
            return 'nonmonetary_point'
        elif iord == 'D':
            return 'nonmonetary_duration'
        else:
            raise ValueError('Invalid iord value: (%s, %s, %s, %s)' % (abstract, datatype, iord, crdr))
    else:
        raise ValueError('Invalid datatype value: (%s, %s, %s, %s)' % (abstract, datatype, iord, crdr))


def make_vector_datasets(tld_path, hdf5, sc_split=False):
    if sc_split:
        tld_path += '/sc_files'
    else:
        tld_path += '/non_sc_files'
    vec_grp = hdf5.require_group('vector')
    for vec_len in [50, 100, 150, 200]:
        grp = vec_grp.require_group(str(vec_len))
        standard_grp = grp.require_group('standard')
        custom_grp = grp.require_group('custom')
        for file_name in os.listdir(tld_path):
            with open('%s/%s' % (tld_path, file_name), 'r') as f:
                lines = np.array(f.readlines(), dtype=h5py.special_dtype(vlen=str))
            if len(lines) <= 0:
                print(file_name, ' empty')
                continue
            category_name = file_name.split('/')[-1].replace('.txt', '')
            print(category_name)
            t = HashSeq2Vec(vec_len)
            vec_array = np.array(Parallel(n_jobs=-1, verbose=0)(delayed(t.transform)([l]) for l in lines),
                                 dtype=np.float32)
            vec_array = np.reshape(vec_array, (len(lines), vec_len))
            if category_name[0] == 's':
                dset = standard_grp.require_group(category_name[2:]).\
                    create_dataset('all_entries', data=vec_array)
            elif category_name[0] == 'c':
                dset = custom_grp.require_group(category_name[2:]).\
                    create_dataset('all_entries', data=vec_array)


def make_vlen_datasets(tld_path, hdf5, sc_split=False):
    text_grp = hdf5.require_group('text')
    standard_grp = text_grp.require_group('standard')
    custom_grp = text_grp.require_group('custom')
    if sc_split:
        tld_path += '/sc_files'
    else:
        tld_path += '/non_sc_files'
    for file_name in os.listdir(tld_path):
        with open('%s/%s' % (tld_path, file_name), 'r') as f:
            lines = np.array(f.readlines(), dtype=h5py.special_dtype(vlen=str))
            if len(lines) <= 0:
                return
        category_name = file_name.split('/')[-1].replace('.txt', '')
        if category_name[0] == 's':
            dset = standard_grp.create_dataset(category_name[2:], data=lines)
        elif category_name[0] == 'c':
            dset = custom_grp.create_dataset(category_name[2:], data=lines)


if __name__ == '__main__':
    DATA_DIR_PATH = '/storage/XBRL_Update'
    # DATA_DIR_PATH = '/Users/ryangiarusso/Desktop/XBRL_Update'
    if '-aw' in sys.argv:
        print('Making master file')
        make_master_file(DATA_DIR_PATH)
        """
        print('')
        print('\rMaking category only database: %s' % 'category files', end='')
        make_category_files(DATA_DIR_PATH)
        cat_f = h5py.File('cat_data.hdf5', 'w')
        print('\rMaking category only database: %s' % 'vlen datasets', end='')
        make_vlen_datasets(DATA_DIR_PATH, cat_f, sc_split=False)
        print('\rMaking category only database: %s' % 'vector datasets', end='')
        make_vector_datasets(DATA_DIR_PATH, cat_f, sc_split=False)
        cat_f.close()
        """
        print('')
        print('\rMaking sc-split database: %s' % 'category files', end='')
        make_sc_category_files(DATA_DIR_PATH)
        sc_f = h5py.File('%s/sc_data.hdf5' % DATA_DIR_PATH, 'w')
        print('\rMaking sc-split database: %s' % 'vlen datasets', end='')
        make_vlen_datasets(DATA_DIR_PATH, sc_f, sc_split=True)
        print('\rMaking sc-split database: %s' % 'vector datasets', end='')
        make_vector_datasets(DATA_DIR_PATH, sc_f, sc_split=True)
        sc_f.close()

    elif '-au' in sys.argv:
        if not os.path.exists('%s/master_tags.txt' % DATA_DIR_PATH):
            print('Making master file')
            make_master_file(DATA_DIR_PATH)

        print('')
        if not os.path.exists('%s/non_sc_files' % DATA_DIR_PATH):
            print('\rMaking category only database: %s' % 'category files', end='')
            make_category_files(DATA_DIR_PATH)
        cat_f = h5py.File('cat_data.hdf5', 'w')
        print('\rMaking category only database: %s' % 'vlen datasets', end='')
        make_vlen_datasets(DATA_DIR_PATH, cat_f, sc_split=False)
        print('\rMaking category only database: %s' % 'vector datasets', end='')
        make_vector_datasets(DATA_DIR_PATH, cat_f, sc_split=False)
        cat_f.close()

        print('')
        if not os.path.exists('%s/sc_files' % DATA_DIR_PATH):
            print('\rMaking sc-split database: %s' % 'category files', end='')
            make_sc_category_files(DATA_DIR_PATH)
        sc_f = h5py.File('sc_data.hdf5', 'w')
        print('\rMaking sc-split database: %s' % 'vlen datasets', end='')
        make_vlen_datasets(DATA_DIR_PATH, sc_f, sc_split=True)
        print('\rMaking sc-split database: %s' % 'vector datasets', end='')
        make_vector_datasets(DATA_DIR_PATH, sc_f, sc_split=True)
        sc_f.close()

    else:
        if '-m' in sys.argv:
            make_master_file(DATA_DIR_PATH)
        if '-catf' in sys.argv:
            make_category_files(DATA_DIR_PATH)
        if '-scf' in sys.argv:
            make_sc_category_files(DATA_DIR_PATH)
        if '-catl' in sys.argv:
            cat_f = h5py.File('cat_data.hdf5', 'r+')
            print('\rMaking category only database: %s' % 'vlen datasets', end='')
            make_vlen_datasets(DATA_DIR_PATH, cat_f, sc_split=False)
            cat_f.close()
        if '-scl' in sys.argv:
            sc_f = h5py.File('sc_data.hdf5', 'r+')
            print('\rMaking sc-split database: %s' % 'vlen datasets', end='')
            make_vlen_datasets(DATA_DIR_PATH, sc_f, sc_split=True)
            sc_f.close()
        if '-catv' in sys.argv:
            cat_f = h5py.File('cat_data.hdf5', 'r+')
            print('\rMaking category only database: %s' % 'vector datasets', end='')
            make_vector_datasets(DATA_DIR_PATH, cat_f, sc_split=False)
            cat_f.close()
        if '-scv' in sys.argv:
            sc_f = h5py.File('sc_data.hdf5', 'r+')
            print('\rMaking sc-split database: %s' % 'vector datasets', end='')
            make_vector_datasets(DATA_DIR_PATH, sc_f, sc_split=True)
            sc_f.close()
