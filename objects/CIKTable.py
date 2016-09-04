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
        Tries to load a serialized CikTable; creates an empty one if it cannot load.
        :return: None
        """
        self.data = None
        try:
            self.load()
            assert(isinstance(self.data, pd.DataFrame))
        except FileNotFoundError:
            # TODO Init properly
            self.data = pd.DataFrame(columns=['CIK', 'Symbol', 'Name', 'Industry', 'Directory_Path'])
        raise NotImplementedError

    def add_row(self, cik, symbol, name):
        # FUTURE require only symbol, lookup cik and name.
        # TODO Add the row to self.data
        raise NotImplementedError

    def remove_row(self, cik=None, symbol=None, name=None):
        # TODO Remove row
        raise NotImplementedError

    def add_column(self, col_name):
        # Future add column name
        raise NotImplementedError
    
    def remove_column(self, col_name):
        # Future remove column name
        raise NotImplementedError

    def change_value(self, new_value, col, cik=None, symbol=None, name=None):
        # TODO Change value
        raise NotImplementedError

    def update(self):
        # TODO load CIK_List.pkl and add_row for every CIK if not in table already
        raise NotImplementedError

    def save(self):
        """
        Dumps DataFrame to EDGAR/objects/ref/CIK_Table.pkl
        :return: None
        """
        with open('EDGAR/objects/ref/CIK_Table.pkl', 'wb') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            f.close()

    def load(self):
        """
        Loads DataFrame from EDGAR/objects/ref/CIK_Table.pkl
        :return:
        """
        with open('EDGAR/objects/ref/CIK_Table.pkl', 'rb') as f:
            self.data = pickle.load(f)
            assert(isinstance(self.data, pd.DataFrame))
            f.close()


