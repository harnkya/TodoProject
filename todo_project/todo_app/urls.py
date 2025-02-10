from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("projects", views.projects, name="projects"),
    path("create_project", views.create_project, name="create_project"),
    path("create_todo", views.create_todo, name="create_todo"),
    path("project_details/<int:project_id>", views.project_details, name="project_details"),
    path("delete_project/<int:project_id>", views.delete_project, name="delete_project"),
    path("logout", views.logout_view, name="logout"),
    path("about", views.about, name="about"),
    path("yes_finish_project", views.yes_finish_project, name="yes_finish_project"),
    path("no_finish_project", views.no_finish_project, name="no_finish_project"),
    path("no_finish_todo", views.no_finish_todo, name="no_finish_todo"),
    path("yes_finish_todo", views.yes_finish_todo, name="yes_finish_todo"),
    path("todo_details", views.todo_details, name="todo_details"),
    path("todo_update", views.todo_update, name="todo_update"),
    path("delete_todo", views.delete_todo, name="delete_todo"),
    path("load_create_todo", views.load_create_todo, name="load_create_todo")

]
