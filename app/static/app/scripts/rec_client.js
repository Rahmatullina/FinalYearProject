Webcam.set({
  width: 650,
  height: 400,
  image_format: 'jpeg',
  jpeg_quality: 90
 });
Webcam.attach( '#onlineVideo' );


function recognize(){
    Webcam.snap( function(data_uri) {
        sendBase64ToServer(data_uri);
    });
}
function strart_record() {

    recognize();
    // display results in page
    // let timerId = setInterval(recognize, 1000);
}
var sendBase64ToServer = function(base64){
    var request = new XMLHttpRequest(),
        path = "/make_recognition/",
        data = {image: base64};

    request.open("POST", path, true);
    var csrftoken = $.cookie('csrftoken');
    request.setRequestHeader('Content-type', "application/json");
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    request.onload = function() {
      result = JSON.parse(request.responseText);
      document.getElementById('screenshots').innerHTML = '<img src="data:image/jpeg;base64,' + result.image + '"/>';
};
    request.send(JSON.stringify(data));

};