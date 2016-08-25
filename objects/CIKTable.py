import pandas as pd
import pickle


class CikTable(object):
    def __init__(self):
        self.data = None
        try:
            self.load()
            assert(isinstance(self.data, pd.DataFrame))
        except FileNotFoundError:
            # TODO Init properly
            self.data = pd.DataFrame(columns=['CIK', 'Symbol', 'Name', 'Industry', 'Directory_Path'])

    def add_row(self, cik, symbol, name):
        # FUTURE require only symbol, lookup cik and name.
        # TODO Add the row to self.data
        pass

    def remove_row(self, cik=None, symbol=None, name=None):
        # TODO Remove row
        pass

    def add_column(self, col_name):
        # TODO add column name
        pass

    def change_value(self, new_value, col, cik=None, symbol=None, name=None):
        # TODO Change value
        pass

    def save(self):
        with open('EDGAR/objects/ref/CIK_Table.pkl', 'wb') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            f.close()

    def load(self):
        with open('EDGAR/objects/ref/CIK_Table.pkl', 'rb') as f:
            self.data = pickle.load(f)
            assert(isinstance(self.data, pd.DataFrame))
            f.close()


