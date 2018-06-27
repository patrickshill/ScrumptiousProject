from django.db import models
import bcrypt
import re

REGEX_EMAIL = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

#Managers
class UserManager(models.Manager):
    def validate_registration(self, postData):
        valid = True
        errors = {
            "first_name"    : [],
            "last_name"     : [],
            "email"         : [],
            "password"      : []
        }

        #Validate first_name
        if len(postData["first_name"]) < 2:
            valid = False
            errors["first_name"].append("First name must contain at least 2 characters")
        if not postData["first_name"].isalpha():
            errors["first_name"].append("First name can only contain letters")
        
        #Validate last_name
        if len(postData["last_name"]) < 2:
            valid = False
            errors["last_name"].append("Last name must contain at least 2 characters")
        if not postData["last_name"].isalpha():
            valid = False
            errors["last_name"].append("Last name can only contain letters")

        #Validate email
        if len(postData["email"]) < 2:
            valid = False
            errors["email"].append("Must proivde an email address")
        elif not re.match(REGEX_EMAIL,postData["email"]):
            valid = False
            errors["email"].append("Invalid email address")

        #Validate password
        if len(postData["password"]) < 8:
            valid = False
            errors["password"].append("Password must be at least 8 characters")
        elif postData["password"] != postData["password_confirm"]:
            valid = False
            errors["password"].append("Passwords do not match")

        #Return errors if not valid
        if not valid:
            return errors

        #Return false and create new user in views
        return False


    def validate_login(self, postData):
        valid = True
        errors = {
            "login" : []
        }

        #check if user exists
        if not User.objects.filter(email=postData["email"]).exists():
            valid = False
        else:
            user = User.objects.get(email=postData["email"])
            #check password
            if not bcrypt.checkpw(postData["password"].encode(),user.password.encode()):
                valid = False

        #Return errors if not valid
        if not valid:
            errors["login"].append("Incorrect username or password")
            return errors
        
        #Return false and login user in views
        return False

#Models
class User(models.Model):
    first_name      = models.CharField(max_length=255)
    last_name       = models.CharField(max_length=255)
    email           = models.CharField(max_length=255)
    password        = models.CharField(max_length=255)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    objects         = UserManager()

class Board(models.Model):
    name            = models.CharField(max_length=255)
    desc            = models.TextField()
    board_users     = models.ManyToManyField(User,related_name="user_boards")
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

class List(models.Model):
    name            = models.CharField(max_length=255)
    board           = models.ForeignKey(Board, on_delete=models.CASCADE,related_name="board_lists")
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

class Task(models.Model):
    name            = models.CharField(max_length=255)
    desc            = models.TextField()
    list_id         = models.ForeignKey(List,on_delete=models.CASCADE,related_name="list_tasks")
    users           = models.ManyToManyField(User,related_name="user_tasks")
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content         = models.TextField()
    task            = models.ForeignKey(Task,on_delete=models.CASCADE,related_name="task_comments")
    user            = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_comments")

