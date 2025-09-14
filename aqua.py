#                                                                    ---------------------------------
#
#                                                                       Script  creado por  Hoshiku
#                                                                       https://github.com/Hoshikuu
#
#                                                                    ---------------------------------

# CIPWEI V3 - AQUA

from hashlib import sha512, sha256
from random import choice
from string import ascii_letters

def create_byte_key(key):
    """Create a byte key from a given string key.

    Args:
        key (str): The key.

    Returns:
        bytes: The byte key.
    """
    hash128 = sha512(key.encode("utf-8")).hexdigest()
    hash641 = sha256(key.encode("utf-8")).hexdigest()
    hash642 = sha256(hash641.encode("utf-8")).hexdigest()
    hash = hash641 + hash128 + hash642
    return bytes.fromhex(hash)

def create_pattern(byte_key, size=128):
    """Create a pattern from a byte key.

    Args:
        byte_key (bytes): The byte key.

    Returns:
        str: The pattern string.
    """
    ascii_table = [chr(i) for i in range(size)]
    used = [False]*size
    result_chars = []
    for byte in byte_key:
        id = byte % size
        while used[id]:
            id = (id + 1) % size
        used[id] = True
        result_chars.append(ascii_table[id])
    return "".join(result_chars)

def create_reverse_pattern(pattern):
    reversed_pattern = [""] * len(pattern)
    
    for char, i in zip(pattern, range(len(pattern))):
        reversed_pattern[ord(char)] = chr(i)
        
    return "".join(reversed_pattern)
        
def create_chunks(data, randomness):
    """Create chunks of data.

    Args:
        data (str): The data string.

    Yields:
        str: The next chunk of data.
    """
    #FIXME: Update DOCSTRING
    # randomness = 50 # 0 - 100 percent of randomness (set to 0 for no randomness)
    # More randomness means higher file size but better security
    size = int(128 * (100 - randomness) / 100)

    for i in range(0, len(data), size):
        chunk = data[i:i+size]
        fill = ''.join(choice(ascii_letters) for _ in range(128 - size))
        if len(chunk) < size:
            i = -1
        chunk += fill
        yield chunk, i // size
        
def remove_chunks(data, randomness):
    """Remove random characters from data chunks.

    Args:
        data (str): The data string with random characters.

    Yields:
        str: The next cleaned chunk of data.
    """
    # randomness = 50 # 0 - 100 percent of randomness (set to 0 for no randomness)
    size = int(128 * (100 - randomness) / 100)

    for i in range(0, len(data), 128):
        chunk = data[i:i+128]
        real_chunk = chunk[:-(128-size)]   # nos quedamos solo con la parte real
        yield real_chunk

def create_shuffled_data(data, pattern, randomness):
    #TODO: Write DOCSTRING
    _chunk = ""
    for chunk, i in create_chunks(data, randomness):
        print(f"Chunk {i}: {chunk} (len={len(chunk)})")
        shuffled_data = []
        # print(_pattern) # ESTO ROMPE LA PUTA TERMINAL QUE COJONES
        if i == 0 or (i % 3) == 0:
            for char in pattern:
                shuffled_data.append(chunk[ord(char)])
        elif i == -1: # Last chunk, Applies special pattern to fit the chunk size
            for char in create_pattern(create_byte_key(_chunk)[:len(chunk)], len(chunk)):
                shuffled_data.append(chunk[ord(char)])
        else:
            for char in create_pattern(create_byte_key(_chunk)):
                shuffled_data.append(chunk[ord(char)])
        _chunk = chunk
        yield "".join(shuffled_data)
        
def create_unshuffled_data(data, pattern):
    #TODO: Write DOCSTRING
    _chunk = ""
    for chunk, i in create_chunks(data, 0):
        unshuffled_data = [""] * len(chunk)
        if i == 0 or (i % 3) == 0:
            for char in create_reverse_pattern(pattern):
                unshuffled_data.append(chunk[ord(char)])
        elif i == -1: # Last chunk, Applies special pattern to fit the chunk size
            rev_pattern = create_reverse_pattern(create_pattern(create_byte_key(_chunk)[:len(chunk)], len(chunk)))
            for char in rev_pattern:
                unshuffled_data.append(chunk[ord(char)])
        else:
            rev_pattern = create_reverse_pattern(create_pattern(create_byte_key(_chunk)))
            for char in rev_pattern:
                unshuffled_data.append(chunk[ord(char)])
        _chunk = "".join(unshuffled_data)
        yield _chunk

#TODO: Implement decryption (unshuffling)

#TODO: Add another layer of encryption (CIPWEI CORE) + decryption

# password = input("Password:")
password = "password"
randomness = 50  # 0 - 100 percent of randomness (set to 0 for no randomness)

pattern = create_pattern(create_byte_key(password))

data = "This is a test message for encryption and decryption. Let's see how it works! 1234567890!@#$%^&*()_+-=[]{}|;:',.<>/?`~ \"\\ End of message. " * 5  # Make it longer

s_data = "".join(list(create_shuffled_data(data, pattern, randomness)))
print("DATA:", s_data)
with open("aqua.shuffled.data", "w+", encoding="UTF-8") as file:
    file.write(s_data)

us_data = "".join(list(remove_chunks("".join(list(create_unshuffled_data(s_data, pattern))), randomness)))
print("DATA:", us_data)

# from cipweiV2 import encriptA, decriptB

# A = encriptA(s_data, 16, password)
# with open("a", "w+", encoding="UTF-8") as file:
#     file.write(A)
    
# B = decriptB(A, 16, password)
# with open("b", "w+", encoding="UTF-8") as file:
#     file.write(B)



# # CIPWEI CORE
# from random import randint as ri; from hashlib import sha3_256 as sh; h = lambda t: sh(sh(str(t).encode()).hexdigest().encode()).hexdigest()
# def cifrarArchivo(mk, cl, msg):
#     s = ri(0, 64 - cl); ct, ss, ek = "", "", h(mk)[s:s + cl]
#     for i in range(0, len(msg), cl):c = msg[i:i + cl]; sg = "".join(chr(abs(ord(a) + ord(b))) for a, b in zip(c, ek)); ct += sg; ek = h(c+sg)[s:s + cl]; ss += h(sg)
#     return h(s) + ct + h(ss)

# print(cifrarArchivo(password, 64, s_data))