var emo_dict = {};
var timer;
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

function stop_record(){
//     const unique = (value, index, self) => {
//   return self.indexOf(value) === index
// }
    clearInterval(window.timer);
    console.log('stop');
    // for (key in emo_dict){
    //         uniq = emo_dict[key].filter(unique);
    //         emo_dict[key] = uniq;
    // }
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var id = urlParams.get('id');
    console.log(id);
    var request = new XMLHttpRequest(),
        path = "/save/";
        data={'emo_dict':emo_dict,'id':id};
    request.open("POST", path, true);
    var csrftoken = $.cookie('csrftoken');
    request.setRequestHeader('Content-type', "application/json");
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    request.onload = function(){
        alert('Data SAVED');
        window.location.href="/";
    };
    request.send(JSON.stringify(data));
}

function start_record() {

    window.timer = setInterval(() => recognize(), 10000);
    console.log('start');
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
        console.log(request.responseText);
        var result = JSON.parse(request.responseText);
        document.getElementById('screenshots').innerHTML = '<img src="data:image/jpeg;base64,' + result.image + '"/>';
        console.log(result);
        var tmp_dict = result['student_dict'];
        var html="";
        for(s in tmp_dict){
            var val = tmp_dict[s];
            if (s in window.emo_dict){
                if( val in window.emo_dict[s]){
                    window.emo_dict[s][val]+=1;
                }
                else
                    window.emo_dict[s][val] = 1;
            }
            else{
                window.emo_dict[s]={};
                window.emo_dict[s][val]=1 ;

            }
        }
        for (el in window.emo_dict){
            html += ("<li><a href=\"#\">" + el + " ={ ");
                for (el2 in window.emo_dict[el]){
                    html += el2 + " " + window.emo_dict[el][el2];
                }
            html+=("}</a></li>")
        }
        console.log(html);
        document.getElementById('rec_stud').innerHTML=html;

};
    request.send(JSON.stringify(data));

};