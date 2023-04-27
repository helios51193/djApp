import string
def checkValidHeader(headers):

    invalidHeaders = []
    punc = string.punctuation
    
    for h in headers:
        if any(c in punc for c in h):
            invalidHeaders.append(h)


    valid = len(invalidHeaders) == 0
    
    return valid, invalidHeaders 



def checkValidOptions(options):

    valid, invalidOptions = checkValidHeader(options)
    return valid, invalidOptions