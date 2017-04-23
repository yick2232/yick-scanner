// H5 plus事件处理
var ret=null;
function plusReady(){
	var self = plus.webview.currentWebview();
	var url = self.getURL();
	console.log( "页面跳转URL: " + self.getURL() );
	var params = getParamsFromURL(url);
	for (var p in params) {
		console.log(p + ': ' + params[p]);
	}
	name_box = document.getElementById('name');
	phoneNumber_box = document.getElementById('phoneNumber');
	email_box = document.getElementById('email');
	name_box.value = params['name'];
	phoneNumber_box.value = params['phoneNumber'];
	email_box.value = params['email'];
}
if(window.plus){
	plusReady();
}else{
	document.addEventListener("plusready",plusReady,false);
}

function getParamsFromURL(url) {
	var ss = url.slice(url.indexOf('?') + 1).split('&');
	var ret = {}
	for (var idx = 0; idx < ss.length; ++idx) {
		if (!ss[idx]) {
			continue;
		}
		var s = ss[idx].split('=');
		ret[s[0]] = decodeURI(s[1]);
	}
	return ret;
}

function saveResult() {
	name_box = document.getElementById('name');
	phoneNumber_box = document.getElementById('phoneNumber');
	email_box = document.getElementById('email');
	name = name_box.value;
	phoneNumber = phoneNumber_box.value;
	email = email_box.value;
	plus.contacts.getAddressBook( plus.contacts.ADDRESSBOOK_PHONE, function( addressbook ) {
		var contact = addressbook.create();
		contact.name = {givenName: name};
		contact.phoneNumbers = [{type:'手机', value: phoneNumber, preferred: true}];
		contact.emails = [{type:'email', value: email, preferred: true}];
		console.log(contact.id);
		contact.save(function(){
			plus.nativeUI.alert('联系人保存成功！', function(){console.log( "识别信息成功保存到用户手机" );}, 'Alert', 'ok');
		}, function(e) {
			plus.nativeUI.alert('联系人保存失败！\n' + e.message, function(){console.log( "识别信息不能成功保存到手机通讯录" );}, 'Alert', 'ok')
		});
		console.log(contact.id);
	}, function ( e ) {
		plus.nativeUI.alert( 'Get address book failed: ' + e.message );
	});
}