function filterFriends(opt) {

  // Remove the users in the friends list
  friendContainer = $("#friendContainer")[0];
  for (var i = 0; i <= friendContainer.childElementCount; ++i) {
    friendContainer.removeChild(friendContainer.childNodes[i]);
  }

  // Fetch a list of friends
  if (opt === "find") {
    $.ajax({
      url: 'friends/find/', // TODO: replace with REST API endpoint when ready
      success: function (data) {
        populateFriendsList(data)
      }
    });
  } else if (opt === "friends" || opt === "following") {
    // $.ajax({
    //   url: '/friends/' + opt + '/',
    //   data: {
    //     'user_id': {{ user.user_id}}
    //     'opt': opt
    //   },
    //   dataType: 'json',
    //   success: populateFriendsList(data)
    // });
  }

}

// TODO: needs adaptation pending finalization of JSON structure of REST API
function populateFriendsList(data) {
  for (var i = 0; i < data.length; ++i) {
    $("#friendContainer").append("<div>" + data[0]["fields"]["username"] + "</div>");
  }
}
