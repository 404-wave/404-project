function filterFriends(opt) {

  // Fetch a list of friends
  path = 'friends/' + opt + '/'; // TODO: replace with REST API endpoint when ready
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
  while (friendContainer.firstChild) {
    friendContainer.removeChild(friendContainer.firstChild);
  }

  // Insert the new users
  // TODO: Create a "card" for each user to be displayed in the list
  for (var i = 0; i < data.length; ++i) {
    $("#friendContainer").append("<div>" + data[i]["fields"]["username"] + "</div>");
  }
}
