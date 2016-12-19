function resizeText() {
    var div = document.getElementById("page");
    div.style.overflow = "auto";
    var fontSize = 32;
    var changes = 0;
    var blnSuccess = true;
    while (div.offsetHeight <= window.innerHeight) {
        div.style.fontSize = fontSize + "px";
        fontSize++;
        changes++;
        if (changes > 500) {
            //failsafe..
            alert("Error")
            blnSuccess = false;
            break;
        }
    }
    while (div.offsetHeight >= window.innerHeight) {
        div.style.fontSize = fontSize + "px";
        fontSize--;
        changes--;
        if (changes > 500) {
            //failsafe..
            alert("Error")
            blnSuccess = false;
            break;
        }
    }
    if (changes > 0) {
        //upon failure, revert to original font size:
        if (blnSuccess)
            fontSize -= 2;
        else
            fontSize -= changes;
        div.style.fontSize = fontSize + "px";
    }
};
window.onresize = resizeText
window.onload = resizeText