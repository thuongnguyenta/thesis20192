function bg_id(id){
    var x= document.getElementById(id).style.backgroundColor;
    if (x==""){
    document.getElementById(id).style.backgroundColor="lightgrey";
    }
    else{
        document.getElementById(id).style.backgroundColor=null;
    }
}


function display(id){
    
    // var x=id+1;
    var status =document.getElementById(id).style.display;
    if (status=="block")
        {  
            //  alert(status);
            document.getElementById(id).style.display =" none";
        }
    else { 
        //  alert(status);
            document.getElementById(id).style.display= "block";    
    }
}

function show_hide(id){
    
    var x=id+1;
    var status =document.getElementById(x).style.display;
    if (status=="block")
        {  
            //  alert(status);
            document.getElementById(x).style.display =" none";
        }
    else { 
        //  alert(status);
            document.getElementById(x).style.display= "block";    
    }
}
function show_detail(id){
    var target_id=id+"_3";
    // alert(target_id);
    var status =document.getElementById(target_id).style.display;
    // alert(status)
    if (status=="block")
        {  
            //  alert(status);
            document.getElementById(target_id).style.display =" none";
        }
    else { 
        //  alert(status);
            document.getElementById(target_id).style.display= "block";    
    }

}
function change_image(id,src){
    var target_id=id;
    // alert (target_id);
    // alert (src);
    // var target_src=
    document.getElementById(target_id).src=src;
}

function show_input(id){
    hide_id=id;
    show_id=id+"_input";
    // alert(show_id);
    document.getElementById(hide_id).style.display =" none";
    document.getElementById(show_id).style.display ="block";
}

function show_image(src,id){
    target_id=id+'_1';
    // alert(target_id);
    // alert(src);
    document.getElementById(target_id).src=src;
}
function show_register(){
    document.getElementById('login_form').style.display="none";
    document.getElementById('register').style.display="block"
}
function show_login(){
    document.getElementById('register').style.display="none";
    document.getElementById('login_form').style.display="block"
}

$(document).ready(function(){
    $("#gender").click(function(){
      $("#gendercb").slideToggle("slow");
    });
  });