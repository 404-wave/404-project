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

Below there is a list of which endpoints are currently working. For posts and comments, it is required to send a header with the requesting user's UUID in the following format: ```X-UUID: {UUID}```. This is required to resolve the privacy concerns of various posts. That is, to determine whether the requesting user can or cannot view the post(s) in question.

Note: Pagination works for any endpoint endpoint related to posts or comments.

### Posts

**GET /author/posts**: returns all posts *visible to the currently authenticated user*.

**GET /posts**: returns all publicly available posts.

**GET /author/{AUTHOR_ID}/posts**: returns all posts from AUTHOR_ID that are *visible to the currently authenticated user*.

**GET /posts/{POST_ID}**: returns a single post *if it is visible to the currently authenticated user*.

An example response:
```
{
    "query": "posts",
    "count": 1,
    "size": 50,
    "next": null,
    "previous": null,
    "posts": [
        {
            "id": "3f46f9c3-256f-441c-899e-928b095df627",
            "user": "54cfdb16-7de4-4ce0-ac7a-68d6e4d90c76",
            "contentType": "text/plain",
            "categories": [],
            "description": "Text post",
            "published": "2019-03-28T02:13:27.833710Z",
            "title": "zredfern - Mar 28, 2019, at 02:13 AM",
            "content": "A public post by Zach.",
            "author": {
                "id": "54cfdb16-7de4-4ce0-ac7a-68d6e4d90c76",
                "host": "https://cmput404-wave.herokuapp.com/",
                "displayName": "zredfern",
                "url": "https://cmput404-wave.herokuapp.com/author/54cfdb16-7de4-4ce0-ac7a-68d6e4d90c76",
                "github": ""
            },
            "comments": [
                {
                    "author": {
                        "id": "da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                        "url": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                        "host": "https://cmput404-wave.herokuapp.com",
                        "displayName": "waveAdmin",
                        "github": ""
                    },
                    "comment": "Hello zach -- from admin.",
                    "published": "2019-03-28T19:45:28.545575Z",
                    "id": "5c7a0c2f-2163-48f3-995e-16d5642bf9a5"
                },
                {
                    "author": {
                        "id": "da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                        "url": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                        "host": "https://cmput404-wave.herokuapp.com",
                        "displayName": "waveAdmin",
                        "github": ""
                    },
                    "comment": "A POSTed comment for Zach by the Admin.",
                    "published": "2019-03-28T19:49:25.440094Z",
                    "id": "6840c410-7e4a-4c04-9a70-be7440c77100"
                },
                {
                    "author": {
                        "id": "da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                        "url": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                        "host": "https://cmput404-wave.herokuapp.com",
                        "displayName": "waveAdmin",
                        "github": ""
                    },
                    "comment": "Hi This is allison",
                    "published": "2019-03-29T16:37:50.323741Z",
                    "id": "99a7dc64-19c3-42a7-929c-bf7860c0a647"
                }
            ],
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": false,
            "source": "https://cmput404-wave.herokuapp.com/posts/3f46f9c3-256f-441c-899e-928b095df627/",
            "origin": "https://cmput404-wave.herokuapp.com/posts/3f46f9c3-256f-441c-899e-928b095df627/"
        }
    ]
}
```


**POST service/posts/{POST_ID}**: insert a new post.

An example of what to POST (this is all that we require):
```
{
	"contentType":"text/plain",
	"content":"Here is some POSTed post content. Neat-o!",
	"author":{ "id":"http://127.0.0.1:8000/author/4a47a810-4b00-4c59-8ec3-e0d4ac0b74fc"},
	"visibility":"PRIVATE",
	"visibleTo":["0a38f43f-0467-48a4-ba28-d9ae3a4a88b5"],
    	"unlisted":false
}
```

##### TODO...

PUT service/posts/{POST_ID}: update an existing post.

### Comments

**GET service/posts/{POST_ID}/comments**: returns all comments in a post if the post is visible to the currently authenticated user.

Response:
```
{
    "query": "comments",
    "count": 1,
    "size": 50,
    "next": null,
    "previous": null,
    "comments": [
        {
            "author": {
                "id": "da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                "url": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                "host": "https://cmput404-wave.herokuapp.com",
                "displayName": "waveAdmin",
                "github": ""
            },
            "comment": "a comment",
            "published": "2019-03-28T21:41:15.965975Z",
            "id": "11085ac2-25a6-4ef3-8b2e-ade3f1e02eed"
        },
    ]
}
```

##### TODO...

**POST service/posts/{POST_ID}/comments**: add a new comment to an existing post.

Example of what to POST:
```
{
    "query": "addComment",
    "post": "3f46f9c3-256f-441c-899e-928b095df627",
    "comment": {
        "author": {
            "id": "da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
            "host": "https://cmput404-wave.herokuapp.com/",
            "url": "https://cmput404-wave.herokuapp.com/service/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
            "github": ""
        },
        "comment": "A POSTed comment for Zach by the Admin.",
        "content_type": "text/plain",
        "published": "2019-03-27T21:44:20.004517",
        "id": "42e37403-ca6b-4733-9af6-33c02fd58797"
    }
}
```

### Friendship

**GET service/author/{AUTHOR_ID}/friends**: returns all friends of AUTHOR_ID.

Response:
```
{
    "query": "friends",
    "authors": [
        "http://127.0.0.1:8000/service/author/88939ffa-c45d-4c10-a4f0-252ccf87740c",
        "http://127.0.0.1:3000/service/author/8e8b3k23-xx2s-dd2f-z3x1-1231df8i340c",
        ...
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

Example request:
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

Example response:
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

Example request:
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

Example response:
```
{
    "id": "da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
    "host": "https://cmput404-wave.herokuapp.com",
    "displayName": "waveAdmin",
    "url": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
    "friends": [
    	{
            "id": "https://cmput404-wave.herokuapp.com/88939ffa-c45d-4c10-a4f0-252ccf87740c",
            "host": "https://cmput404-wave.herokuapp.com",
            "displayName": "bpanda",
            "url": "https://cmput404-wave.herokuapp.com/author/88939ffa-c45d-4c10-a4f0-252ccf87740c"
        }
    ],
    "github": "",
    "firstName": "Wave",
    "lastName": "Admin",
    "email": "waveadmin@gmail.com",
    "bio": "newnew"
}
```
