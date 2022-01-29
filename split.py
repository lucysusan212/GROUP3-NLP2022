import pickle

parse_file = '../parse/parsedata.pkl'
with open(parse_file, 'rb') as pf:
    str_list = pickle.load(pf)

# split