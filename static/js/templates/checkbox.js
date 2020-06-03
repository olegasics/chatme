window.onload = function() {
    var c = document.querySelector('#shest0');

    c.onclick = function() {
        if (c.checked) {
            window.location.replace('/order/?ended=1')
            // xhttp.open("GET", '/orders/?ended=1', true );
            // xhttp.send();
        } else {
            window.location.replace('/order/?ended=0')
            // xhttp.open("GET", '/orders/?ended=0', true);
            // xhttp.send();
        }
    }
}
