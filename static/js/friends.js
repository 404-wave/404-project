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
    let username = data[i]["fields"]["username"];
    let image = '<img src="/static/images/singleslothwave.png" alt=${username} width="35">'
    let div = `<div class="friend_name">${image}<a href=\"../profile/${id}\">${username}</a></div>`;
    $("#friendContainer").append(div)
  }
}


function change_follow(followerID, followeeID, e) {
  var url_val = "follow/";
  if (e.id != "Follow"){
    url_val = "unfollow/";
  }
  $.ajax({
    url: url_val,
    data: {
      followerID: followerID,
      followeeID: followeeID
    },
    success: function (data) {
      switchButton(data, e);
      //eplaceUnfollowButton(data);
    },
    error: function(xhr, status, error) {
      console.log(error)
    }
  });
}


function switchButton(data, button) {
  let followerID = data["followerID"];
  let followeeID = data["followeeID"];
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

