import string
import copy
import random



alphabetU = list(string.ascii_uppercase)

allAscii = [chr(i) for i in range(256)]

def make_fv_matrix(matstring=None):
    if matstring:
        return [[matstring[j*26+i] for i in range(26)] for j in range(26)]
    else:
        mat = []
        row_alphabet_string = ""
        for i in range(26):
            while not row_alphabet_string or row_alphabet_string in mat:
                temp_alphabet = copy.copy(alphabetU)
                random.shuffle(temp_alphabet)
                row_alphabet_string = "".join(temp_alphabet)
                # random.shuffle(row_alphabet)
            mat.append(row_alphabet_string)
        return mat

full_vignere_matrix = make_fv_matrix()

def vignere_encrypt(plainteks, key):
    plainteks = plainteks.upper()
    lc = list(plainteks)
    key = list(key)
    for i in range(len(lc)):
        lc[i] = chr((ord(lc[i]) + ord(key[i % len(key)])) % 26 + ord('A'))
    return {"cipherteks" : "".join(lc)}

def vignere_decrypt(cipherteks, key):
    cipherteks = cipherteks.upper()
    lp = list(cipherteks)
    key = list(key)
    for i in range(len(lp)):
        lp[i] = chr((ord(lp[i]) - ord(key[i % len(key)])) % 26 + ord('A'))
    return {"plainteks" : "".join(lp)}

def ak_vignere_encrypt(plainteks, key):
    plainteks = plainteks.upper()
    lc = list(plainteks)
    key = list(key)
    key.extend(lc)
    key = key[:len(lc)]
    for i in range(len(lc)):
        lc[i] = chr((ord(lc[i]) + ord(key[i])) % 26 + ord('A'))
    return {"cipherteks" : "".join(lc)}

def ak_vignere_decrypt(cipherteks, key):
    cipherteks = cipherteks.upper()
    lp = list(cipherteks)
    key = list(key)
    key.extend(lp)
    key = key[:len(lp)]
    for i in range(len(lp)):
        lp[i] = chr((ord(lp[i]) - ord(key[i])) % 26 + ord('A'))
    return {"plainteks" :"".join(lp)}

def makestring(mat):
    return "".join(mat[i][j] for i in range(len(mat)) for j in range(len(mat)))

def full_vignere_encrypt(plainteks, key):
    plainteks = plainteks.upper()
    lp = list(plainteks)
    lc = []
    for i in range(len(lp)):
        ch = full_vignere_matrix[ord(key[i % len(key)]) - ord('A')][ord(lp[i]) - ord('A')]
        lc.append(ch)
    return {"cipherteks" : "".join(lc), "collat" : makestring(full_vignere_matrix)}

def full_vigenere_decrypt(cipherteks, key, matstring):
    full_mat = make_fv_matrix(matstring)
    cipherteks = cipherteks.upper()
    lp = list(cipherteks)
    lc = []
    for i in range(len(lp)):
        ch = chr(full_mat[ord(key[i%len(key)])-ord('A')].index(lp[i]) + ord('A'))
        lc.append(ch)
    return {"plainteks" : "".join(lc)}

def make_pf_matrix(key):
    set_alph = list(copy.copy(alphabetU))[::-1]
    set_alph.remove('J')
    key = list(key)[::-1]
    matrix = [["" for i in range(5)] for j in range(5)]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if not key:
                matrix[i][j] = set_alph.pop()
            else:
                ch = key.pop()
                matrix[i][j] = ch
                set_alph.remove(ch)
    print(matrix)
    return matrix

def pf_lookup_encrypt(pair, pfmat):
    if pair == (" ",""):
        return (" ","")
    a,b = pair
    ax,ay,bx,by =0,0,0,0
    for i in range(len(pfmat)):
        for j in range(len(pfmat)):
            if pfmat[i][j] == a:
                ax,ay = i,j
            if pfmat[i][j] == b:
                bx,by = i,j
    if ax == bx:
        ca = pfmat[ax][(ay+1) % 5]
        cb = pfmat[bx][(by+1) % 5]
    elif ay == by:
        ca = pfmat[(ax+1) % 5][ay]
        cb = pfmat[(bx+1) % 5][by]
    else:
        ca = pfmat[ax][by]
        cb = pfmat[bx][ay]
    return (ca, cb)

