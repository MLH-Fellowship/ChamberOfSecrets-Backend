import os, sys
readsize = 1024

def join(fromdir, tofile):
    """Rejoins encrypted horcruxes into a single encrypted file.
    Args-
        fromdir::str: Path to the directory where the files are getting stored.
        tofile::str: Path of the file that the encrypted horcruxes will be combined into.
    Returns-
        None
    """
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    parts.sort(  )
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while True:
            filebytes = fileobj.read(readsize)
            if not filebytes: 
                break
            output.write(filebytes)
        fileobj.close(  )
    output.close(  )

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: join.py [from-dir-name to-file-name]')
    else:
        if len(sys.argv) != 3:
            interactive = 1
            fromdir = input('Directory containing part files? ')
            tofile  = input('Name of file to be recreated? ')
        else:
            interactive = 0
            fromdir, tofile = sys.argv[1:]
        absfrom, absto = map(os.path.abspath, [fromdir, tofile])
        print('Joining', absfrom, 'to make', absto)

        try:
            join(fromdir, tofile)
        except:
            print('Error joining files:')
            print(sys.exc_type, sys.exc_value)
        else:
           print('Join complete: see', absto)
        if interactive: input('Press Enter key') # pause if clicked