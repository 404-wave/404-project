function filterFriends(opt, e) {

  // Fetch a list of friends
  path = opt + '/'; // TODO: replace with REST API endpoint when ready
  $.ajax({
    url: path,
    success: function (data) {
      populateFriendsList(data);
      active_friend_button(e);
    },
    error: function(xhr, status, error) {
      console.log(error)
    } 
  });
}

function active_friend_button(e){
  var buttons = document.getElementsByClassName('friend_btn active');
  if (buttons.length > 0){
    buttons[0].className = 'friend_btn';
  }
  e.className  += " active";
}

// TODO: needs adaptation pending finalization of JSON structure of REST API
function populateFriendsList(data) {

  // Remove the users in the friends list
  friendContainer = document.getElementById("friendContainer");
  while (friendContainer.firstChild) {
    friendContainer.removeChild(friendContainer.firstChild);
  }
  // Insert the new users
  for (var i = 0; i < data.length; ++i) {
    console.log(data);
    console.log(data[i]);
    let id = data[i]["pk"];
    let host = data[i]["fields"]["host"];
    host = strip_host(host);
    let username = data[i]["fields"]["username"];
    let image = '<img src="/static/images/singleslothwave.png" alt=${username} width="35">'
    let div = `<div class="friend_name">${image}<a href=\"../profile/${host}${id}\">${username}</a></div>`;
    $("#friendContainer").append(div)
  }
}

function strip_host(host){
  reg = /https?:\/\//gi;
  var k = host.replace(reg, '');
  k = k.replace(/\/$/gi, '')
  return k;
}


function change_follow(followerID,followerUser,followerHost,
  followeeID,followeeUser,followeeHost,e) {
  let url_val = 'follow/';
  if (e.id != "Follow"){
    url_val = "unfollow/";
  }
  
  $.ajax({
    url: url_val,
    data: {      
      followerID: followerID,
      followeeID: followeeID,
      followerUser: followerUser,
      followeeUser: followeeUser,
      'followeeserver': standardizeUrl(followeeHost),
      'followerserver':standardizeUrl(followerHost),
    },
    success: function (data) {
 
      if (standardizeUrl(followerHost) != standardizeUrl(followeeHost) && e.id == "Follow"){
        addFromOtherNode(data);
      }
      switchButton(data, e);
      //eplaceUnfollowButton(data);
    },
    error: function(xhr, status, error) {
      console.log(error)
    }
  });
}


function switchButton(data, button) {
  let followerID = data['followerID'];
  let followeeID = data['followeeID'];
  var text_val = "Unfollow";
  let div = document.getElementById(button.id);
  if (button.id != "Follow") {
      text_val = "Follow";
  }
    div.innerText = text_val;
    button.id = text_val;
}

function checkChanges(localUser,localUserServer,requestor,requestorServer){
  console.log("WE IN HEREEEE");
  let path1 = standardizeUrl(localUserServer)+"author/"+localUser+"/friends/"+stripProtocol(standardizeUrl(requestorServer))+requestor;
  let path2 = 'getNodeList/';
  $.ajax({
    //checks if the local user followed them back
    url: path1,
    success: function(content){
      console.log("Successfully retrieved if local author followed back")
      let contents = content;
      let isFriends= contents['friends'];
      if (isFriends){
        console.log("about to remove notifs")
        removeFromNotifs(localUser,requestor);
      }
    },
    error: function(xhr,status,error){
      console.log("Error: ",error, status);
    }
  });
  $.ajax({
    url:path2,
    success: function(data){
      let content = findNodeUserAndPass(data,requestorServer);
      let nodeUser = content['username'];
      let nodePass = content['password'];
      checkFromOtherNode(localUser,requestor,requestorServer,nodeUser,nodePass);
    }

  })
}

function stripProtocol(server){
  let newServer = server;
  if (server.startsWith("https://")){
    newServer = server.replace(/^https?\:\/\//i, "");
  }
  return newServer;
}
function removeFromNotifs(localUser,foreignUser){
  let path = 'change_ModelDatabase/';
  $.ajax({
    url:path,
    type:"POST",
    data: {'local':localUser,'foreign':foreignUser,'follows':"false",
    "x-csrftoken":getCookie("csrftoken")},
    dataType:"json",
    success: function(data){
      console.log("Succesfully removed user from FRs");
    },
    error: function(xhr,status,error){
      console.log("error: ", error, status,xhr);
    }
  });
}

function changeFollowDB(localUser,foreignUser){
  let path = 'change_ModelDatabase/';
  $.ajax({
    url:path,
    type:"POST",
    data: {'local':localUser,'foreign':foreignUser,'follows':"delete",
    "x-csrftoken":getCookie("csrftoken")},
    dataType:"json",
    success: function(data){
      console.log("Succesfully changed Follow DB");
    },
    error: function(xhr,status,error){
      console.log("error: ", error, status,xhr);
    }
  });
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
      let foreignUserFollowList = content['authors'];
      if (!foreignUserFollowList.includes(localUser) ){
        console.log("Foreign unfollow. Removing from dB")
        removeFromNotifs(localUser,foreignUser);
        changeFollowDB(localUser,foreignUser);
      }
    },
    error: function(xhr,status,error){
      console.log("error: " + error);
    }
  });
}

