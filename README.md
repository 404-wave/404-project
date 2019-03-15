# 404-project
CMPUT 404 Distributed Social Network


# Licensing and Contributors

Generally, everything is licensed under Apache 2 by [Z-Red](https://github.com/Z-Red).

Contributors: </br>
`
Araien Zach Redfern


Sources</br>
========================</br>
stackoverflow  </br>
TITLE: Make a div into a link </br>
URL:  https://stackoverflow.com/questions/796087/make-a-div-into-a-link </br>
ANSWER: https://stackoverflow.com/a/3494108</br>
AUTHOR: thepeer - https://stackoverflow.com/users/79527/thepeer</br>
## How to run the project locally:
```


# Create a virtual environment
1. virtualenv venv --python=python3

# Activate your virtual environment
2. source venv/bin/activate

# Install all dependencies
3. pip install -r requirements.txt 

# Run database migrations
4. python3 manage.py migrate

# Create a local super user
5. python3 manage.py createsuperuser

# Activate the super user
6. python manage.py shell
   from users.models import User
   user = User.objects.filter(username='{name of superuser created}')[0]
   user.is_active = True
   user.save()

# Run the server locally 
7. python3 manage.py runserver
```

## API

Below there is a list of which endpoints are currently working. Additonally, there is a section of TODOs if something has not yet been implemented.

Note: Pagination works for any endpoint endpoint related to posts or comments.

### Posts

GET service/author/posts: returns all posts visible to the currently authenticated user.

GET service/posts: returns all publicly available posts.

GET service/author/{AUTHOR_ID}/posts: returns all posts from AUTHOR_ID that are visible to the currently authenticated user.

GET service/posts/{POST_ID}: returns a single post if it is visible to the currently authenticated user.

##### TODO...

POST service/posts/{POST_ID}: insert a new post.

PUT service/posts/{POST_ID}: update an existing post.

### Comments

GET service/posts/{POST_ID}/comments: returns all comments in a post if the post is visible to the currently authenticated user.

##### TODO...

POST service/posts/{POST_ID}/comments: add a new comment to an existing post.

### Friendship

GET service/author/{AUTHOR_ID}/friends: returns all friends of AUTHOR_ID.

GET service/author/{AUTHOR_ID1>/friends/{AUTHOR_ID2}: returns a response specifying if AUTHOR_ID1 is a friend of AUTHOR_ID2.

POST service/author/{AUTHOR_ID}/friends: accepts a list of authors and returns a list of authors that are friends of AUTHOR_ID.

POST service/friendrequest: accepts two authors and creates a friend request if they are not already friends.

### Profiles

GET service/author/{AUTHOR_ID}: returns the profile associated with AUTHOR_ID.
