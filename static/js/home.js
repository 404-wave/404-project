//will show tabs if selected
function showTab(e){
    var target_id = this.firstElementChild.id
    var target_class = this.firstElementChild.className
    if (target_class == "showing"){
        return;
    }
    var sibling = this.nextElementSibling
    if (sibling == undefined){
        sibling = this.previousElementSibling
    }
    let show_this=target_id
    let hide_this = sibling.firstElementChild.id

    this.firstElementChild.setAttribute("class", "showing");
    sibling.firstElementChild.classList.remove("showing");
    hideElements(hide_this)
    showElements(show_this)
}

function hideElements(class_name){
    var hidden = document.getElementsByClassName(class_name);
    for (var i of hidden) {
        i.style.display ="none";
    }

}
function showElements(class_name){
    var shown = document.getElementsByClassName(class_name);
    for (var i of shown) {
        i.style.display ="block";
    }

}

//set up tabs 
//TODO - set up animation (still working on)
function setTabs() {
    var tabs = document.getElementsByClassName("tabs")
    for (li_num of tabs) {
        for (let i = 0; i<li_num.children.length; i++){
            li_num.children[i].addEventListener("click", showTab);
        }
    }
    hideElements('github_post');
    hideElements('upload_image');
}

    //Creating a textarea with auto-resize
    //https://stackoverflow.com/questions/454202/creating-a-textarea-with-auto-resize
    //DreamTeK -https://stackoverflow.com/users/2120261/dreamtek
    // Annswer - https://stackoverflow.com/posts/25621277/revisions
function auto_text(){
    $('textarea').each(function () {
        this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
      }).on('input', function () {
        this.style.height = 50+ 'px';
        this.style.height = (this.scrollHeight) + 'px';
        isActive(this);
      })
      .on('focus', function () {
        $('.settingss').show()
    })
      .on('blur', function () {
          isActive(this);})
      
          ;
    $("#id_privacy").change(function(){
        private();
       })}


function file_listener(){
    $('#id_image').on('click', function(){
        $('.settingss').show();
    })
}

      
function isActive(e){
    var text = e.value;
    if (text == ""){
        $('.settingss').hide()
    }
    else {
        $('.settingss').show()
    }
}

function private(){
    var values = $("#id_privacy").val();
  if(values == 1){
    $("#id_accessible_users").show();
  }
  else
    $("#id_accessible_users").hide();
}
  



//message for empty
function setEmptyMessage() {
    var githubs = document.getElementsByClassName('github_post');
    if (githubs.length == 0){
        var git = document.getElementById('empty_git');
        git.style.display = "block";
    }
}

function setMarkdown2(){
    var converter = new showdown.Converter(),
    text = $('textarea')[0].value
    html = converter.makeHtml(text);
    elem.innerHTML = html;
}
function setStreamMarkdown(){
    var markdown = $('.markdown');
    for (let value of markdown) { 
        setMarkdown(value.children); 
}}

function setMarkdown(elem){
    var converter = new showdown.Converter(),
    text = elem[0].innerHTML;
    html = converter.makeHtml(text);
    elem.innerHTML = html;
}