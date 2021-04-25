var user = "0"

var password = "0"

var check = '0'


async function call(){

var request = require('request');
var options = { 
		 "async": true,
                 "crossDomain": true,
                 'method': 'GET',
                 'url': 'http://114.71.221.47:7579/Mobius/control/security/la',
                 'headers': {
                 'Accept': 'application/json',
                 'X-M2M-RI': '12345',
                 'X-M2M-Origin': 'C'
                                 }
                                }; 

await request(options, function (error, response) {
//if (error) throw new Error(error);
   console.log(response.body);
   data=JSON.parse(response.body);
   check = data["m2m:cin"];
   check = check["con"];
   check = check.split(',');	
   user = check[1];
   password = check[2];
   send();
	

});



}

async function camcall(photo_pathreal){

var request = require('request');
var options = {
  'method': 'POST',
  'url': 'http://114.71.221.47:7579/Mobius/control/cam',
  'headers': {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'C',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
  },
  body: "{\n    \"m2m:cin\": {\n        \"con\": \"" + "114.71.221.39:9091" + photo_pathreal + "\"\n    }\n}"

};

await request(options, function (error, response) {
  if (error) throw new Error(error);
  console.log(response.body);

});


var request = require('request');
var options = {
  'method': 'POST',
  'url': 'http://114.71.221.47:7579/Mobius/' + user + '/cam',
  'headers': {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': password,
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
  },
  body: "{\n    \"m2m:cin\": {\n        \"con\": \"" + "114.71.221.39:9091" + photo_pathreal + "\"\n    }\n}"

};



await request(options, function (error, response) {
  if (error) throw new Error(error);
  console.log(response.body);
	
  clearInterval(playAlert);

});

 clearInterval(playAlert);


}



var http = require('http');

var express = require('express');

var smartmirror = express();

smartmirror.use(express.static(__dirname));

http.createServer(smartmirror).listen(9091,function() {

	console.log('server on 9091...');

});


async function send(){ 

if( check[0] == '1'){

var exec_photo = require('child_process').exec;

//var video_path = __dirname+"/public/video/"+Date.now()+'.h264';

var photo_pathreal = "/Public/" + Date.now() + ".jpg";

var photo_path = __dirname + photo_pathreal;


var cmd_photo = 'raspistill -o '+photo_path;


await exec_photo(cmd_photo, function(error, stdout, stderr){

	console.log('Photo Saved : ',photo_path);

//	require('./mailer').sendEmail(photo_path);
	camcall(photo_pathreal);
});

 }

}

playAlert =  setInterval(function() {
   call();
 }, 3000);

function exit() {

	process.exit();	

}


