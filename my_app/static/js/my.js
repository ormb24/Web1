function showResponse(divId) {
    //Debug : window.alert("showResponse")
    //Debug : window.alert(divId.style.display);
    if (divId.style.display === "none") {
       divId.style.display = "block";
    } else {
       divId.style.display = "none";
    }
}
/**
* Name : showHide(myDiv)
* Description : Show / Hide Element by Id
*/
    function showHide(myDiv){
        var x = document.getElementById(myDiv);
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }