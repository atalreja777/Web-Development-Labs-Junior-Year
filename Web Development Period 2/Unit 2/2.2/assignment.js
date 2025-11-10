const alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j","k", "l", "m", "n", "o", "p", "q", "r", "s", "t","u", "v", "w", "x", "y", "z"];
const ALPHABET_LENGTH = 26;

function caesarCipher(message, shift){
    let fs = "";
    for(let ind = 0; ind < message.length; ind++){
        
        if(isCapitalLetter(message[ind]))
        {
            let initIndex = alphabet.indexOf(message[ind].toLowerCase());
            let finalindex = shiftLogic(initIndex, shift);
            fs += returnCapitalLetter(alphabet[finalindex]);
            continue;
        }
        else if(isLowercaseLetter(message[ind]))
        {
            let initIndex = alphabet.indexOf(message[ind]);
            let finalindex = shiftLogic(initIndex, shift);
            fs += message[finalindex];
        }
        else{
            fs += message[ind];
        }
    }
    return fs;
}

function caesarDecode(message, shift){
    let fs="";
    for(let ind = 0; ind<message.length; ind++){
        
        if(isCapitalLetter( message[ind]))
        {
            let initIndex =  alphabet.indexOf(message[ind].toLowerCase());
            let finalindex =shiftLogic(initIndex, -shift);
            fs +=returnCapitalLetter(alphabet[finalindex]);
            continue;
        }
        else if(isLowercaseLetter(message[ind]))
        {
            let initIndex = alphabet.indexOf(message[ind]);
            let finalindex = shiftLogic(initIndex, -shift);
            fs += alphabet[finalindex];
        }
        else{
            fs += message[ind];
        }
    }

    return fs;
}

function generateCipher(){
    const letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j","k", "l", "m", "n", "o", "p", "q", "r", "s", "t","u", "v", "w", "x", "y", "z"];
    let currentIndex = letters.length;
    let randomIndex;

    while (currentIndex !== 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [letters[currentIndex], letters[randomIndex]] = [letters[randomIndex], letters[currentIndex]];
    }

    const cipherMap = {};
    for(let ind = 0; ind < ALPHABET_LENGTH; ind++){
        cipherMap[alphabet[ind]] = letters[ind];
    }

    return cipherMap;
}


function substitutionCipher(message, cipherMap){
    let fs = "";
    for(let ind = 0; ind < message.length; ind++){
        if(isCapitalLetter(message[ind]))
        {
            let lowerChar = message[ind].toLowerCase();
            let inCipher = cipherMap[lowerChar];
            if(inCipher)
            {
                fs += returnCapitalLetter(inCipher);
            }
            else
            {
                fs += message[ind];
            }
            continue;
        }
        else if(isLowercaseLetter(message[ind]))
        {
            let inCipher = cipherMap[message[ind]];
            if(inCipher)
            {
                fs += inCipher;
            }
            else
            {
                fs += message[ind];
            }
        }
        else
        {
            fs += message[ind];
        }
    }
    return fs;
}




function substitutionDecode(message, cipherMap){
    let fs = "";
    for(let ind = 0; ind < message.length; ind++){
        
        if(isCapitalLetter(message[ind]))
        {
            let lowerChar = message[ind].toLowerCase();
            let oVal = getoValValue(cipherMap, lowerChar);
            if(oVal){
                fs += returnCapitalLetter(oVal);
            }
            else{
                fs += message[ind];
            }
            continue;
        }
        else if(isLowercaseLetter(message[ind]))
        {
            let oVal = getoValValue(cipherMap, message[ind]);
            if(oVal){
                fs += oVal;
            }
            else{
                fs += message[ind];
            }
        }
        else{
            fs += message[ind];
        }
    }
    return fs;
}


const getoValValue = (map, sV) => {
    for (let [k, v] of map.entries()) {
        if (v=== sV) {
            return k;
        }
    }
    return undefined;
}
const isCapitalLetter =(charString) =>
{
  return ( charString.length ===1&&charString>="A"&& charString<="Z");
};

const returnCapitalLetter = (cString) =>{
    return cString.toUpperCase();
}

const isLowercaseLetter = (cString) =>
{
    return (cString.length === 1 && cString <="z" && cString >= "a");
};

const shiftLogic=(givenI, shift)=>{
    return ((givenI + shift)%26 + 26) % 26;
};

const alphabetLetter = (cString) =>{
    if (cString.length !== 1) return false;
    const ch = cString.toLowerCase();
    return alphabet.indexOf(ch) !== -1;
}