

function fileUpload(){
    var file = document.getElementById("upF");

    if (file.files){
        var reader = new FileReader();
        reader.filename = file.files[0].name
        reader.onload = e=>{
            document.getElementById("plainteks").value = e.target.result
            document.getElementById("filename").value = e.target.filename
            document.getElementById("plaintekshidden").value = e.target.result
            console.log(e.target.result)
            console.log(e.target.filename)
        }   
        reader.readAsText(file.files[0])
    }
}

//snippet to download a text
var textFile;
makeTextFile = function (text) {
    var data = new Blob([text], {type: 'text/plain'});

    // If we are replacing a previously generated file we need to
    // manually revoke the object URL to avoid memory leaks.
    if (textFile !== null) {
      window.URL.revokeObjectURL(textFile);
    }

    textFile = window.URL.createObjectURL(data);

    // returns a URL you can use as a href
    return textFile;
  };

function affine(){
    document.getElementById("choice").value="affine"
    document.getElementById("choicet").innerHTML="Current chosen is Affine algorithm"
    document.getElementById("matriks").hidden = true
    document.getElementById("label").innerHTML = ""
}
function vigenere(){
    document.getElementById("choice").value="vigenere"
    document.getElementById("choicet").innerHTML="Current chosen is vigenere algorithm"
    document.getElementById("matriks").hidden = true
    document.getElementById("label").innerHTML = ""
}
function playfair(){
    document.getElementById("choice").value="playfair"
    document.getElementById("choicet").innerHTML="Current chosen is playfair algorithm"
    document.getElementById("matriks").hidden = true
    document.getElementById("label").innerHTML = ""
}
function fvigenere(){
    document.getElementById("choice").value="fvigenere"
    document.getElementById("choicet").innerHTML="Current chosen is full vigenere algorithm"
    document.getElementById("matriks").hidden = false
    document.getElementById("label").innerHTML = "Full Vigenere Matrix for decrypt : "
}
function akvigenere(){
    document.getElementById("choice").value="avigenere"
    document.getElementById("choicet").innerHTML="Current chosen is autokey vigenere algorithm"
    document.getElementById("matriks").hidden = true
    document.getElementById("label").innerHTML = ""
}
function evigenere(){
    document.getElementById("choice").value= "evigenere"
    document.getElementById("choicet").innerHTML="Current chosen is extended vigenere algorithm"
    document.getElementById("matriks").hidden = true
    document.getElementById("label").innerHTML = ""
}

//download string as file snippet
function download(strData, strFileName, strMimeType) {
    var D = document,
        A = arguments,
        a = D.createElement("a"),
        d = A[0],
        n = A[1],
        t = A[2] || "text/plain";

    //build download link:
    a.href = "data:" + strMimeType + "charset=utf-8," + escape(strData);


    if (window.MSBlobBuilder) { // IE10
        var bb = new MSBlobBuilder();
        bb.append(strData);
        return navigator.msSaveBlob(bb, strFileName);
    } /* end if(window.MSBlobBuilder) */



    if ('download' in a) { //FF20, CH19
        a.setAttribute("download", n);
        a.innerHTML = "downloading...";
        D.body.appendChild(a);
        setTimeout(function() {
            var e = D.createEvent("MouseEvents");
            e.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            a.dispatchEvent(e);
            D.body.removeChild(a);
        }, 66);
        return true;
    }
        //do iframe dataURL download: (older W3)
        var f = D.createElement("iframe");
        D.body.appendChild(f);
        f.src = "data:" + (A[2] ? A[2] : "application/octet-stream") + (window.btoa ? ";base64" : "") + "," + (window.btoa ? window.btoa : escape)(strData);
        setTimeout(function() {
            D.body.removeChild(f);
        }, 333);
        return true;
}


function encrypt(){
    var alg = document.getElementById("choice").value
    var key = document.getElementById("key").value

    if (alg == evigenere){
        plainteks = document.getElementById("plaintekshidden").value
    }else{
        var plainteks = document.getElementById("plainteks").value
    }
    
    fetch(
        "http://localhost:6969/encrypt",
        {
            method : 'POST',
            headers: {
                'Content-type' : 'Application/json'
            },
            body : JSON.stringify({
                "algorithm" : alg,
                "plainteks" : plainteks,
                "key" : key
            })
        }
    )
     .then(resp => resp.json())
     .then(resp => {
         console.log(resp)
         if (alg != 'evigenere'){
            document.getElementById("result").innerHTML = "Cipherteks : " + resp['cipherteks'];
        }
         if (alg == 'fvigenere'){
             document.getElementById("collat").innerHTML = "Matriks FVigenere : " + resp['collat']
         }else if (alg == 'evigenere'){
            download(resp['cipherteks'],document.getElementById("filename").value,'text/plain')
            document.getElementById("collat").innerHTML = "File saved as : " + document.getElementById("filename").value
         }
        })
     .catch(err => console.log(err))
}

function decrypt(){
    var alg = document.getElementById("choice").value
    var cipherteks = document.getElementById("plainteks").value
    var key = document.getElementById("key").value
    var matriks = document.getElementById("matriks").value
    
    fetch(
        "http://localhost:6969/decrypt",
        {
            method : 'POST',
            headers: {
                'Content-type' : 'Application/json'
            },
            body : JSON.stringify({
                "algorithm" : alg,
                "cipherteks" : cipherteks,
                "key" : key,
                "matriks" : matriks
            })
        }
    )
     .then(resp => resp.json())
     .then(resp => {
        //  document.getElementById("result").innerHTML = "Plainteks : " + resp['plainteks'];
         if (alg != 'evigenere'){
            document.getElementById("result").innerHTML = "Plainteks : " + resp['plainteks'];
        }
         if (alg == 'evigenere'){
            download(resp['plainteks'],document.getElementById("filename").value,'text/plain')
            document.getElementById("collat").innerHTML = "File saved as : " + document.getElementById("filename").value
         }
        })
     .catch(err => console.log(err))
}