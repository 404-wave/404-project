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
      try {
        friends = data['friends'];
        for (item of friends) {
          requestDisplayNameFriend(item);
      }
    }
    catch(e){
      populate_names(data);
    }
    }

function populate_names(data){
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
// TODO: needs adaptation pending finalization of JSON structure of REST API
function populatefriends(data) {
      var re = new RegExp('(.*)([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$)');
      var id = data['id'];
      var result = id.match(re);
      id = result[2];
      re = new RegExp('^https?:\/\/([^\/]*)');
      var host = data['host'];
      result = host.match(re);
      host = result[1];
      let image = '<img src="/static/images/singleslothwave.png" alt=${username} width="35">'
      var username = data['displayName'];
      let div = `<div class="friend_name">${image}<a href=\"../profile/${host}${id}\">${username}</a></div>`;
      $("#friendContainer").append(div)
}


function requestDisplayNameFriend(user) {
  console.log(user);
  path = user;
  $.ajax({
    url: path,
    success: function (data) {
      populatefriends(data);
    },
    error: function(xhr, status, error) {
      console.log(error)
    } 
  });
}

function strip_host(host){
  reg = /https?:\/\//gi;
  var k = host.replace(reg, '');
  k = k.replace(/\/$/gi, '');
  return k;
}

function RequestDisplayName(user) {
  console.log(user);
  path = user;
  $.ajax({
    url: path,
    success: function (data) {
      populateDropDown(data);
    },
    error: function(xhr, status, error) {
      console.log(error)
    } 
  });
}


function populateDropDown(data){
  // Remove the users in the friends list
  dropdown = document.getElementById("dropdown");
  while (dropdown.firstChild) {
    dropdown.removeChild(dropdown.firstChild);
  }
  var re = new RegExp('(.*)([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$)');
  var id = data['id'];
  var result = id.match(re);
  id = result[2];
  re = new RegExp('^https?:\/\/([^\/]*)');
  var host = data['host'];
  result = host.match(re);
  host = result[1];
  var username = data['displayName'];
  var div = `<div><a href=\"../profile/${host}${id}\">${username}</a></div>`;
    $("#dropdown").append(div)
  dropdown.classList.toggle("show");
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
  var friends = data['friends'];
  for (item of friends)
    {RequestDisplayName(item)}
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
  let path = serverUrl+"friendrequest/";
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
    console.log("NODE:");
    console.log(stand_node);
    console.log("SERVER:")
    console.log(server);
    
    if (stand_node == server){
      let data = {
        'username':nodeList[node]['username'],
        'password':nodeList[node]['password']
      };
      return data;
    }
  }
}