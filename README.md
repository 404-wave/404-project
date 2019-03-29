# 404-project
CMPUT 404 Distributed Social Network


# Licensing and Contributors

Generally, everything is licensed under Apache 2 by [Z-Red](https://github.com/Z-Red).

Contributors: </br>
```
Araien Zach Redfern 
Austin PennyFeather 
Kerry Li 
Allison Boukall 
Shu-Jun Pierre Lin 
```

Sources</br>
========================</br>
stackoverflow  </br>
TITLE: Make a div into a link </br>
URL:  https://stackoverflow.com/questions/796087/make-a-div-into-a-link </br>
ANSWER: https://stackoverflow.com/a/3494108</br>
AUTHOR: thepeer - https://stackoverflow.com/users/79527/thepeer</br>

## How to set up nodes

On the remote server:</br>

1.) Create an account for the local host using the registration page</br>
2.) go to the admin page</br>
3.) find the node you added as a USER (user table). </br>
4.) set the “is-active” to true</br>
5.) set the HOST to be the HOSTNAME for that node. (http://127.0.0.1:8000 for localhosts)</br>
6.) save</br>
On the local host:v
1.) go to the admin interface</br>
2.) add a new row in the Node table</br>
3.) set the HOST to be the host you are CONNECTING TO (http://Heroku whatever...)</br>
4.) add the username and password you set up in the last set of steps</br>
Think of it like this.... on any node, you need other nodes to authenticate with you, so the foreign nodes must be _users_.</br>

But, when you want to add foreign nodes to _get info from_, you just add them to the Node table</br>
</br>
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

Below there is a list of which endpoints are currently working. Additonally, there is a section of TODOs if something has not yet been implemented. Right now, it doesn't really matter if the the "id" of authors has a prepended host, since the host usually comes with the request or request body anyways.

Note: Pagination works for any endpoint endpoint related to posts or comments.

### Posts

GET service/author/posts: returns all posts visible to the currently authenticated user.

GET service/posts: returns all publicly available posts.

GET service/author/{AUTHOR_ID}/posts: returns all posts from AUTHOR_ID that are visible to the currently authenticated user.

GET service/posts/{POST_ID}: returns a single post if it is visible to the currently authenticated user.

An example response:
```
{
    "query": "posts",
    "count": 4,
    "size": 1,
    "next": "http://127.0.0.1:8000/service/author/1900e266-dd80-455b-b9dd-abf09c14116e/posts?page=4&size=1",
    "previous": "http://127.0.0.1:8000/service/author/1900e266-dd80-455b-b9dd-abf09c14116e/posts?page=2&size=1",
    "posts": [
        {
            "id": 2,
            "user": "1900e266-dd80-455b-b9dd-abf09c14116e",
            "contentType": "text/plain",
            "published": "2019-03-15T15:22:21.421428Z",
            "content": "This should be a private post from zach that no one should see.",
            "author": {
                "id": "http://127.0.0.1:8000/1900e266-dd80-455b-b9dd-abf09c14116e",
                "host": "http://127.0.0.1:8000/",
                "displayName": "zredfern",
                "url": "http://127.0.0.1:8000/home/profile/1900e266-dd80-455b-b9dd-abf09c14116",
                "github": "Z-Red"
            },
            "comments": [],
            "visibility": "PRIVATE",
            "visible_to": [],
            "unlisted": false
        }
    ]
}
```

##### TODO...

POST service/posts/{POST_ID}: insert a new post.

PUT service/posts/{POST_ID}: update an existing post.

### Comments

**GET service/posts/{POST_ID}/comments**: returns all comments in a post if the post is visible to the currently authenticated user.

