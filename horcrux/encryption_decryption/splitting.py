import sys, os
import math

def split(fromfile, todir, split_name):
    """Splits a given encrypted file into 3 horcruxes.
    Args-
        fromfile::str: Path of the file to be splitted
        todir::str: Path of the directory where the splits are to be created
        split_name::str: Part of the name of the split that is to be created
    Returns-
        partnum
    """ 
    filesize = os.path.getsize(fromfile)
    chunksize = math.ceil(float(filesize)/3)
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fname in os.listdir(todir):            # delete any existing files
            os.remove(os.path.join(todir, fname)) 
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while True:                                    # eof = empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: 
            break
        partnum  = partnum + 1
        filename = os.path.join(todir, f"{split_name}0{partnum}")
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum
            