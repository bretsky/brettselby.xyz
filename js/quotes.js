function replaceQuote() {
	$.get("cgi-bin/quote-gen.py", function(data) {
		document.getElementById("quote").innerHTML = data
		var quote = $("#quotetext");
	    var quoteAuthor = $(".quoteauthor");
	    var quoteCell = $("#quote");
	    quoteCell.height(quote.height() + quoteAuthor.height());
	})
}




function resizeBackground() {
	var bg = $("html");
	bg.height(window.innerHeight);
    var quote = $("#quotetext");
    var quoteAuthor = $(".quoteauthor");
    var quoteCell = $("#quote");
    quoteCell.height(quote.height() + quoteAuthor.height());
}

window.onload = replaceQuote()
$(window).resize(resizeBackground);
var bg = $("html");
bg.height(window.innerHeight);
resizeBackground()
