function getReply() {
	input = document.getElementById("sms-text").value
	if ($.trim(input).length == 0) {
		return
	}
	chat = document.getElementById("chat")
	container = document.createElement("div")
	chat.appendChild(container)
	container.className = "message-container"
	newMessage = document.createElement("p")
	container.appendChild(newMessage)
	newMessage.innerHTML = input
	newMessage.className = "my-bubble"	
	chat.scrollTop = chat.scrollHeight
	document.getElementById("sms-text").value = ""
	$.get("http://m.brettselby.xyz/cgi-bin/brett-bot.py", {s: input}, function(data) {
		container = document.createElement("div")
		container.className = "message-container"
		newReply = document.createElement("p")
		newReply.innerHTML = data
		newReply.className = "bubble"
		container.appendChild(newReply)
		chat.appendChild(container)
		chat.scrollTop = chat.scrollHeight
	})
}

$(function(){
	$("#sms-text").keypress(function (e) {
		if (e.keyCode == 13) {
			getReply()
		}
	});
});