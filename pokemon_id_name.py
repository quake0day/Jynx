import csv

def get_id2name_table():
    id2name = {}
    with open('./data/pokemon.csv', 'rb') as f:
        reader = csv.reader(f)
        list_ = list(reader)
        for i in xrange(1, 152):
            id2name[int(list_[i][0])] = list_[i][1] 
    return id2name

if __name__ == "__main__":    
    get_id2name_table()