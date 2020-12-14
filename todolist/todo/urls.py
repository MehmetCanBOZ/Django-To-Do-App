from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("todo",views.todo,name="todo"),
    path("todo/<int:list_id>",views.listitem,name="listitem"),
    path("todo/<int:list_id>/add",views.additem,name="additem"),
    path("todo/<int:list_id>/completed",views.complete,name="complete"),
    path("todo/<int:list_id>/expired", views.expired, name="expired"),
    path("todo/<int:list_id>/delete",views.deletetodo,name="deletetodo"),
    path("todo/<int:list_id>/<int:item_id>",views.done,name="done"),
    path("addtodo",views.addtodo,name="addtodo"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]