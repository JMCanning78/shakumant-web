function clear_choices() {
    var choices = document.getElementsByClassName("chosen");
    for (var i = 0; i < choices.length; i++) {
	if (choices[i].id) {
/*	    alert('Setting ' + choices[i].id + '.display = "none"'); */
	    choices[i].style.display = "none";
	}
    }
}
function display_choice(id) {
    clear_choices();
/*    alert('Setting ' + id + '.display = "block"'); */
    document.getElementById(id).style.display = "block";
}
function send_info_email() {
    var prefixes = ['www.' ];
    var host = window.location.hostname;
    if (host == '') {
	host = "localhost"
    }
    for (var i=0; i < prefixes.length; i++) {
	prefix = prefixes[i]
	if (host.substring(0,prefix.length) == prefix) {
	    host = host.slice(prefix.length)
	}
    }
    var mailloc = 'mailto' + ':' + 'info@' + host +
	'?subject=More%20info%20please';
    window.location.assign(mailloc);
}
function call_info_phone() {
    var seq = '0380';
    var areacode = '(971)-';
    var exchange = '251-';
    var uri = 'tel:' + '+1' + areacode + exchange + seq;
    window.location.assign(uri);
}


