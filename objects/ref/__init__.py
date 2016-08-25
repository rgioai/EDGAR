# v0.1.1 requires no init.
from ref_functions import *
import subprocess

subprocess.run(['chmod 751 setup.sh', './setup.sh'])

ref_functions.init_cik_list()

ref_functions.update_file_structure()
