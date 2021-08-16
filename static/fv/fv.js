
update = function(){
    var ageELem = document.getElementById("age");
    if(imageSent==true){
        if (ageELem.value<18){
            errmsg.innerHTML="You should be gareater than 18";
        }
        else if(ageELem.value>=age[0] && ageELem.value<=age[1]){
            errmsg.innerHTML="Everything is fine";
        }
        else{
            errmsg.innerHTML="Your age didn't match."
        }
    }
}
