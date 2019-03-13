//will show tabs if selected
function showTab(e){
    if (e.target.class == "showing"){
        return;
    }
    var show =  "stream_post";
    var hide = "github_post";  
    var class_show = document.getElementById('stream');
    var class_hide = document.getElementById('github');

    if (e.target.id == "github"){
       show = "github_post";
       hide = "stream_post";
       class_show = document.getElementById('github');
       class_hide = document.getElementById('stream');
    }
    class_show.setAttribute("class", "showing");
    class_hide.classList.remove("showing");
    var hidden = document.getElementsByClassName(hide);
    for (var i of hidden) {
        i.style.display ="none";
    }
    var shown = document.getElementsByClassName(show);
    for (var i of shown) {
        i.style.display ="block";
    }

}
//set up tabs 
//TODO - set up animation (still working on)
function setTabs() {
    var tabs = document.getElementById("tabs").children;
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", showTab);
    }
    var githubs = document.getElementsByClassName('github_post');
    for (var i of githubs) {
        i.style.display ="none";
    }
}

//message for empty
function setEmptyMessage() {
    var githubs = document.getElementsByClassName('github_post');
    if (githubs.length == 0){
        var git = document.getElementById('empty_git');
        git.style.display = "block";
    }
}

