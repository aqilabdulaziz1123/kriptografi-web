from cypher import *
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/encrypt", methods=["POST"])
def encrypt():
    req = request.json
    alg = req['algorithm']
    plainteks = req['plainteks']
    key = req['key']
    func = {
        'vigenere' : vignere_encrypt,
        'avigenere' : ak_vignere_encrypt,
        'playfair' : playfair_encrypt,
        'affine' : affine_encrypt,
        'fvigenere' : full_vignere_encrypt,
        'evigenere' : e_vignere_encrypt
    }

    return jsonify(func[alg](plainteks, key))

@app.route("/decrypt", methods=["POST"])
def decrypt():
    req = request.json
    alg = req['algorithm']
    plainteks = req['cipherteks']
    key = req['key']
    func = {
        'vigenere' : vignere_decrypt,
        'avigenere' : ak_vignere_decrypt,
        'playfair' : playfair_decrypt,
        'affine' : affine_decrypt,
        'fvigenere': full_vigenere_decrypt,
        'evigenere' : e_vignere_decrypt
    }

    if alg == 'fvigenere':
        ret = jsonify(func[alg](plainteks,key,req['matriks']))
    else:
        ret = jsonify(func[alg](plainteks, key)) 

    return ret

if __name__=='__main__':
    app.run(port=6969)