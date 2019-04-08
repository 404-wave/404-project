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
    $("#id_accessible_users").prev().show()
    $("#id_accessible_users").show();
  }
  else{
    $("#id_accessible_users").prev().hide()
    $("#id_accessible_users").hide();
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

function setMarkdown2(){
    var converter = new showdown.Converter({'strikethrough': 'true'});
    text = $('textarea')[0].value
    html = converter.makeHtml(text);
    elem.innerHTML = html;
}
function setStreamMarkdown(){
    var markdown = $('.markdown');
    for (let value of markdown) { 
        setMarkdown(value.children[0]); 
}}

function setMarkdown(elem){
    var converter = new showdown.Converter({'strikethrough': 'true', 
    'simplifiedAutoLink': 'true',
'simpleLineBreaks': 'true'});
    converter.setFlavor('github');
    text = elem.innerHTML;
    html = converter.makeHtml(text);
    elem.innerHTML = html;
}
function checkFromOtherNode(localUser,foreignUser,server,nodeUsername,nodePassword){
    let path = standardizeUrl(server)+"service/author/"+foreignUser+"/friends/";
    $.ajax({
      url:path,
      type:"GET",
      headers: {"Authorization":"Basic "+btoa(nodeUsername+":"+ nodePassword)},
      success: function(response){
        console.log("Successfully got foreign user following list");
        let content = response;
        let foreignList = content['authors'];
        let foreignFriends = [];
        foreignList.forEach((url)=>{
          let friend = url.split("/").pop();
          foreignFriends.push(friend);
        });
        console.log(foreignFriends);
        console.log(localUser);
        if ( foreignFriends && !foreignFriends.includes(localUser) ){
           console.log("Foreign unfollow. Removing from dB");
           changeFollowDB(localUser,foreignUser);
         }
      },
      error: function(xhr,status,error){
        console.log("error: " + error);
      }
    });
  }

// function removeFromNotifs(localUser,foreignUser){
//     let path = 'change_ModelDatabase/';

//     $.ajax({
//         url:path,
//         type:"POST",
//         data: {'local':localUser,'foreign':foreignUser,'follows':"false",
//         },
//         headers:{"x-csrftoken":csrfToken},
//         dataType:"json",
//         success: function(data){
//         console.log("Succesfully removed user from FRs");
//         },
//         error: function(xhr,status,error){
//         console.log("error: ", error, status,xhr);
//         }
//     });
// }

function stripProtocol(server){
    let newServer = server;
    if (server.startsWith("https://")){
      newServer = server.replace(/^https?\:\/\//i, "");
    }
    return newServer;
}

function changeFollowDB(localUser,foreignUser){
    let path = 'friends/change_ModelDatabase/';
  
    $.ajax({
      url:path,
      type:"POST",
      data: {'local':localUser,'foreign':foreignUser,'follows':"delete"},
      headers: {"x-csrftoken":csrfToken},
      dataType:"json",
      success: function(data){
        console.log("Succesfully changed Follow DB");
      },
      error: function(xhr,status,error){
        console.log("error: ", error, status,xhr);
      }
    });
}

function checkChanges(localUser,localUserServer,nodeList){

    let path1 = standardizeUrl(localUserServer)+"service/author/"+localUser+"/friends/";
    let localFriends;
    $.ajax({
      //checks if the local user followed them back
      url: path1,
      success: function(content){
        localFriends= content['authors'];

        if (localFriends){
            for(let i=0;i<localFriends.length;i++){
              let friend = localFriends[i];

              let url = friend.split("/");
              let hostname = standardizeUrl(url[2]);

              if (hostname != standardizeUrl(localUserServer)){
                let friendID = url.pop();
                let userPassObj = findNodeUserAndPass(JSON.parse(nodeList),hostname);
                let nodeUsername = userPassObj['username'];
                let nodePassword = userPassObj['password'];

                checkFromOtherNode(localUser,friendID,hostname,nodeUsername,nodePassword);

              }
            }
        }

      },
      error: function(xhr,status,error){
        console.log("Error: ",error, status);
      }
    });
}

function standardizeUrl(url){
  let serverUrl = url.replace(/\s+/g,"");
  if(serverUrl.endsWith("/") == false){
    serverUrl = serverUrl + "/";
  }
  if(serverUrl.startsWith("http://")== true){
    serverUrl = serverUrl.split("http://").pop();
    serverUrl = "https://"+serverUrl;
  }
  else if(/^https?:\/\//.test(serverUrl) == false){ 
    serverUrl = "https://"+serverUrl;
  }
  return serverUrl;
}

function findNodeUserAndPass(nodeList,server){
  for(let node in nodeList){
    let stand_node = standardizeUrl(node);
    if (stand_node == server){
      let data = {
        'username':nodeList[node]['username'],
        'password':nodeList[node]['password']
      };
      return data;
    }
  }
}
function strip_host(host){
  reg = /\/.*\/$/gi;
  var k = host.replace(reg, '');
  return k;
}

function findDisplayName(user,node, e) {
  console.log(user);
  path = user;
  $.ajax({
    url: path,
    success: function (data) {
      changeDisplayName(data, node);
    },
    error: function(xhr, status, error) {
      console.log(error)
    } 
  });
}

function changeDisplayName(data, node){
  node.childNodes[0].childNodes[1].textContent = " "+data['displayName']
}

function populateAccessibleList(){
  var select_parent = $('#id_accessible_users')[0];
  var select = select_parent.children;
  var size = select.length;
  var host = window.location.protocol+'//'+window.location.host
  for (i=0; i<select.length; i++){
    var name = select[i].firstChild.firstChild.value;
    if (!name.includes(host)){
      findDisplayName(name, select[i])
    }
  }

}
function home_js(){
  setTabs();
  setEmptyMessage();
  auto_text();
  private();
  file_listener();
  setStreamMarkdown();
  populateAccessibleList();
}