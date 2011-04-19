

def parseline(line):
    '''Compiles a single line of baseline into bytecode.

    Takes a string of the form
        INT : stuff

    Returns a triple (word,list,line), where list contains a list of (register,item) 
    pairs.  Register is one of 'AV'.  If register is A or V, item is an
    integer ; if register is '-' item is a string.

    Register is one of 'AV'; each item is an integer.  Comments (in the -
    register) are cleaned out.

    The third element of the returned triple is the input line, for debugging.


    >>> parseline('100 : ²³ ²³₄₅²³66₄₅ ₄ ₅ ₄₅Hilarious')
    (100, [('A',23), ('A',23), ('V',45), ('A',23), ('-','66'), ('V',45), ('V',4), ('V',5), ('V',45), ('-','Hilarious')])
    '''
    wordname, sep, definition = line.partition(':')
    if sep is '':
        raise Exception("wtf, failed parse on this line: " + line)
    
