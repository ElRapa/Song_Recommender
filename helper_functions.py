import pickle

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def chunks_list(lst, n):
    """List of successive n-sized chunks from lst."""
    return list(chunks(lst,n))

def write_list_txt(list, path):
    '''save list to .txt'''
    with open(path, "wb") as fp:   #Pickling
        pickle.dump(list, fp)

def read_list_txt(path):
    '''open list saved to .txt'''
    with open(path, "rb") as fp:   # Unpickling
        a = pickle.load(fp)
    return a