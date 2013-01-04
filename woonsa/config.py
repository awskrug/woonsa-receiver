import os.path

from yaml import load

def load_config_from_file(filename):
    dirname = os.path.dirname(filename)
    with open(filename) as f:
        lc = load(f)
    cf_dict = dict(lc)

    return cf_dict
