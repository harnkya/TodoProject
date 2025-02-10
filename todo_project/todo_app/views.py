# fonksiyonlar class'lar burada

import time
from gc import get_objects
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import title
from scripts.regsetup import description

from .models import Todos, Projects
from .forms import ListForm
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:  # user varsa
            login(request, user)
            messages.success(request, "Login Successfully")
            print("login success")
            return redirect("projects")
        else:
            messages.warning(request, "Invalid Username or Password")
            print("login olmadi")
            return render(request, "todo_app/login.html")
    else:
        if request.user.is_authenticated:  # giriş yapmış kullanıcının tekrar giriş yapmaya çalışması
            return redirect("projects")
        return render(request, "todo_app/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return render(request, "todo_app/login.html")


def register_view(request):
    # username'ler eşsiz olmalıymış...

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if authenticate(request, username=username, password=password):
            messages.warning(request, "User already exists")
            print("user exist")
            return redirect("register")
        else:

            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                messages.success(request, "User Created Successfully")
                return redirect("projects")
            except Exception:
                print("exception")
                messages.warning(request, "Username already exists")
                return redirect("register")
    else:
        return render(request, "todo_app/register.html")


@login_required(login_url="login")
def projects(request):  # bu sadece projectleri getirecek, hızlı proje ekleme kısmını yapmadım henüz belki de yapmam
    projects = Projects.objects.filter(user=request.user)
    return render(request, "todo_app/projects.html", {"projects": projects})


@login_required(login_url="login")
def project_details(request, project_id):
    if request.method == "POST":  # burada project title ve description değişiyor
        print("ifte")
        title = request.POST.get("title")
        description = request.POST.get("description")
        project = get_object_or_404(Projects, id=project_id, user=request.user)
        project.title = title
        project.description = description
        project.save()
        todo_list = Todos.objects.filter(user=request.user, Project=project, )
        messages.success(request, "Project details changed successfully ")
        # return redirect("project_details", project_id=project_id)
        # render(request, "todo_app/project_details.html", {"project": project, "todo_list": todo_list})
        return redirect("projects")

    else:  # buradası da sayfa ilk kez yüklenirken
        project = get_object_or_404(Projects, user=request.user, id=project_id)
        todo_list = Todos.objects.filter(user=request.user, Project=project, )
        return render(request, "todo_app/project_details.html", {"project": project, "todo_list": todo_list})


@login_required(login_url="login")
def delete_project(request, project_id):
    try:
        project = get_object_or_404(Projects, user=request.user, id=project_id)
        project.delete()
        messages.success(request, "Project Deleted Successfully")
        print("ife girdi başarılı bir şekilde sildi")
        return redirect("projects")
    except Exception as e:
        messages.error(request, "Project Delete Error!")
        print("if'e düştü hata da şu: " + e)
        return redirect("projects")


@login_required(login_url="login")
def create_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            description = request.POST.get("description")
            user = request.user
            finished = request.POST.get("finished")
            finished = True if finished == "on" else False
            Projects.objects.create(title=title, description=description, user=user, finished=finished)
            messages.success(request, "Project Created Successfully")
            return redirect("projects")
        else:
            print("else e düştü")
            messages.warning(request, "Title can not be empty")
            return redirect("create_project")
    else:
        return render(request, "todo_app/create_project.html")


def create_todo(request):  # title description finished project_id gelecek oradan yürü
    title = request.POST.get("title")
    if title:
        project_id = request.POST.get("project_id")
        description = request.POST.get("description")
        print("ife girebildi")
        print(project_id)
        finished = True if request.POST.get("finished") == "on" else False
        project = Projects.objects.filter(id=int(project_id), user=request.user).first()
        Todos.objects.create(title=title, description=description, finished=finished, Project=project,
                             user=request.user)
        messages.success(request, "Todo Created Successfully")
        print(request.POST.get("project_id"))
        return redirect("project_details", project_id)
    else:
        messages.warning(request, "Title can not be empty")
        project_id = request.POST.get("project_id")
        print(project_id)
        return render(request, "todo_app/create_todo.html", {"project_id": project_id})


def load_create_todo(request):
    if request.method == "POST":
        print("else'de sayfayı ilk kez yükledi")
        project_id = request.POST.get("project_id")
        print(project_id)
        return render(request, "todo_app/create_todo.html", {"project_id": project_id})


def about(request):
    return render(request, "todo_app/about.html")


def yes_finish_project(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = get_object_or_404(Projects, id=project_id, user=request.user)
        project.finished = True
        project.save()
        messages.success(request, "Project marked as finished successfully!")
        return redirect("projects")
    else:
        print("else")


def no_finish_project(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = get_object_or_404(Projects, id=project_id, user=request.user)
        project.finished = False
        project.save()
        messages.success(request, "Project marked as unfinished successfully!")
        return redirect("projects")
        return redirect("projects")
    else:
        print("else")


def yes_finish_todo(request):
    if request.method == "POST":
        todo_id = request.POST.get("todo_id")
        todo = get_object_or_404(Todos, id=todo_id, user=request.user)
        todo.finished = True
        todo.save()
        messages.success(request, "Todo marked as finished!")
        project_id = todo.Project_id
        return redirect("project_details", project_id=project_id)
    else:
        print("Forbidden request!")


def no_finish_todo(request):
    if request.method == "POST":
        todo_id = request.POST.get("todo_id")
        todo = get_object_or_404(Todos, id=todo_id, user=request.user)
        todo.finished = False
        todo.save()
        messages.success(request, "Todo marked as unfinished!")
        project_id = todo.Project_id
        return redirect("project_details", project_id=project_id)
    else:
        print("Forbidden request!")


def todo_details(request):
    # sayfayı 1 kez yükleyip  bırakacak
    if request.method == "POST":
        todo_id = request.POST.get("todo_id")
        todo = get_object_or_404(Todos, id=todo_id, user=request.user)
        return render(request, "todo_app/todo_details.html", {"todo": todo})
    else:
        print("else e düştü, burası invalid")


def todo_update(request):
    if request.method == "POST":
        title = request.POST.get("title")
        todo_id = request.POST.get("todo_id")
        todo = get_object_or_404(Todos, id=todo_id)
        if title:
            description = request.POST.get("description")
            todo.title = title
            todo.description = description
            todo.save()
            messages.success(request, "Todo updated successfully!")
            print("ifte")
            project_id = todo.Project_id
            return redirect("project_details", project_id=project_id)
        else:
            messages.warning(request, "Title can not be empty!")
            print("elsede ")
            return render(request, "todo_app/todo_details.html", {"todo": todo})


def delete_todo(request):
    if request.method == "POST":
        todo_id = request.POST.get("todo_id")
        todo = get_object_or_404(Todos, id=todo_id)
        todo.delete()
        messages.success(request, "Todo deleted successfully!")
        return redirect("project_details", project_id=todo.Project.id)
    else:
        messages.error(request, "Invalid request method.")
        print("delete_todo else'i")
