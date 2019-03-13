function filterFriends(opt) {

  // Fetch a list of friends
  path = opt + '/'; // TODO: replace with REST API endpoint when ready
  $.ajax({
    url: path,
    success: function (data) {
      populateFriendsList(data);
    },
    error: function(xhr, status, error) {
      console.log(error)
    }
  });
}


// TODO: needs adaptation pending finalization of JSON structure of REST API
function populateFriendsList(data) {

  // Remove the users in the friends list
  friendContainer = document.getElementById("friendContainer");
  while (friendContainer.firstChild) {
    friendContainer.removeChild(friendContainer.firstChild);
  }
  // Insert the new users
  // TODO: Create a "card" for each user to be displayed in the list
  for (var i = 0; i < data.length; ++i) {
    let id = data[i]["pk"];

    let username = data[i]["fields"]["username"];
    let div = `<div><a href=\"../profile/${id}\">${username}</a></div>`;
    $("#friendContainer").append(div)
  }
}


function follow(followerID, followeeID, e) {

  $.ajax({
    url: "follow/",
    data: {
      followerID: followerID,
      followeeID: followeeID
    },
    success: function (data) {
      switchButton(data);
    },
    error: function(xhr, status, error) {
      console.log(error)
    }
  });
}

function unfollow(followerID, followeeID, e) {

  $.ajax({
    url: "unfollow/",
    data: {
      followerID: followerID,
      followeeID: followeeID
    },
    success: function (data) {
      replaceUnfollowButton(data);
    },
    error: function(xhr, status, error) {
      console.log(error)
    }
  });
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
