from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *

#Page views
def index(request):
    if "logged" not in request.session:
        request.session["logged"]       = False
        request.session["userID"]       = -1
        request.session["first_name"]   = ""
        request.session["last_name"]    = ""
        request.session["email"]        = ""
    else:
        if request.session["logged"]:
            return redirect("/projects")
    return render(request, "scrumptious/index.html")

def register(request):
    return render(request, "scrumptious/register.html")

def login(request):
    return render(request, "scrumptious/login.html")

def userProfile(request):
    user = User.objects.get(id=request.session["userID"])
    context = {
        "user" : user
    }
    return render(request, "scrumptious/userProfile.html",context)

def projects(request):
    user    = User.objects.get(id=request.session["userID"])
    boards  = user.user_boards.all()
    context = {
        "user"      : user,
        "boards"    : boards
    }
    return render(request,"scrumptious/projects.html",context)

def board(request,boardID):
    board = Board.objects.get(id=boardID)
    lists = board.board_lists.all()
    context = {
        "board" : board,
        "lists"  : lists
    }
    return render(request,"scrumptious/board.html",context)


#Actions
def registerUser(request):
    errors = User.objects.validate_registration(request.POST)
    request.session["first_name"]   = request.POST["first_name"]
    request.session["last_name"]    = request.POST["last_name"]
    request.session["email"]        = request.POST["email"]

    if errors:
        for key in errors:
            for error in errors[key]:
                messages.error(request, error, extra_tags="registration")

        return redirect("/register")
    else:
        newUser = User.objects.create(
            first_name  = request.POST["first_name"],
            last_name   = request.POST["last_name"],
            email       = request.POST["email"],
            password    = bcrypt.hashpw(request.POST["password"].encode(),bcrypt.gensalt()).decode()
        )
        print(newUser)
        #store session vars
        request.session["userID"] = newUser.id
        request.session["logged"] = True

    return redirect("/projects")

def loginUser(request):
    errors = User.objects.validate_login(request.POST)

    if errors:
        for key in errors:
            for error in errors[key]:
                messages.error(request, error, extra_tags="login")
        redirect("/login")
    else:
        user = User.objects.get(email=request.POST["email"])
        
        #store session vars
        request.session["logged"] = True
        request.session["userID"] = user.id
        
    return redirect("/projects")

def logout(request):
    request.session.clear()
    return redirect("/")

def updateUser(request):
    user = User.objects.get(id=request.POST["userID"])
    user.first_name = request.POST["first_name"]
    user.last_name = request.POST["last_name"]
    user.email = request.POST["email"]
    user.save()
    
    return redirect("/profile")

###### Board routes ######
def createBoard(request):
    user        = User.objects.get(id=request.session["userID"])
    newBoard    = Board.objects.create(name=request.POST["name"],desc="")
    newBoard.board_users.add(user)
    return redirect("/projects")

def addList(request):
    boardID = request.POST["boardID"]
    board   = Board.objects.get(id=boardID)
    List.objects.create(name=request.POST["name"],board=board)
    return redirect("/board/"+boardID)

def addTask(request):
    user        = User.objects.get(id=request.session["userID"])
    boardID     = request.POST["boardID"]
    listID      = List.objects.get(id=request.POST["listID"])
    listCount   = len(List.objects.get(id=request.POST["listID"]).list_tasks.all())

    newTask = Task.objects.create(
        name        = request.POST["name"],
        desc        = request.POST["desc"],
        list_id     = listID,
        order       = listCount+1
    )
    newTask.users.add(user)

    return redirect("/board/"+boardID)

def taskEditModal(request):
    print("GET: ",request.GET)
    # for key in request.GET:
    #     data = json.loads(key)
    # print(data)
    context = {
        "task"  : Task.objects.get(id=request.GET["task"]),
        "board" : Board.objects.get(id=request.GET["board"])
    }
    return render(request,"scrumptious/taskModal.html",context)
    # return HttpResponse("hello")

def updateTask(request):
    print(request.method)
    print(request.POST["boardID"])
    boardID = request.POST["boardID"]
    task    = Task.objects.get(id=request.POST["taskID"])

    #update task
    task.name = request.POST["name"]
    task.desc = request.POST["desc"]
    task.save()

    return redirect("/board/"+boardID)

def updateList(request):
    #load json sting
    for key in request.GET:
        data = json.loads(key)
    print(data)
    #update order for each item in list
    for index in data['data']:
        list_id = List.objects.get(id=index[2])
        task = Task.objects.get(id=index[0])
        task.order      = index[1]
        task.list_id    = list_id
        task.save()
    return HttpResponse("successfully updated order")

def addComment(request):
    print("METHOD:",request.POST)
    user    = User.objects.get(id=request.session["userID"])
    task    = Task.objects.get(id=request.POST["taskID"])
    board   = Board.objects.get(id=request.POST["boardID"])
    comment = request.POST["comment_content"]
    
    # Add comment
    c = Comment.objects.create(content=comment,task=task,user=user)
    print(c)

    
    context = {
        "task"      : task,
        "board"     : board,
        "comments"  : task.task_comments.all(),
    }

    return render(request,"scrumptious/taskModal.html",context)

def deleteComment(request):
    print("METHOD:",request.GET)

    task    = Task.objects.get(id=request.GET["task"])
    board   = Board.objects.get(id=request.GET["board"])
    comment = Comment.objects.get(id=request.GET["comment"])
    
    # Add comment
    comment.delete()

    
    context = {
        "task"      : task,
        "board"     : board,
        "comments"  : task.task_comments.all(),
    }

    return render(request,"scrumptious/taskModal.html",context)