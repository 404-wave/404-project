# 404-project
CMPUT 404 Distributed Social Network

Promo Video: https://www.youtube.com/watch?v=7JXo1xYwdx4

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

**GET /author/posts/**: returns all posts *visible to the currently authenticated user* from our server *and our connected nodes* **only if the request came from an author that we are hosting**. The point here is that we could call our own endpoint to get the posts an author could see. However, we **stronlgy disagree** that we should be sharing posts from our connected nodes with our other connected nodes. For this reason, if the request _came from_ one of our connected nodes then they will _not receive foreign posts_. E.g., requests for posts that came from nodes will only be returned posts hosted on our server. Two example CURL wil be provided to highlight the difference.

**GET /posts/**: returns all publicly available posts that exist on *our server only*. That is, posts from other servers will *not* be shown when this endpoint is called. This is in coordination with the requirement, "a GET without a postfixed “postid” should return a list of all “PUBLIC” visibility posts ***on your node***"

**GET /author/{AUTHOR_ID}/posts/**: returns all posts from AUTHOR_ID that are *visible to the currently authenticated user* that exist on *our server only*. That is, for an {AUTHOR_ID} that is *not* hosted on our server, you will *not* see their posts.

**GET /posts/{POST_ID}/**: returns a single post *if it is visible to the currently authenticated user* and that post exists on *our server only*. This will not get a post that is hosted on another server.

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
            "id": "a27b37c4-bae9-4b15-9b01-e1c2f1def47e",
            "user": "8ac6dd85-2f2f-4b40-8188-791bfd215dfc",
            "contentType": "text/plain",
            "categories": [],
            "description": "Text post",
            "published": "2019-04-02T13:58:47.164233+00:00",
            "title": "gary1 - Apr 2, 2019, at 13:58 PM",
            "content": "Hello! My name is Gary. Everyday I release new cat facts. Follow me and let's chat chat(fr)!",
            "author": {
                "id": "8ac6dd85-2f2f-4b40-8188-791bfd215dfc",
                "host": "https://cmput404-wave.herokuapp.com",
                "displayName": "gary1",
                "url": "https://cmput404-wave.herokuapp.com/author/8ac6dd85-2f2f-4b40-8188-791bfd215dfc",
                "github": ""
            },
            "comments": [
                {
                    "author": {
                        "id": "f6ea3270-3e4d-4547-9ee6-8def7f1fe01a",
                        "url": "https://myblog-cool.herokuapp.com/service/author/f6ea3270-3e4d-4547-9ee6-8def7f1fe01a",
                        "host": "https://myblog-cool.herokuapp.com/",
                        "displayName": "Jackson0",
                        "github": "https://github.com/Zhipeng-Chang/"
                    },
                    "comment": "Hi Gary!",
                    "published": "2019-04-02T14:32:30.324495Z",
                    "id": "6ebffa4e-0100-4136-8de2-ecd1ac045c96"
                }
            ],
            "visibility": "PUBLIC",
            "visibleTo": null,
            "unlisted": false,
            "source": "https://cmput404-wave.herokuapp.com/posts/a27b37c4-bae9-4b15-9b01-e1c2f1def47e/",
            "origin": "https://cmput404-wave.herokuapp.com/posts/a27b37c4-bae9-4b15-9b01-e1c2f1def47e/"
        }
    ]
}
```

**POST service/posts/{POST_ID}**: insert a new post. The restriction that we impose for this is that the author's ID must match a valid user that we host on *our server*.

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

### Comments

**GET service/posts/{POST_ID}/comments/**: returns all comments in a post if the post is visible to the currently authenticated user, and that post is hosted on *our server*.

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
                "id": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                "url": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
                "host": "https://cmput404-wave.herokuapp.com",
                "displayName": "waveAdmin",
                "github": "Z-Red"
            },
            "comment": "Wow what a great post, on such a great website.",
            "published": "2019-03-28T21:41:15.965975Z",
            "id": "11085ac2-25a6-4ef3-8b2e-ade3f1e02eed"
        },
    ]
}
```

**POST service/posts/{POST_ID}/comments/**: add a new comment to an existing post, only if that post is hsoted on *our server*.

Example of what to POST:
```
{
    "query": "addComment",
    "post": "3f46f9c3-256f-441c-899e-928b095df627",
    "comment": {
        "author": {
            "id": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
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
        "https://cmput404-wave.herokuapp.com/service/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
        "https://cmput-404-proj-test.herokuapp.com/service/author/fc9239c0-5d8c-451c-847b-b68d26a40df9"
    ]
}
```

~~**GET service/author/{AUTHOR_ID1>/friends/{AUTHOR_ID2}**: returns a response specifying if AUTHOR_ID1 is a friend of AUTHOR_ID2. AUTHOR_ID1 is from our server and AUTHOR_ID2 is a foreign server. Hostname is the host of AUTHOR_ID2.~~ We are using a modified endpoint that achieves the same thing. Please refer below...

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

**POST service/friendrequest**: accepts two authors and creates a friend request if they are not already friends. Author is the user from our server and friend is the requesting user from a foreign server.

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
    "id": "https://cmput-404-proj-test.herokuapp.com/author/39500b60-210f-4318-81e0-08e18489d77e",
    "host": "https://cmput-404-proj-test.herokuapp.com",
    "displayName": "waveTestAdmin",
    "url": "https://cmput-404-proj-test.herokuapp.com/author/39500b60-210f-4318-81e0-08e18489d77e",
    "friends": [
        {
            "id": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f",
            "host": "https://cmput404-wave.herokuapp.com",
            "displayName": "waveAdmin",
            "url": "https://cmput404-wave.herokuapp.com/author/da986903-8f86-4fc3-ba02-69ef5e6e6e9f"
        },
        {
            "id": "https://cmput-404-proj-test.herokuapp.com/author/fc9239c0-5d8c-451c-847b-b68d26a40df9",
            "host": "https://cmput-404-proj-test.herokuapp.com",
            "displayName": "boopbop",
            "url": "https://cmput-404-proj-test.herokuapp.com/author/fc9239c0-5d8c-451c-847b-b68d26a40df9"
        }
    ],
    "github": "Z-Red",
    "firstName": "Zach",
    "lastName": "Redfern",
    "email": "zred@gmail.com",
    "bio": "\"I like to party\" - Andy Samberg"
}
```
