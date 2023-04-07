function showResponse(divId) {
    //Debug : window.alert("showResponse")
    //Debug : window.alert(divId.style.display);
    if (divId.style.display === "none") {
       divId.style.display = "block";
    } else {
       divId.style.display = "none";
    }
}