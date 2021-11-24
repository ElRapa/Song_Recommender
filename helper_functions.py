def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def chunks_list(lst, n):
    """List of successive n-sized chunks from lst."""
    return list(chunks(lst,n))