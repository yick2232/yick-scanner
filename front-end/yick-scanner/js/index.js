var server="http://www.yickliao.cn:8888";
var files=[];
// 上传文件
function upload(){
	if(files.length<=0){
		plus.nativeUI.alert("没有添加上传文件！");
		return;
	}
	//outSet("开始上传：")
	var wt=plus.nativeUI.showWaiting();
	var task=plus.uploader.createUpload(server,
		{method:"POST"},
		function(t,status){ //上传完成
			if(status==200){
				result = t.responseText
			}else{
				result = "上传失败"
			}
			wt.close();
			//将结果传入另外一个窗口并进行展示
			console.log(result)
			showResult(result);
		}
	);
	//task.addData("client","HelloH5+");
	task.addData("uid",getUid());
	for(var i=0;i<files.length;i++){
		var f=files[i];
		task.addFile(f.path,{key:f.name});
	}
	task.start();
}
//弹窗展示结果
function showResult(result) {
	result = JSON.parse(result);
	for (var item in result) {
		console.log(item);
		console.log(result[item]);
	}
	console.log(result['Name']);
	console.log(result['PhoneNumber'])
	var w = plus.webview.create(
		url = 'show.html?name=' + result['Name'] + '&phoneNumber=' + result['PhoneNumber'] + '&email=' + result['Email'],
		id = 'show.id'
	);
	w.addEventListener("loaded",function(){
		console.log('loaded');
		w.show();
	},false);
}
// 拍照添加文件
function appendByCamera(){
	plus.camera.getCamera().captureImage(function(p){
		appendFile(p);
	});	
}
// 从相册添加文件
function appendByGallery(){
	plus.gallery.pick(function(p){
        appendFile(p);
    });
}
// 添加文件
var index=1;
function appendFile(p){//文件绝对路径
	var fe=document.getElementById("files");
	var li=document.createElement("li");
	var n=p.substr(p.lastIndexOf('/') + 1);//文件名
	li.innerText=n;
	fe.appendChild(li);
	files.push({name:"uploadkey" + index,path:p});
	index++;
	empty.style.display="none";//隐藏'无上传文件'一行字
}
// 产生一个随机数
function getUid(){
	return Math.floor(Math.random()*100000000+10000000).toString();
}