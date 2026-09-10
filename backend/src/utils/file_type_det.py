import filetype

def guess_file_type(path:str):
    try:
        kind = filetype.guess(path)
    except:
        return None
    if kind is None:
        return None
    return kind.extension