function replaceUnfollowButton(data) {

  let followerID = data["followerID"];
  let followeeID = data["followeeID"];

  let div = `<button onClick="follow(${followerID}, ${followeeID})">Follow</button>`;

  followBtnContainer = document.getElementById("followBtnContainer");
  while (followBtnContainer.firstChild) {
    followBtnContainer.removeChild(followBtnContainer.firstChild);
  }

  $("#followBtnContainer").append(div);
}

function displayNotifications(data){
  //TODO should make it look nicer
  let div = document.getElementById("friend_reqs_container");
  let button = document.getElementById("friend_reqs_button");
  div.style.padding= '0';
  div.style.margin = '0';
 
  button.innerHTML = `Friend Requests <span id='notif'>(${data})</span> `;
}

function filterRequests(){
  let path = "friend_requests/";
  $.ajax({
    url:path,
    success: function(data){
        populateRequests(data);
    },
    error: function(xhr, status, error) {
      console.log(error)
    }
  });
}


function populateRequests(data){
  // Remove the users in the friends list
  dropdown = document.getElementById("dropdown");
  while (dropdown.firstChild) {
    dropdown.removeChild(dropdown.firstChild);
  }
  //insert users
  for (var x = 0; x < data['posts'].length; ++x) {
    let id = data['posts'][x]['id'];
    let host = data['posts'][x]['host'];
    let username = data['posts'][x]['username'];
    let div = `<div><a href=\"../profile/${host}${id}\">${username}</a></div>`;
    $("#dropdown").append(div)
  }
  dropdown.classList.toggle("show");
}


function closeDropDown(){
  //Credit https://www.w3schools.com/howto/howto_js_dropdown.asp
  //allows dropdown to disappear when user clicks anything but the menu
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdwn-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
}

function addFromOtherNode(data){
  
  const followerID = data['followerID'];
  const followeeID = data['followeeID'];
  let serverUrl = data['followeeServer'];
  serverUrl = standardizeUrl(serverUrl);
  let hostUrl = data['followerServer'];
  hostUrl = standardizeUrl(hostUrl);
  
  let nodeList = data['nodes']; 
  let userPassObj = findNodeUserAndPass(nodeList,serverUrl);
  const nodeUsername = userPassObj['username'];
  const nodePassword = userPassObj['password'];
  console.log("NODEUSERNAME:");
  console.log(nodeUsername);
  console.log("NODEPASSWORD:");
  console.log(nodePassword);

  const followerUsername = data['followerUser'];
  const followeeUsername = data['followeeUser']; 
  let path = serverUrl+"service/friendrequest/";
  path = path.replace(/\s+/g, "");

  const request_user_url = hostUrl+"author/"+followerID;
  const req_profile_url = hostUrl+"author/"+followerID;
  const recip_user_url = serverUrl+"author/"+followeeID;
  const recip_profile_url = serverUrl+"author/"+followeeID;

  let payload = {
    "query":"friendrequest",
    "author": {
        "id":  request_user_url,
        "host": hostUrl,
        "displayName": followerUsername,
        "url":req_profile_url,
        },  
    "friend": {
        "id": recip_user_url,
        "host": serverUrl,
        "displayName": followeeUsername,
        "url": recip_profile_url
    }
  };

  console.log(JSON.stringify(payload,null,2));

  $.ajax({
    url:path,
    type:"POST",
    data:JSON.stringify(payload),
    dataType: "json",
    contentType: "application/json",
    headers: {"Authorization":"Basic "+btoa(nodeUsername+":"+ nodePassword),
                "x-csrftoken":csrfToken,
                "content-type": "application/json"},
    success: function(){
      console.log("Successfully sent Request to Other Server");
    },
    error: function(xhr,status,error){
      console.log("error: Problem sening ajax request \t",error);
    }
  });
}

// function tempAddNode(){
//   let path = "https://myblog-cool.herokuapp.com/"+"service/friendrequest/";
//   let payload = {
//     "query":"friendrequest",
//     "author": {
//         "id":  "https://fast-forest-91959.herokuapp.com/author/aa2d733d-e1b9-413c-a046-dc93b31fd9ac",
//         "host": "https://fast-forest-91959.herokuapp.com/",
//         "displayName": "test",
//         "url":"https://fast-forest-91959.herokuapp.com/author/aa2d733d-e1b9-413c-a046-dc93b31fd9ac",
//         },  
//     "friend": {
//         "id": "https://myblog-cool.herokuapp.com/author/f6ea3270-3e4d-4547-9ee6-8def7f1fe01a",
//         "host": "https://myblog-cool.herokuapp.com/",
//         "displayName": "Jackson0",
//         "url": "https://myblog-cool.herokuapp.com/author/f6ea3270-3e4d-4547-9ee6-8def7f1fe01a"
//     }
//   };

//   console.log(JSON.stringify(payload,null,2));
//   $.ajax({
//     url:path,
//     type:"POST",
//     data:JSON.stringify(payload),
//     dataType:"json",
//     contentType:"application/json",
//     username: "kerry",
//     password: "kerrypassword",
//     success: function(){
//       console.log("Successfully sent ");
//     },
//     error: function(xhr,status,error){
//       console.log("error: ", error,status);
//     }
    
//   });
// }
function standardizeUrl(url){
  let serverUrl = url.replace(/\s+/g,"");
  if(serverUrl.endsWith("/") == false){
     serverUrl = serverUrl + "/";
  }
  if(serverUrl.indexOf("https://") === -1){ 
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