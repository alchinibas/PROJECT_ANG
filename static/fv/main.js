$(document).ready(function(){
  let namespace = "/";
  let video = document.querySelector("#video");
  let canvas = document.querySelector("#canvas");
  let ctx = canvas.getContext('2d');
  let photo = document.getElementById('photo');
  var localMediaStream = null;

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }

    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

    let dataURL = canvas.toDataURL('image/jpeg');

    
    socket.emit('input image', dataURL);
    
    // socket.emit('output image')


    socket.on('output image',function(data){


    photo.setAttribute('src', data.image_data);

    });


  }

  var constraints = {
    video: true
  };
  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    localMediaStream = stream;

    setInterval(function () {
      sendSnapshot();
    }, 50);
  }).catch(function(error) {
    console.log(error);
  });

});