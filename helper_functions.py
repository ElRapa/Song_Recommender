import pickle
import re

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

def txt_to_list(path):
    '''open .txt and loads it into unique list of seprated words'''
    with open(path,'r',encoding='utf-8') as f:
        word_list = []
        for line in f:
            for word in line.split():
                word = re.sub('[^A-Za-z0-9]+', '', word)
                if len(word) > 0:
                    word_list.append(word)
#        word_list=[word for line in f for word in line.split()]
    return list(set(word_list))