def pf_lookup_decrypt(pair, pfmat):
    if pair == (" ","") or pair == ("", " "):
        return pair
    a,b = pair
    ax,ay,bx,by = 0,0,0,0
    for i in range(len(pfmat)):
        for j in range(len(pfmat)):
            if pfmat[i][j] == a:
                ax,ay = i,j
            if pfmat[i][j] == b:
                bx,by = i,j
    if ax == bx:
        ca = pfmat[ax][(ay-1) % 5]
        cb = pfmat[bx][(by-1) % 5]
    elif ay == by:
        ca = pfmat[(ax-1) % 5][ay]
        cb = pfmat[(bx-1) % 5][by]
    else:
        ca = pfmat[ax][by]
        cb = pfmat[bx][ay]
    return (ca, cb)

def playfair_encrypt(plainteks, key):
    plainteks = plainteks.upper()
    pfmat = make_pf_matrix(key)
    lp = list(plainteks)[::-1]
    pairs = []
    while lp:
        temp = lp.pop()
        if temp == " ":
            pairs.append((" ",""))
        elif not lp or lp[-1] == temp:
            pairs.append((temp,'x'))
        else:
            pairs.append((temp,lp.pop()))
    pairs = pairs[::-1]
    encrypted_pairs = [pf_lookup_encrypt(pair,pfmat) for pair in pairs]
    return {"cipherteks" : "".join(["".join(pair) for pair in encrypted_pairs[::-1]])}
    
def playfair_decrypt(cipherteks, key):
    pfmat = make_pf_matrix(key)
    lp = list(cipherteks)[::-1]
    pairs = []
    while lp:
        temp = lp.pop()
        pairs.append((temp,lp.pop()))
    pairs = pairs[::-1]
    encrypted_pairs = [pf_lookup_decrypt(pair,pfmat) for pair in pairs]
    return {"plainteks" : "".join(["".join(pair) for pair in encrypted_pairs[::-1]])}

# Extended Euclidean Algorithm for finding modular inverse
# eg: modinv(7, 26) = 15
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y
 
def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

def affine_encrypt(plainteks, key):
    plainteks = plainteks.upper().strip()
    lp = list(plainteks)
    a = int(key.split(',')[0])
    b = int(key.split(',')[1])
    lc = []
    for ch in lp:
        lc.append(chr(((a*(ord(ch) - ord('A')) + b) % 26) + ord('A')))
    return {"cipherteks" : "".join(lc)}

def affine_decrypt(cipherteks, key):
    cipherteks = cipherteks.upper().strip()
    lc = list(cipherteks)
    a = int(key.split(',')[0])
    b = int(key.split(',')[1])
    lp = []
    for ch in lc:   
        lp.append(chr(((modinv(a,26) * (ord(ch) - ord('A') - b)) % 26) + ord('A')))
    return {"plainteks" : "".join(lp)}

def process_file(file,bytes=False):
    if bytes:
        with open(file,'rb') as f:
            teks = f.read()
        return teks
    with open(file) as f:
        teks = f.read()
    return teks

def make_extended_matrix():
    mat = []
    row_alphabet_string = ""
    for i in range(256):
        temp_alphabet = copy.copy(allAscii)
        temp_alphabet.extend(temp_alphabet[:i])
        del temp_alphabet[:i]
        row_alphabet_string = "".join(temp_alphabet)
        mat.append(row_alphabet_string)
    return mat

def extended_vigenere_encrypt(plainteks, key):
    mat = make_extended_matrix()
    plainteks = plainteks.upper()
    lp = list(plainteks)
    lc = []
    for i in range(len(lp)):
        ch = mat[ord(key[i])][ord(lp[i])]
        lc.append(ch)
    return {"cipherteks" : "".join(lc)}

def e_vignere_encrypt(plainteks, key):
    plainteks = plainteks.upper()
    lc = list(plainteks)
    key = list(key)
    for i in range(len(lc)):
        if (ord(lc[i]) > 256): print(ord(lc[i]))
        lc[i] = chr((ord(lc[i]) + ord(key[i % len(key)])) % 256)
    return {"cipherteks" : "".join(lc)}

def e_vignere_decrypt(cipherteks, key):
    cipherteks = cipherteks.upper()
    lp = list(cipherteks)
    key = list(key)
    for i in range(len(lp)):
        lp[i] = chr((ord(lp[i]) - ord(key[i % len(key)])) % 256)
    return {"plainteks" : "".join(lp)}
