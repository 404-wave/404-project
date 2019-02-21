//holds all form validations for the app

function redAlert(errorField) {
    console.log(errorField);
    el = document.getElementById("id_"+errorField).parentElement
    el.classList.add("redAlert");
}  
function showTab(){
    el = document.getElementById("content").children;
    tabs = document.getElementById("tabs").children;
    for (var i = 0; i < el.length; i++) {
        if (this == tabs[i]){
            el[i].setAttribute("id", "current");  
            tabs[i].setAttribute("id", "current_tab")
        }
        else {
            el[i].setAttribute("id", "hide_div");  
            tabs[i].setAttribute("id", "hide_tab")
        }
    }
}
function myFunction() {
    el = document.getElementById("content").children;
    tabs = document.getElementById("tabs").children;
    for (var i = 0; i < el.length; i++) {
        el[i].setAttribute("id", "hide_div");  
        tabs[0].setAttribute("id", "hide_tab")
        tabs[i].addEventListener("click", showTab);
    }
    el[0].setAttribute("id", "current");
    tabs[0].setAttribute("id", "current_tab")
}
window.onload = myFunction;
