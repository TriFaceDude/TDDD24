function inputFocus(i){
    if(i.value==i.defaultValue){ i.value=""; i.style.color="#000"; }
}

function inputBlur(i){
    if(i.value==""){ i.value=i.defaultValue; i.style.color="#888"; }
}

function catchError(status){

	if(status.success == false){ alert(status.message); }
}

function toUserObject(email, password, firstname, familyname, gender, city, country){
	
	var user = new Object();
	user.email = email;
	user.password = password;
	user.firstname = firstname;
	user.familyname = familyname;
	user.gender = gender;
	user.city = city;
	user.country = country;
	
	return user;
}
