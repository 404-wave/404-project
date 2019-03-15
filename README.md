# 404-project
CMPUT 404 Distributed Social Network


# Licensing and Contributors

Generally, everything is licensed under Apache 2 by [Z-Red](https://github.com/Z-Red).

Contributors: </br>
`
Araien Zach Redfern <br>
Austin PennyFeather <br>
Kerry Li <br>
Allison Boukall <br>
Shu-Jun Pierre Lin <br>


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
