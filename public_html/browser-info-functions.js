/* Set all the navigator property elements */

function populate_object_elements(obj) {
    for (prop in obj) {
	var oname = obj.toString().replace(/\[object ([^\]]*)\]/i, '$1')
	var name = oname + "." + prop;
	var elem = document.getElementById(name);
	if (elem) {
	    old = elem.innerHTML.replace(/ \(was.*\)/, '').replace(/\s*/, '')
	    if (typeof obj[prop] == 'function') {
		elem.innerHTML = "(function) " + obj[prop]()
	    } else {
		elem.innerHTML = obj[prop]
	    }
	    if (old.length > 0 && old != elem.innerHTML) {
		elem.innerHTML += ' (was ' + old + ')'
	    }
	}
    }
}
