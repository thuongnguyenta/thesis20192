// function show_hide(id){
    
//     var x="id_"+id;
//     var status =document.getElementById(x).style.display;
//     // alert(x,status);
//     if (status=="block")
//         {  
//             //  alert(status);
//             document.getElementById(x).style.display =" none";
//         }
//     else { 
//         //  alert(status);
//             document.getElementById(x).style.display= "block";    
//     }
//     alert(document.getElementById(x).style.display);
// }

function show(id){
    var x="id_"+id;
    document.getElementById(x).style.display= "block";  
    
}

function hide(id){
    var x="id_"+id;
    // alert(x);
    document.getElementById(x).style.display= "none";  
    
}


function hide_color(id){
    var x="colour_"+id;
    // alert(x);
    document.getElementById(x).style.display= "none";  
    
}

function show_color(id){
    var x="colour_"+id;
    // alert(x);
    document.getElementById(x).style.display= "block";
}

function hide_order(id){
    var x="order_"+id;
    // alert(x);
    document.getElementById(x).style.display= "none";  
    
}

function show_order(id){
    var x="order_"+id;
    // alert(x);
    document.getElementById(x).style.display= "block";
}


