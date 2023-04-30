import hashlib 

with open("./xueanquanhelperforteacher.exe","rb") as hashjiaoyan:
    bytes = hashjiaoyan.read() # read file as bytes
    readable_hash = hashlib.sha256(bytes).hexdigest()   ;
    print(readable_hash)
