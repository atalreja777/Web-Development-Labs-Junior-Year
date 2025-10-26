const alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j","k", "l", "m", "n", "o", "p", "q", "r", "s", "t","u", "v", "w", "x", "y", "z"];
const ALPHABET_LENGTH = 26;

function caesarCipher(message, shift){
    let finalString = "";
    for(let ind = 0; ind < message.length; ind++){
        
        if(isCapitalLetter(message[ind]))
        {
            let initIndex = alphabet.indexOf(message[ind].toLowerCase());
            let finalindex = shiftLogic(initIndex, shift);
            finalString += returnCapitalLetter(alphabet[finalindex]);
            continue;
        }
        else if(isLowercaseLetter(message[ind]))
        {
            let initIndex = alphabet.indexOf(message[ind]);
            let finalindex = shiftLogic(initIndex, shift);
            finalString += message[finalindex];
        }
        else{
            finalString += message[ind];
        }
    }
    return finalString;
}

function caesarDecode(message, shift){
    let finalString = "";
    for(let ind = 0; ind < message.length; ind++){
        
        if(isCapitalLetter(message[ind]))
        {
            let initIndex = alphabet.indexOf(message[ind].toLowerCase());
            let finalindex = shiftLogic(initIndex, -shift);
            finalString += returnCapitalLetter(alphabet[finalindex]);
            continue;
        }
        else if(isLowercaseLetter(message[ind]))
        {
            let initIndex = alphabet.indexOf(message[ind]);
            let finalindex = shiftLogic(initIndex, -shift);
            finalString += alphabet[finalindex];
        }
        else{
            finalString += message[ind];
        }
    }

    return finalString;
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
    let finalString = "";
    for(let ind = 0; ind < message.length; ind++){
        if(isCapitalLetter(message[ind]))
        {
            let lowerChar = message[ind].toLowerCase();
            let inCipher = cipherMap[lowerChar];
            if(inCipher)
            {
                finalString += returnCapitalLetter(ciphered);
            }
            else
            {
                finalString += message[ind];
            }
            continue;
        }
        else if(isLowercaseLetter(message[ind]))
        {
            let inCipher = cipherMap[message[ind]];
            if(inCipher)
            {
                finalString += inCipher;
            }
            else
            {
                finalString += message[ind];
            }
        }
        else
        {
            finalString += message[ind];
        }
    }
    return finalString;
}




function substitutionDecode(message, cipherMap){
    let finalString = "";
    for(let ind = 0; ind < message.length; ind++){
        
        if(isCapitalLetter(message[ind]))
        {
            let lowerChar = message[ind].toLowerCase();
            let original = getOriginalValue(cipherMap, lowerChar);
            if(original){
                finalString += returnCapitalLetter(original);
            }
            else{
                finalString += message[ind];
            }
            continue;
        }
        else if(isLowercaseLetter(message[ind]))
        {
            let original = getOriginalValue(cipherMap, message[ind]);
            if(original){
                finalString += original;
            }
            else{
                finalString += message[ind];
            }
        }
        else{
            finalString += message[ind];
        }
    }
    return finalString;
}


const getOriginalValue = (map, searchValue) => {
    for (let [key, value] of map.entries()) {
        if (value === searchValue) {
            return key;
        }
    }
    return undefined;
}
const isCapitalLetter =(characterString) =>
{
  return ( characterString.length ===1&&characterString>="A"&& characterString<="Z");
};

const returnCapitalLetter = (characterString) =>{
    return characterString.toUpperCase();
}

const isLowercaseLetter = (characterString) =>
{
    return (characterString.length === 1 && characterString <=z && characterString >= a);
};

const shiftLogic=(initialIndex, shift)=>{
    return ((initialIndex + shift)%26 + 26) % 26;
};

const alphabetLetter = (characterString) =>{
    if (characterString.length !== 1) return false;
    const ch = characterString.toLowerCase();
    return alphabet.indexOf(ch) !== -1;
}