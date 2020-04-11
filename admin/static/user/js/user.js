function show_hide(){
    
    // var x=id+1;
    var status =document.getElementById('login_form').style.display;
    // alert(status);
    if (status=="block")
        {  
            //  alert(status);
            document.getElementById('login_form').style.display ="none";
            document.getElementById('register_form').style.display =" block";
            document.getElementById('login_register').innerHTML="Login";
        }
    else { 
        //  alert(status);
        document.getElementById('login_form').style.display =" block";
        document.getElementById('register_form').style.display =" none";
        document.getElementById('login_register').innerHTML="Create an Account";
    }
}

function show_image(src,id){
    target_id=id+'_1';
    // alert(target_id);
    // alert(src);
    document.getElementById(target_id).src=src;
}

function show(id){
    var x="id_"+id;
    document.getElementById(x).style.display= "block";  
    
}

function hide(id){
    var x="id_"+id;
    // alert(x);
    document.getElementById(x).style.display= "none";  
    
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