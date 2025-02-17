from hashlib import sha3_256


# Devuelve la cadena de texto en sha3-256 Doble
def sha256(text):
    string = str(text)
    stringsha256 = sha3_256(string.encode("UTF-8")).hexdigest()
    return sha3_256(stringsha256.encode("UTF-8")).hexdigest()

chunkLevel = 16
processedContent = []

with open("test.wei") as file:
    fileContent = file.read()
    content = fileContent[64:-64]
    print(content)
    for i in range(0, len(content), chunkLevel):
        processedContent.append(content[i:i+chunkLevel])
    print(processedContent)

    sha256Content = ""

    for seg in processedContent:
        sha256Content = sha256Content + sha256(seg)

    checksum = sha256(sha256Content)
    print(checksum)

    print(fileContent[-64:])
    
    for i in range(64):
        seed = sha256(i)
        print(seed)
        if seed == fileContent[:64]:
            print(i)
            break
