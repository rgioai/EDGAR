import pandas as pd
import pickle


class CikTable(object):
    """
    Stores and manipulates a Pandas DataFrame of basic company reference information for
    companies currently in the CIK_List.pkl for data collection.

    Not implemented as of version 0.1.
    """
    def __init__(self):
        """
        Tries to load a serialized CikTable; else, creates from csv.
        :return: None
        """
        self.data = None
        try:
            self.load_pkl()
            assert(isinstance(self.data, pd.DataFrame))
        except FileNotFoundError:
            self.load_csv()
            assert(isinstance(self.data, pd.DataFrame))

    def find(self, symbol, cik=None):
        if symbol is None:
            raise NotImplementedError


    def add_row(self, symbol, cik='NaN', name='NaN', sector='NaN', industry='NaN', date_added='NaN', date_removed='NaN', reason='NaN'):
        if cik == 'NaN':
            # Future Dynamic cik lookup
            pass
        df = pd.DataFrame([symbol, cik, name, sector, industry, date_added, date_removed, reason], columns=
        ['Ticker symbol', 'CIK,Security', 'GICS Sector', 'GICS Sub Industry', 'Date added','Date Removed,Reason'])
        self.data.append(df, ignore_index=True)

    def remove_row(self, key):
        try:
            key = int(key)
        except ValueError:
            key = self.get_cik(key)
        # TODO select row containing key as cik
        # TODO remove that row
        raise NotImplementedError

    def change_value(self, new_value, col, cik=None, symbol=None, name=None):
        # TODO Change value
        raise NotImplementedError

    def get_cik(self, symbol):
        # TODO Find the row containing that symbol
        # TODO Retun its cik
        raise NotImplementedError

    def update(self):
        # TODO load CIK_List.pkl and add_row for every CIK if not in table already
        raise NotImplementedError

    def save(self):
        """
        Dumps DataFrame to EDGAR/objects/ref/CIK_Table.pkl
        :return: None
        """
        with open('objects/ref/CIK_Table.pkl', 'wb') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            f.close()

    def load_pkl(self):
        """
        Loads DataFrame from EDGAR/objects/ref/CIK_Table.pkl
        :return:
        """
        with open('objects/ref/CIK_Table.pkl', 'rb') as f:
            self.data = pickle.load(f)
            assert(isinstance(self.data, pd.DataFrame))
            f.close()

    def load_csv(self):
        """
        Loads DataFrame from EDGAR/objects/ref/CIK_Table.csv
        :return:
        """
        raise NotImplementedError
