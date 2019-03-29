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
    let id = data[i]["pk"];
    let host = data[i]["fields"]["host"];
    host = strip_host(host)
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
      'followeeserver': followeeHost,
      'followerserver':followerHost,
    },
    success: function (data) {
      if (followerHost != followeeHost && e.id == "Follow"){
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

// function checkOtherNodes(user,requestorID,requestorServer){
//   let path = '/friends';
//   $.ajax({
//     url: path,
//     success:  function(data){
//       removeUnfollows(data,requestorID,requestorServer);
//     },
//     error: function(xhr,status,error){
//       console.log("Error: ",error, status);
//     }
//   })
// }

// function removeUnfollows(data,follower,server){

//   // let authorFriends = new Set();
//   // for (let userobj in data){
//   //   let id = data[userobj]["pk"];
//   //   authorFriends.add(id);
//   // }
  
//   authorFriends = Array.from(authorFriends);
//   let path = standardizeUrl(server)+"service/author"+follower;
//   $.ajax({
//     url:path,
//     type:"GET",
//     success: function(response){
//       let content = JSON.parse(repsonse);
//       let friendList = content['authors'];
//       for (let i=0; i<authorFriends.length;i++){
//         if ()
//       }

//     }
//   })
//}
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
    headers: {"Authorization":"Basic "+nodeUsername+":"+nodePassword,
                "x-csrftoken":csrfToken,
                "cache-control": "no-cache"},
    success: function(){
      console.log("Successfully sent Request to Other Server");
    },
    error: function(xhr,status,error){
      console.log("error: ",error);
    }
  });

}

function tempAddNode(){
  let path = "https://myblog-cool.herokuapp.com/"+"service/friendrequest/";
  let payload = {
    "query":"friendrequest",
    "author": {
        "id":  "https://fast-forest-91959.herokuapp.com/author/aa2d733d-e1b9-413c-a046-dc93b31fd9ac",
        "host": "https://fast-forest-91959.herokuapp.com/",
        "displayName": "test",
        "url":"https://fast-forest-91959.herokuapp.com/author/aa2d733d-e1b9-413c-a046-dc93b31fd9ac",
        },  
    "friend": {
        "id": "https://myblog-cool.herokuapp.com/author/f6ea3270-3e4d-4547-9ee6-8def7f1fe01a",
        "host": "https://myblog-cool.herokuapp.com/",
        "displayName": "Jackson0",
        "url": "https://myblog-cool.herokuapp.com/author/f6ea3270-3e4d-4547-9ee6-8def7f1fe01a"
    }
  };

  console.log(JSON.stringify(payload,null,2));
  $.ajax({
    url:path,
    type:"POST",
    data:JSON.stringify(payload),
    dataType:"json",
    contentType:"application/json",
    username: "kerry",
    password: "kerrypassword",
    success: function(){
      console.log("Successfully sent ");
    },
    error: function(xhr,status,error){
      console.log("error: ", error,status);
    }
    
  });
}
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