Response:
```
{
    "query": "comments",
    "count": 2,
    "size": 50,
    "next": null,
    "previous": null,
    "comments": [
        {
            "author": {
                "id": "http://127.0.0.1:8000/e114cd5f-6efb-41d6-a220-24be52eeb139",
                "url": "http://127.0.0.1:8000/home/profile/e114cd5f-6efb-41d6-a220-24be52eeb139",
                "host": "http://127.0.0.1:8000/",
                "displayName": "tred",
                "github": ""
            },
            "comment": "Great public post Zach! Ha ha lol rofl",
            "contentType": "text/plain",
            "published": "2019-03-15T15:35:09.863373Z",
            "id": 1
        },
        {
            "author": {
                "id": "http://127.0.0.1:8000/1900e266-dd80-455b-b9dd-abf09c14116e",
                "url": "http://127.0.0.1:8000/home/profile/1900e266-dd80-455b-b9dd-abf09c14116",
                "host": "http://127.0.0.1:8000/",
                "displayName": "zredfern",
                "github": "Z-Red"
            },
            "comment": "Thank you, Mother.",
            "contentType": "text/plain",
            "published": "2019-03-15T15:37:54.384661Z",
            "id": 2
        }
    ]
}
```

##### TODO...

POST service/posts/{POST_ID}/comments: add a new comment to an existing post.

### Friendship

**GET service/author/{AUTHOR_ID}/friends**: returns all friends of AUTHOR_ID.

Response:
```
{
    "query": "friends",
    "authors": [
        "88939ffa-c45d-4c10-a4f0-252ccf87740c"
    ]
}
```

**GET service/author/{AUTHOR_ID1>/friends/{AUTHOR_ID2}**: returns a response specifying if AUTHOR_ID1 is a friend of AUTHOR_ID2.

Response:
```
{
    "query": "friends",
    "authors": [
        "http://127.0.0.1:8000/author/1900e266-dd80-455b-b9dd-abf09c14116e",
        "http://127.0.0.1:8000/author/88939ffa-c45d-4c10-a4f0-252ccf87740c"
    ],
    "friends": true
}
```

**POST service/author/{AUTHOR_ID}/friends**: accepts a list of authors and returns a list of authors that are friends of AUTHOR_ID.

Request:
```
{
	"query":"friends",
	"author":"http://127.0.0.1:8000/author/1900e266-dd80-455b-b9dd-abf09c14116e",
	"authors": [
	   "http://127.0.0.1:8000/author/de305d54-75b4-431b-adb2-eb6b9e546013",
		"http://127.0.0.1:8000/author/88939ffa-c45d-4c10-a4f0-252ccf87740c",
  	]
}
```

Response:
```
{
	"query":"friends",
 	"author":"http://127.0.0.1:8000/author/1900e266-dd80-455b-b9dd-abf09c14116e",
	"authors": [
		"http://127.0.0.1:8000/author/88939ffa-c45d-4c10-a4f0-252ccf87740c",
  	]
}
```

**POST service/friendrequest**: accepts two authors and creates a friend request if they are not already friends.

Request:
```
{
	"query":"friendrequest",
	"author": {
		"id":"http://127.0.0.1:8000/author/1900e266-dd80-455b-b9dd-abf09c14116e",
		"host":"http://127.0.0.1:8000/",
		"displayName":"zredfern",
      "url":"http://127.0.0.1:8000/author/1900e266-dd80-455b-b9dd-abf09c14116e",
	},
	"friend": {
		"id":"http://127.0.0.1:8000/author/88939ffa-c45d-4c10-a4f0-252ccf87740c",
		"host":"http://127.0.0.1:8000/",
		"displayName":"bpanda",
      "url":"http://127.0.0.1:8000/author/88939ffa-c45d-4c10-a4f0-252ccf87740c",

	}
}
```

### Profiles

**GET service/author/{AUTHOR_ID}**: returns the profile associated with AUTHOR_ID.

Response:
```
{
    "id": "http://127.0.0.1:8000/1900e266-dd80-455b-b9dd-abf09c14116e",
    "host": "http://127.0.0.1:8000/",
    "displayName": "zredfern",
    "url": "http://127.0.0.1:8000/home/profile/1900e266-dd80-455b-b9dd-abf09c14116",
    "friends": [
        {
            "id": "http://127.0.0.1:8000/88939ffa-c45d-4c10-a4f0-252ccf87740c",
            "host": "http://127.0.0.1:8000/",
            "displayName": "bpanda",
            "url": "http://127.0.0.1:8000/home/profile/88939ffa-c45d-4c10-a4f0-252ccf87740c"
        }
    ],
    "github": "Z-Red",
    "firstName": "Zach",
    "lastName": "Redfern",
    "email": "zachredfern@hotmail.com",
    "bio": "Just a regular d00d."
}
```
