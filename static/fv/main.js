
  let namespace = "/";
  let video = document.querySelector("#video");
  let canvas = document.querySelector("#canvas");
  let ctx = canvas.getContext('2d');
  let photo = document.getElementById('photo');
  var localMediaStream = null;
  var errmsg=document.querySelector("#errmsg");
  imageSent=false;
  age=[];
  gender='';
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  window.count=0;
  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }

    
    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

    let dataURL = canvas.toDataURL('image/jpeg');

    data = JSON.stringify({"image":dataURL,"capture":window.count})

    socket.emit('input image', data);
    
    // socket.emit('output image')


    socket.on('output image',function(data){
  
      if(data.capture==1){
        imageSent=true;
        age=data.data[0];
        gender=data.data[1];
        update(age, gender);
      }
      else if (data.capture==-1 && window.imageSent==false){
        window.count=0
      }
      photo.setAttribute('src', data.image_data);
      if(!imageSent){
        errmsg.innerHTML=data.message;
      }
      
      
      // console.log(window.age, window.gender)
    });

  }

  var constraints = {
    video: {
      height:360,
      width:640
    }
  };
  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    localMediaStream = stream;

    setInterval(function () {
      if(window.count<=3){
        window.count+=1
      }
      else{

      }
      sendSnapshot();
    }, 1000);
  }).catch(function(error) {
    console.log(error);
  });

