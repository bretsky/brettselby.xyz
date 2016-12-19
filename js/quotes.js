function replaceQuote() {
	quote = $.get("cgi-bin/quote-gen.py", function(data) {
		document.getElementById("quote").innerHTML = data
	})
}

window.onload = replaceQuote()